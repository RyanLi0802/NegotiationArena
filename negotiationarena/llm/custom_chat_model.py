import openai
import os
import sys
import uuid
import json
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    BaseMessageChunk,
    ChatMessage,
    ChatMessageChunk,
    FunctionMessage,
    FunctionMessageChunk,
    HumanMessage,
    HumanMessageChunk,
    InvalidToolCall,
    SystemMessage,
    SystemMessageChunk,
    ToolCall,
    ToolMessage,
    ToolMessageChunk,
)
from langchain_core.language_models import BaseChatModel, SimpleChatModel, LanguageModelInput
from langchain_core.language_models.llms import create_base_retry_decorator
from langchain_core.messages import AIMessageChunk, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import run_in_executor, Runnable
from langchain_core.output_parsers.openai_tools import (
    JsonOutputKeyToolsParser,
    PydanticToolsParser,
    make_invalid_tool_call,
    parse_tool_call,
)
from langchain_core.utils import secret_from_env
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.tools import BaseTool
# from langchain_community.adapters.openai import (
#     convert_dict_to_message,
#     convert_message_to_dict,
# )
# from langchain_openai import ChatOpenAI
# from langchain_openai.chat_models import _convert_dict_to_message
from langchain_community.chat_models.openai import ChatOpenAI
from negotiationarena.llm.prompt_utils import bind_tools_to_system_prompt
from negotiationarena.llm.utils import parse_llm_output


def _convert_message_to_dict(message: BaseMessage) -> dict:
    """Convert a LangChain message to a dictionary.

    Args:
        message: The LangChain message.

    Returns:
        The dictionary.
    """
    message_dict: Dict[str, Any]
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
        if "function_call" in message.additional_kwargs:
            message_dict["function_call"] = message.additional_kwargs["function_call"]
            # If function call only, content is None not empty string
            if message_dict["content"] == "":
                message_dict["content"] = None
        if "tool_calls" in message.additional_kwargs:
            message_dict["tool_calls"] = message.additional_kwargs["tool_calls"]
            # If tool calls only, content is None not empty string
            if message_dict["content"] == "":
                message_dict["content"] = None
        if "full_message" in message.additional_kwargs and message.additional_kwargs["full_message"]:
            # full_message is not empty, replace the current content with full message
            message_dict["content"] = message.additional_kwargs["full_message"]
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    elif isinstance(message, FunctionMessage):
        message_dict = {
            "role": "function",
            "content": message.content,
            "name": message.name,
        }
    elif isinstance(message, ToolMessage):
        run_results = {
            "name": message.name,
            "id": message.tool_call_id,
            "return_value": message.content
        }
        message_dict = {
            "role": "user",
            "content": "Tool call results:\n" + json.dumps(run_results, indent=4),
            "tool_call_id": message.tool_call_id,
        }
    else:
        raise TypeError(f"Got unknown type {message}")
    if "name" in message.additional_kwargs:
        message_dict["name"] = message.additional_kwargs["name"]
    return message_dict


def _convert_dict_to_message(_dict: Mapping[str, Any]) -> BaseMessage:
    """Convert a dictionary to a LangChain message.

    Args:
        _dict: The dictionary.

    Returns:
        The LangChain message.
    """
    role = _dict.get("role")
    name = _dict.get("name")
    id_ = _dict.get("id")
    if role == "user":
        return HumanMessage(content=_dict.get("content", ""), id=id_, name=name)
    elif role == "assistant":
        # Fix for azure
        # Also OpenAI returns None for tool invocations
        content = _dict.get("content", "") or ""
        additional_kwargs: Dict = {}
        if function_call := _dict.get("function_call"):
            additional_kwargs["function_call"] = dict(function_call)
        if full_message := _dict.get("full_message"):
            additional_kwargs["full_message"] = full_message
        tool_calls = []
        invalid_tool_calls = []
        if raw_tool_calls := _dict.get("tool_calls"):
            additional_kwargs["tool_calls"] = raw_tool_calls
            for raw_tool_call in raw_tool_calls:
                try:
                    tool_calls.append(ToolCall(name=raw_tool_call['function']['name'], args=raw_tool_call['function']['arguments'], id=raw_tool_call['id'], type="tool_call"))
                except Exception as e:
                    invalid_tool_calls.append(
                        make_invalid_tool_call(str(raw_tool_call), str(e))
                    )
        # print(tool_calls)
        # print()
        # print(invalid_tool_calls)
        return AIMessage(
            content=content,
            additional_kwargs=additional_kwargs,
            name=name,
            id=id_,
            tool_calls=tool_calls,
            invalid_tool_calls=invalid_tool_calls,
        )
    elif role == "system":
        return SystemMessage(content=_dict.get("content", ""), name=name, id=id_)
    elif role == "function":
        return FunctionMessage(
            content=_dict.get("content", ""), name=cast(str, _dict.get("name")), id=id_
        )
    elif role == "tool":
        additional_kwargs = {}
        if "name" in _dict:
            additional_kwargs["name"] = _dict["name"]
        return ToolMessage(
            content=_dict.get("content", ""),
            tool_call_id=cast(str, _dict.get("tool_call_id")),
            additional_kwargs=additional_kwargs,
            name=name,
            id=id_,
        )
    else:
        return ChatMessage(content=_dict.get("content", ""), role=role, id=id_)  # type: ignore[arg-type]

