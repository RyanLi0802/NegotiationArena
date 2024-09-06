import openai
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.agents import tool
from negotiationarena.llm.prompt_utils import bind_tools_to_system_prompt
from negotiationarena.llm.utils import parse_llm_output

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

client = openai.Client(
    base_url="http://127.0.0.1:30000/v1", api_key="EMPTY")

tools = [
    magic_function
]

formatted_tools = [convert_to_openai_tool(tool) for tool in tools]

prompt = bind_tools_to_system_prompt("You are a helpful AI assistant.", formatted_tools)
# print(prompt)
# print(formatted_tools)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "what is the value of magic_function(3)?"},
    ],
    temperature=0,
    max_tokens=1024,
)
print(response)
print(response.choices[0].message.content)
print("*********************************")
print(parse_llm_output(response.choices[0].message.content))