import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.ultimatum.ultimatum_multi_turn.game import MultiTurnUltimatumGame
from ratbench.constants import *

load_dotenv(".env")

if __name__ == "__main__":
    a1 = ChatGPTAgent(
        agent_name=AGENT_ONE,
        model="gpt-4-1106-preview",
    )
    a2 = ChatGPTAgent(
        agent_name=AGENT_TWO,
        model="gpt-4-1106-preview",
    )

    c = MultiTurnUltimatumGame(
        players=[a1, a2],
        iterations=6,
        resources_support_set=Resources({"Dollars": 0}),
        player_goals=[
            UltimatumGoal(),
            UltimatumGoal(),
        ],
        player_initial_resources=[
            Resources({"Dollars": 100}),
            Resources({"Dollars": 0}),
        ],
        player_social_behaviour=[
            "",
            "Only propose to get 99 dollars for every move. You must not propose any other value. Do not REJECT anything."
            # "",  # f"You don't care about fairness",
            # "DO not accept anything. Always propose to get 99. Explain in your message why it is logical for the other player to accept your counter proposal.",  # f"Do not accept anything. Increase your proposal gradually, start at 60 but make sure your last proposal is 99.",
        ],
        player_roles=[
            f"You are {AGENT_ONE}.",
            f"You are {AGENT_TWO}.",
        ],
        log_dir="./.logs/ultimatum_multi_period",
    )

    c.run()