class CustomChatModel(ChatOpenAI):
    model_type: str = Field(default="custom-chat")
    tools: Optional[List[Any]] = None
    
    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"openai_api_key": "EMPTY"}
    
    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return self.model_type + "-chat"
    
    def bind_tools(
        self,
        tools: Sequence[Union[Dict[str, Any], Type, Callable, BaseTool]],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind tool-like objects to this chat model.

        Assumes model is compatible with OpenAI tool-calling API.

        Args:
            tools: A list of tool definitions to bind to this chat model.
                Supports any tool definition handled by
                :meth:`langchain_core.utils.function_calling.convert_to_openai_tool`.
            tool_choice: Which tool to require the model to call.
                Must be the name of the single provided function or
                "auto" to automatically determine which function to call
                (if any), or a dict of the form:
                {"type": "function", "function": {"name": <<tool_name>>}}.
            kwargs: Any additional parameters are passed directly to
                ``self.bind(**kwargs)``.
        """
        formatted_tools = [convert_to_openai_tool(tool) for tool in tools]
        
        self.tools = formatted_tools
        return super().bind(tools=formatted_tools, **kwargs)
    
    
    def bind_functions(
        self,
        functions: Sequence[Union[Dict[str, Any], Type[BaseModel], Callable]],
        function_call: Optional[str] = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind functions (and other objects) to this chat model.

        Args:
            functions: A list of function definitions to bind to this chat model.
                Can be  a dictionary, pydantic model, or callable. Pydantic
                models and callables will be automatically converted to
                their schema dictionary representation.
            function_call: Which function to require the model to call.
                Must be the name of the single provided function or
                "auto" to automatically determine which function to call
                (if any).
            kwargs: Any additional parameters to pass to the
                :class:`~langchain.runnable.Runnable` constructor.
        """
        from langchain.chains.openai_functions.base import convert_to_openai_function

        formatted_functions = [convert_to_openai_function(fn) for fn in functions]
        self.tools = formatted_tools
        if function_call is not None:
            if len(formatted_functions) != 1:
                raise ValueError(
                    "When specifying `function_call`, you must provide exactly one "
                    "function."
                )
            if formatted_functions[0]["name"] != function_call:
                raise ValueError(
                    f"Function call {function_call} was specified, but the only "
                    f"provided function was {formatted_functions[0]['name']}."
                )
            function_call_ = {"name": function_call}
            kwargs = {**kwargs, "function_call": function_call_}
        return super().bind(
            functions=formatted_functions,
            **kwargs,
        )
    
    def _create_message_dicts(
        self, messages: List[BaseMessage], stop: Optional[List[str]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        params = self._client_params
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop"] = stop
        message_dicts = [_convert_message_to_dict(m) for m in messages]
        if self.tools:
            has_system_prompt = False
            for msg in message_dicts:
                if msg['role'] == 'system':
                    system_prompt = msg['content']
                    msg['content'] = bind_tools_to_system_prompt(system_prompt, self.tools)
                    has_system_prompt = True
                    break
            if not has_system_prompt:
                system_prompt = "You are a helpful assistant"
                message_dicts = [{
                    'role': 'system',
                    'content': bind_tools_to_system_prompt(system_prompt, self.tools),
                }] + message_dicts

        return message_dicts, params
    
    def _create_chat_result(self, response: Union[dict, BaseModel]) -> ChatResult:
        generations = []
        if not isinstance(response, dict):
            response = response.dict()
        for res in response["choices"]:
            if self.tools:
                # attempt to parse the tool calls
                full_message = res["message"]["content"]
                scratchpad, parsed_message = parse_llm_output(full_message)
                if parsed_message['type'] == 'text_message':
                    # res["message"]['full_message'] = full_message
                    res["message"]["content"] = parsed_message["content"]
                else:
                    assert parsed_message['type'] == 'tool_calls'
                    tool_calls = []
                    for tool_call in parsed_message['content']:
                        if 'id' not in tool_call:
                            tool_call['id']  = 'call_' + str(uuid.uuid4())
                        tool_calls.append({
                            'id': tool_call['id'],
                            'type': 'function',
                            'function': {
                                'name': tool_call['name'],
                                'arguments': tool_call['arguments']
                            }
                        })
                    res["message"]["tool_calls"] = tool_calls
                    res["message"]['content'] = None
                    res['finish_reason'] = 'tool_calls'
            res["message"]['full_message'] = scratchpad + json.dumps(parsed_message, indent=4)
            message = _convert_dict_to_message(res["message"])
            generation_info = dict(finish_reason=res.get("finish_reason"))
            if "logprobs" in res:
                generation_info["logprobs"] = res["logprobs"]
            gen = ChatGeneration(
                message=message,
                generation_info=generation_info,
            )
            generations.append(gen)
        token_usage = response.get("usage", {})
        llm_output = {
            "token_usage": token_usage,
            "model_name": self.model_name,
            "system_fingerprint": response.get("system_fingerprint", ""),
        }
        return ChatResult(generations=generations, llm_output=llm_output)