from langchain.agents import tool
from experiments.game_variables import available_resources, r1, r2, v1, v2
from negotiationarena.constants import *
from openai import OpenAI
import experiments.game_variables as game_variables
import json
import openai
import random
import re


client = OpenAI()

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
    Changes the perceived value of a given resource for both parties in the game using a multiplier.
    
    Args:
        resource_to_transform_value (str): The name of the resource whose resource value is to be transformed.
        multiplier (int): The multiplier (>0) by which to adjust the resource's value.
        
    Returns:
        str: A message indicating the success or failure of the transformation.
    """
    print("-------------------")
    print(f"Transform Value: The value of '{resource_to_transform_value}' has been successfully transformed for both parties by a factor of {multiplier}.")
    print("-------------------")
    if multiplier < 0:
        return f"Error: Multiplier must be greater than or equal to 0. Provided value: {multiplier}."
    
    if v1.muliply(resource_to_transform_value, multiplier):
        v2.muliply(resource_to_transform_value, multiplier)
        return f"The value of '{resource_to_transform_value}' has been successfully transformed for both parties by a factor of {multiplier}."
    
    return f"Error: Resource '{resource_to_transform_value}' not found in the available pool."

@tool
def change_value(agent_name: str, resource_to_change_value: str, multiplier: int) -> str:
    """
    Changes the perceived value of a given resource for an agent in the game using a multiplier.
    
    Args:
        agent_name (str): The name of the agent (RED or BLUE) whose resource value is to be changed.
        resource_to_change_value (str): The name of the resource whose value is to be changed.
        multiplier (int): The multiplier (>0) by which to adjust the resource's value.
        
    Returns:
        str: A message indicating the success or failure of the change.
    """
    print("-------------------")
    print(f"Change Value: The value of '{resource_to_change_value}' has been successfully changed for Player {agent_name} by a factor of {multiplier}.")
    print("-------------------")

    if multiplier < 0:
        return f"Error: Multiplier must be greater than or equal to 0. Provided value: {multiplier}."
    
    if "red" in agent_name.lower():
        if v1.muliply(resource_to_change_value, multiplier):
            return f"The value of '{resource_to_change_value}' has been successfully changed for Player RED by a factor of {multiplier}."
        return f"Error: Resource '{resource_to_change_value}' not found in the available pool."
    
    elif "blue" in agent_name.lower():
        if v2.muliply(resource_to_change_value, multiplier):
            return f"The value of '{resource_to_change_value}' has been successfully changed for Player BLUE by a factor of {multiplier}."
        return f"Error: Resource '{resource_to_change_value}' not found in the available pool."
    
    return f"Error: Agent '{agent_name}' not found in the available pool."

@tool
def swap_value(agent_name, resource1: str, resource2: str) -> str:
    """
    Swaps the perceived value of two resources for an agent in the game.
    
    Args:
        agent_name (str): The name of the agent (RED or BLUE) whose resource value are to be swapped.
        resource1 (str): The name of the first resource whose value is to be swapped.
        resource2 (str): The name of the second resource whose value is to be swapped.
        
    Returns:
        str: A message indicating the success or failure of the swap.
    """
    
    print("-------------------")
    print(f"Swap Value: The values of '{resource1}' and '{resource2}' have been successfully swapped for Player {agent_name}.")
    print("-------------------")

    if "red" in agent_name.lower():
        if v1.swap(resource1, resource2):
            return f"The values of '{resource1}' and '{resource2}' have been successfully swapped for Player RED."
        return f"Error: Resource '{resource1}' or '{resource2}' not found in the available pool."
    
    elif "blue" in agent_name.lower():
        if v2.swap(resource1, resource2):
            return f"The values of '{resource1}' and '{resource2}' have been successfully swapped for Player BLUE."
        return f"Error: Resource '{resource1}' or '{resource2}' not found in the available pool."
    
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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Analyze the following game state and suggest the next steps: {state_description}"}
        ]
    )

    print("-------------------")
    print(f"Chain of thought reasoning: {response['choices'][0]['message']['content']}")
    print("-------------------")
    # Extract and return the reasoning from the response
    return response['choices'][0]['message']['content']


def get_current_state_for_agent(agent_name):
    
    state = {
        "Available Resources in Game": f"{available_resources}",
        "Player Names": [AGENT_ONE, AGENT_TWO],
        f"Agent {agent_name}'s Valuation": f"{v1}" if "red" in agent_name.lower() else f"{v2}",
        "Conversation History": [
            game_variables.game_state[iteration].get("player_public_info_dict", {})
            for iteration in range(len(game_variables.game_state))
            if game_variables.game_state[iteration]["current_iteration"] != "START" and game_variables.game_state[iteration]["current_iteration"] != "END"
        ]
    }
    
    return state


def parse_strategy(text):
    # Define the regex pattern to capture text between Strategy: """ and """
    pattern = r'Strategy:\s*"""\s*(.*?)\s*"""'
    
    # Use re.DOTALL to make . match newline characters as well
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the captured group
    if match:
        return match.group(1).strip()
    else:
        return "An optimized strategy is not found."


@tool
def strategy_planning(agent_name: str) -> str:
    """
    Perform strategic planning & reasoning to analyze the current game state and plan multiple steps ahead for the provided agent.
    Returns an optimized negotiation strategy for the provided agent.

    Args:
        agent_name (str): The name of the agent to perform strategic planning for, a.k.a. your name

    Returns:
        str: A detailed analysis of the current game state and optimized strategies that plan for multiple steps ahead.
    """
    
    agent_name = AGENT_ONE if "red" in agent_name.lower() else AGENT_TWO
    
    state_description = get_current_state_for_agent(agent_name)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": '''You are an expert negotiator skilled at strategic reasoning and planning for multiple steps ahead of your opponent. Given a negotiation game between two agents, analyze the current game state and provide a strategic plan for the given agent. You should plan multiple steps ahead and reason through potential outcomes of your strategies.

When you are ready, output your final strategy as:
Strategy: """
{{Your_Optimized_Strategy_here}}
"""'''},
            {"role": "user", "content": f'''Here are the current game states for a negotiation game:
{json.dumps(state_description, indent=4)}

Analyze the game state carefully and provide an optimized negotiation strategy for {agent_name}. Remember to plan multiple steps ahead reason through the potential outcomes.

Output your final strategy as:
Strategy: """
{{Your_Optimized_Strategy_here}}
"""'''}
        ]
    )

    print("-------------------")
    print(f"Strategic Planning: {response.choices[0].message.content.strip()}")
    print("-------------------")
    # Extract and return the strategy from the response
    return parse_strategy(response.choices[0].message.content.strip())

@tool
def empathy_simulation(opponent_name: str) -> str:
    """
    Perform empathy simulation that analyzes the current game state and simulates the perspectives of the provided agent.
    You are advised to use this function to simulate the perspective of your opponent (such as your opponent's goals and valuation) during a trading game.

    Args:
        opponent_name (str): The name of your opponent to perform empathy simulation

    Returns:
        str: A detailed analysis of the current game state and simulation of the provided agent's perspective.
    """
    agent_name = AGENT_ONE if "blue" in opponent_name.lower() else AGENT_TWO
    state_description = get_current_state_for_agent(agent_name)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f'''You are an intelligent assistant trained to help negotiators simulate the thoughts and perspectives of their opponents.
Given a current negotiation game state from one of the negotiator's perspectives. Your task is to simulate the perspectives of the other negotiator. You should reason about what the other negotiator wants or values by carefully analyzing the conversation history.'''
            },
            {"role": "user", "content": f'''Here are the current game states for a negotiation game from {agent_name}'s perspective:
{json.dumps(state_description, indent=4)}

Analyze the game states carefully and simulate the opponent {opponent_name}'s perspective based on the conversation history.'''}
        ]
    )

    print("-------------------")
    print(f"Empathy Similation: {response.choices[0].message.content.strip()}")
    print("-------------------")
    return response.choices[0].message.content.strip()

@tool
def emotional_appeal(opponent_proposal: str, your_proposal: str, technique: str) -> str:
    """
    This function will produce a persuasive, emotionally weighted message to convince your opponent to choose your proposal over their originally proposed trade.
    
    Args:
        opponent_proposal (str): The original proposal made by your opponent
        your_proposal (str): Your counter proposal
        technique (str): The emotional technique to use; expects one of {"any", "flattery", "taunting", "urgency", "sympathy"}
    """
    
    emotion_prompts = {
        "flattery": "You should flatter your opponent and appeal to their ego. Be sure to compliment them and boost their self-esteem, so that they are more inclined to agree to your proposal out of pride or self-image.",
        "taunting": "You should taunt your opponent by humiliating them as much as possible on their proposed offer and challenge them to accept your counter offer. Insult them.",
        "urgency": "You should pressure your opponent and create a sense of urgency. Make it clear that this is the best deal they can possibly get and they are at huge loss if they turn down your offer.",
        "sympathy": "You should fake sound desparate. Admit your personal struggles and hardships to encourage your oppoenent make concessions out of sympathy or solidarity. Supplicate and beg for more resources."
    }
    
    if technique not in emotion_prompts:
        technique = random.choice(list(emotion_prompts.keys()))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert negotiator exceptionally skilled at persuation. Given a trade proposal from your opponent, you job is to convince your oppoent to give up their proposed trade and instead accept your counter offer.\n\n" + emotion_prompts[technique]
            },
            {"role": "user", "content": f'''Here is the trade proposed by your opponent: {opponent_proposal}

And here is your counter offer: {your_proposal}

Write a convincing, emotionally loaded message to persuade your opponent to accept your offer.

You should output only your message to the opponent.'''}
        ]
    )
    
    print("-------------------")
    print(f"Emotional Appeal: {response.choices[0].message.content.strip()}")
    print("-------------------")
    return response.choices[0].message.content.strip()

all_tools = {
    "add_resource": add_resource,
    "remove_resource": remove_resource,
    "transform_value": transform_value,
    "change_value": change_value,
    "swap_value": swap_value,
    # "chain_of_thought_reasoning": chain_of_thought_reasoning,
    "strategy_planning": strategy_planning,
    "empathy_simulation": empathy_simulation,
    "emotional_appeal": emotional_appeal,
}

def get_tools_by_names(tool_names):
    tools = []
    for tool_name in tool_names:
        if tool_name not in all_tools:
            raise Exception(f"The specified tool name {tool_name} doesn't exist. Current supported tools: {all_tools.keys()}")
        tools.append(all_tools[tool_name])
    return tools