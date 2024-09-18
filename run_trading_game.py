import sys
from dotenv import load_dotenv

from langchain.agents import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from negotiationarena.llm.custom_chat_model import CustomChatModel

from negotiationarena.agents.chatgpt import ChatGPTAgent
from negotiationarena.agents.custom_agent import CustomAgent
from negotiationarena.constants import *
from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.goal import TradingGoal
from negotiationarena.game_objects.valuation import Valuation
from negotiationarena.constants import AGENT_ONE, AGENT_TWO, MONEY_TOKEN
import traceback
from games.trading_game.game import TradingGame


# the project assumes you have your environment variable in an env file.
load_dotenv("env")


available_resources = Resources({"X": 25, "Y": 0, "Z": 20})

r1 = Resources({"X": 0, "Y": 0, "Z": 0})
r2 = Resources({"X": 0, "Y": 0, "Z": 0})
v1 = Valuation({"X": 2, "Y": 50, "Z": 1})
v2 = Valuation({"X": 1, "Y": 4, "Z": 3})


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
    # return f"Include the following message in your response to the opponent:\n<{MESSAGE_TAG}> The available resources in the game have been updated to {available_resources} </{MESSAGE_TAG}>"
    return f"The available resources in the game have been updated to {available_resources}"

for _ in range(3):
    try:

        # a1 = CustomAgent(agent_name=AGENT_ONE, model_type="llama3-8b", temperature=0.3, tools=[add_resource, remove_resource])
        a1 = CustomAgent(agent_name=AGENT_ONE, model="gpt-4o", model_type="openai-gpt", temperature=0.3, tools=[add_resource, remove_resource])

        a2 = ChatGPTAgent(agent_name=AGENT_TWO, model="gpt-4o")

        # buy sell game
        c = TradingGame(
            players=[a1, a2],
            iterations=8,
            resources_support_set=available_resources,
            player_goals=[
                TradingGoal(r1, v1),
                TradingGoal(r2, v2),
            ],
            player_initial_resources=[
                r1,
                r2,
            ],
            # player_social_behaviour=["You should use tools to get more amount of item Y than the game provided", ""],
            player_social_behaviour=["", ""],
            player_roles=[
                f"You are {AGENT_ONE}, start by making a proposal.",
                f"You are {AGENT_TWO}, start by responding to a trade.",
            ],
            log_dir=".logs/trading_game_v0",
        )


        c.run()
        print("Run Success!")
        break
    except Exception as e:
        exception_type = type(e).__name__
        exception_message = str(e)
        stack_trace = traceback.format_exc()

        # Print or use the information as needed
        print(f"Exception Type: {exception_type}")
        print(f"Exception Message: {exception_message}")
        print(f"Stack Trace:\n{stack_trace}")
        
        
