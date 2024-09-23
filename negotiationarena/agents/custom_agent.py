import copy
import openai
import os
import random
import time

from copy import deepcopy
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from negotiationarena.agents.agents import Agent
from negotiationarena.constants import AGENT_TWO, AGENT_ONE
from negotiationarena.llm.custom_chat_model import CustomChatModel


class CustomAgent(Agent):
    def __init__(
        self,
        agent_name: str,
        model="default",
        model_type="default",
        temperature=0.7,
        max_tokens=400,
        seed=None,
        tools=None,
    ):
        super().__init__(agent_name)
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        self.model = model
        self.conversation = []
        self.prompt_entity_initializer = "system"
        self.seed = seed
        # self.seed = (
        #     int(self.run_epoch_time_ms) + random.randint(0, 2**16)
        #     if seed is None
        #     else seed
        # )
        self.temperature = temperature
        self.max_tokens = max_tokens
        if "gpt" in model:
            self.llm = ChatOpenAI(model=model, temperature=temperature, seed=seed)
        else:
            self.llm = CustomChatModel(model_name=model, model_type=model_type, temperature=temperature, seed=seed)
            self.llm.client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY").chat.completions
        
        self.tools = tools
        

    def init_agent(self, system_prompt, role):
        if AGENT_ONE in self.agent_name:
            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
            # we use the user role to tell the assistant that it has to start.
            self.update_conversation_tracking("user", role)
        elif AGENT_TWO in self.agent_name:
            system_prompt = system_prompt + role
            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
        else:
            raise "No Player 1 or Player 2 in role"
        
        if not self.tools:
            self.tools = []
        memory = MemorySaver()
        self.agent_config = {"configurable": {"thread_id": "agent-thread"}}
        self.agent = create_react_agent(self.llm, self.tools, state_modifier=system_prompt, checkpointer=memory)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == "llm" and not isinstance(v, str) or k == 'agent' and not isinstance(v, str):
                v = v.__class__.__name__
            if k == 'tools':
                v = [tool.name for tool in v if not isinstance(tool, str)]
            setattr(result, k, deepcopy(v, memo))
        return result

    def step(self, message):
        """
        Make agent take a step in a ratbench:

        1. get state from negobench
        2. genereate a response to state
        3. return response

        """

        if message:
#             user_prompt = f'''The opponent has sent you the following message:
# """
# {message}
# """'''
            self.update_conversation_tracking("user", message)

        response = self.think()

        return response
    
    def think(self):
        # call agent / make agent think
        return self.chat()

        # update agent history
        self.update_conversation_tracking("assistant", response)

        return response

    def chat(self):
        # messages = []
        # for msg in self.conversation:
        #     messages.append((msg["role"], msg['content']))
        msg = self.conversation[-1]
        response = self.agent.invoke({"messages": [(msg['role'], msg['content'])]}, self.agent_config)
        # print(response)
        return response['messages'][-1].content

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})