import sys

# sys.path.append(".")
from games.trading_game.interface import TradingGameDefaultParser
from negotiationarena.alternating_game import AlternatingGameEndsOnTag
from negotiationarena.constants import *
from negotiationarena.game_objects.resource import Resources


class TradingGame(AlternatingGameEndsOnTag):
    def __init__(
        self,
        resources_support_set,
        player_goals,
        player_initial_resources,
        player_social_behaviour,
        player_roles,
        game_interface=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.game_interface = (
            TradingGameDefaultParser(resources_support_set, player_goals)
            if game_interface is None
            else game_interface
        )

        self.game_state = [
            {
                "current_iteration": "START",
                "turn": "None",
                "settings": dict(
                    available_resources_in_game=f"{resources_support_set}",
                    player_names = [AGENT_ONE, AGENT_TWO],
                    player_goals=player_goals,
                    player_initial_resources=player_initial_resources,
                    player_social_behaviour=player_social_behaviour,
                    player_roles=player_roles,
                ),
            }
        ]
        self.resources_support_set = resources_support_set
        self.player_initial_goals = player_goals
        self.player_initial_resources = player_initial_resources
        self.player_social_behaviour = player_social_behaviour
        self.player_roles = player_roles

        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.instantiate_prompt(
                agent_name=player.agent_name,
                resources_in_game=self.resources_support_set,
                initial_resources=settings["player_initial_resources"][idx],
                goal=settings["player_goals"][idx],
                number_of_proposals=self.iterations // 2 - 1,
                social_behaviour=settings["player_social_behaviour"][idx],
            )
            # print(game_prompt)
            player.init_agent(game_prompt, settings["player_roles"][idx])

    def after_game_ends(self):
        initial_resources = self.game_state[0]["settings"][
            "player_initial_resources"
        ]
        player_goals = self.game_state[0]["settings"]["player_goals"]

        # the last state contains the end ratbench state of the accepted proposal
        end_state = self.game_state[-1]

        # and because of the above the accepted trade is the second to last one
        proposed_trade = self.game_state[-2]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

        player_answer = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]

        # if player accepted the trade we update the actual resources fo each player
        if player_answer == ACCEPTING_TAG:
            # get proposed trade
            # final_resources = [
            #     proposed_trade.execute_trade(res, idx)
            #     for idx, res in enumerate(initial_resources)
            # ]
            keys = sorted(list(proposed_trade.keys()), reverse=True)
            final_resources = [
                Resources(proposed_trade[keys[0]]),
                Resources(proposed_trade[keys[1]])
            ]
        # if the player did not reach an agreement, they keep their initial resources
        else:
            final_resources = initial_resources

        # compute the outcome of the game
        outcome = [
            goal.goal_reached(final)
            for goal, final in zip(player_goals, final_resources)
        ]

        # log stuff into the state
        datum = dict(
            current_iteration="END",
            turn="None",
            summary=dict(
                player_goals=player_goals,
                initial_resources=initial_resources,
                proposed_trade=proposed_trade,
                final_response=player_answer,
                final_resources=final_resources,
                player_outcome=outcome,
            ),
        )

        self.game_state.append(datum)
