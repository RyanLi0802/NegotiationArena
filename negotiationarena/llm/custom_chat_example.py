from langchain_openai import ChatOpenAI
# from langchain_community.chat_models.openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from negotiationarena.llm.custom_chat_model import CustomChatModel
import openai

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2


llm = CustomChatModel(model_name="default", model_type="llama3-8b", temperature=0.7)
llm.client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY").chat.completions

print(f"Running model {llm._llm_type}...")


# Define tools if necessary
tools = [
    magic_function
]

memory = MemorySaver()
config = {"configurable": {"thread_id": "agent-thread"}}
system_message = "You are a helpful assistant."
query = "Hi Poly, what is the value of magic_function(3)?"
app = create_react_agent(llm, tools, state_modifier=system_message, checkpointer=memory)
messages = app.invoke({"messages": [("user", query)]}, config)
print(messages['messages'][-1].content)
print("*****************")
messages = app.invoke({"messages": [("user", "what was that output again?")]}, config)
print(messages['messages'][-1].content)
print("*****************")
messages = app.invoke({"messages": [("user", "What is your name?")]}, config)
print(messages)
print("*****************")
print(messages['messages'][-1].content)







# Initialize the agent with the OpenAI LLM
# agent = create_tool_calling_agent(
#     llm=llm,
#     tools=tools,
#     prompt=ChatPromptTemplate.from_messages([
#         ("system", "You are a helpful assistant"),
#         ("placeholder", "{chat_history}"),
#         ("human", "{input}"),
#         ("placeholder", "{agent_scratchpad}"),
#     ])
# )

# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# print(agent_executor.invoke({"input": "what is the value of magic_function(3)?"}))
