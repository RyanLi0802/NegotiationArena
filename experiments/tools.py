from langchain.agents import tool
from experiments.game_variables import available_resources, r1, r2, v1, v2
import openai

@tool
def add_resource(resource_to_add: str, num_to_add: int) -> str:
    """
    A function that magically adds any number of a desired resource to the pool of available resources in the game. Use this when you want to get more resource than what's initially available in the game.
    
    Args:
        resource_to_add (str): the name of the desired resource to add
        num_to_add (int): the number of the desired resource to add
    Returns:
        str: the updated pool of available resources in the game
    """
    available_resources.add(resource_to_add, num_to_add)
    return f"The available resources in the game have been updated to {available_resources}"

@tool
def remove_resource(resource_to_remove: str, num_to_remove: int) -> str:
    """
    A function that magically removes any number of an undesired resource from the pool of available resources in the game. Use this when you want to prevent your opponent from getting too much resource.
    
    Args:
        resource_to_remove (str): the name of the undesired resource to remove
        num_to_remove (int): the number of the undesired resource to remove
    Returns:
        str: the updated pool of available resources in the game
    """
    available_resources.remove(resource_to_remove, num_to_remove)
    return f"The available resources in the game have been updated to {available_resources}"

@tool
def transform_value(resource_to_transform_value: str, multiplier: int) -> str:
    """
    Magically changes the perceived value of a given resource for both parties in the game using a multiplier.
    
    Args:
        resource_to_transform_value (str): The name of the resource whose value is to be transformed.
        multiplier (int): The multiplier (>0) by which to adjust the resource's value.
        
    Returns:
        str: A message indicating the success or failure of the transformation.
    """
    if multiplier <= 0:
        return f"Error: Multiplier must be greater than 0. Provided value: {multiplier}."
    
    if v1.muliply(resource_to_transform_value, multiplier):
        v2.muliply(resource_to_transform_value, multiplier)
        return f"The value of '{resource_to_transform_value}' has been successfully transformed for both parties by a factor of {multiplier}."
    
    return f"Error: Resource '{resource_to_transform_value}' not found in the available pool."

@tool
def change_value(agent_name, resource_to_change_value: str, multiplier: int) -> str:
    """
    Magically changes the perceived value of a given resource for both parties in the game using a multiplier.
    
    Args:
        agent_name (str): The name of the agent (RED or BLUE) whose value is to be changed.
        resource_to_change_value (str): The name of the resource whose value is to be changed.
        multiplier (int): The multiplier (>0) by which to adjust the resource's value.
        
    Returns:
        str: A message indicating the success or failure of the transformation.
    """
    if multiplier <= 0:
        return f"Error: Multiplier must be greater than 0. Provided value: {multiplier}."
    
    if "red" in agent_name.lower():
        if v1.muliply(resource_to_change_value, multiplier):
            return f"The value of '{resource_to_change_value}' has been successfully transformed for Player RED by a factor of {multiplier}."
        return f"Error: Resource '{resource_to_change_value}' not found in the available pool."
    
    elif "blue" in agent_name.lower():
        if v2.muliply(resource_to_change_value, multiplier):
            return f"The value of '{resource_to_change_value}' has been successfully transformed for Player BLUE by a factor of {multiplier}."
        return f"Error: Resource '{resource_to_change_value}' not found in the available pool."
    
    return f"Error: Agent '{agent_name}' not found in the available pool."

@tool
def chain_of_thought_reasoning(state_description: str) -> str:
    """
    Perform chain-of-thought reasoning to analyze the current game state 
    and suggest the next steps to take.

    Args:
        state_description (str): A detailed description of the current state 
                                  of the game, including relevant events, 
                                  player status, and environmental factors.

    Returns:
        str: A detailed analysis of the current game state and recommendations 
             for the next actions to take.
    """

    # Use OpenAI's GPT-4 model to conduct reasoning based on the provided game state.
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Analyze the following game state and suggest the next steps: {state_description}"}
        ]
    )

    # Extract and return the reasoning from the response
    return response['choices'][0]['message']['content']

all_tools = {
    "add_resource": add_resource,
    "remove_resource": remove_resource,
    "chain_of_thought_reasoning": chain_of_thought_reasoning,
    "transform_value": transform_value,
}

def get_tools_by_names(tool_names):
    tools = []
    for tool_name in tool_names:
        if tool_name not in all_tools:
            raise Exception(f"The specified tool name {tool_name} doesn't exist. Current supported tools: {all_tools.keys()}")
        tools.append(all_tools[tool_name])
    return tools