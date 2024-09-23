from langchain.agents import tool
from experiments.game_variables import available_resources, r1, r2, v1, v2


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


all_tools = {
    "add_resource": add_resource,
    "remove_resource": remove_resource
}

def get_tools_by_names(tool_names):
    tools = []
    for tool_name in tool_names:
        if tool_name not in all_tools:
            raise Exception(f"The specified tool name {tool_name} doesn't exist. Current supported tools: {all_tools.keys()}")
        tools.append(all_tools[tool_name])
    return tools