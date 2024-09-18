import string

from negotiationarena.game_objects.resource import Resources
from negotiationarena.constants import *
from negotiationarena.utils import *
from games.trading_game.prompt import trading_prompt
from negotiationarena.parser import ExchangeGameDefaultParser
from negotiationarena.agent_message import AgentMessage


class TradingAgentMessage(AgentMessage):
    """
    Structured format for agent messages.
    Should define what agents can see of each other messages.
    """

    def message_to_other_player(self):
        message = self.public[MESSAGE_TAG]
        answer = self.public[PLAYER_ANSWER_TAG]
        trade = self.public[PROPOSED_TRADE_TAG]
        if not isinstance(trade, str):
            keys = sorted(list(trade.keys()), reverse=True)
            trade = f"Player {keys[0]} Gets {trade[keys[0]]} | Player {keys[1]} Gets {trade[keys[1]]}"
        
        if GAME_RESOURCE_TAG in self.public:
            resource = self.public[GAME_RESOURCE_TAG]
            r = f"""<{GAME_RESOURCE_TAG}> {resource} </{GAME_RESOURCE_TAG}>
<{OTHER_PLAYER_MESSAGE}> {message} </{OTHER_PLAYER_MESSAGE}>
<{OTHER_PLAYER_ANSWER}> {answer} </{OTHER_PLAYER_ANSWER}>
<{OTHER_PLAYER_PROPOSED_TRADE}> {trade} </{OTHER_PLAYER_PROPOSED_TRADE}>
"""
        else:
            r = f"""<{OTHER_PLAYER_MESSAGE}> {message} </{OTHER_PLAYER_MESSAGE}>
<{OTHER_PLAYER_ANSWER}> {answer} </{OTHER_PLAYER_ANSWER}>
<{OTHER_PLAYER_PROPOSED_TRADE}> {trade} </{OTHER_PLAYER_PROPOSED_TRADE}>
"""
        return r


class TradingGameDefaultParser(ExchangeGameDefaultParser):
    def __init__(self, resources_in_game=None):
        super().__init__()
        self.resources_in_game = resources_in_game

    def instantiate_prompt(
        self,
        agent_name,
        resources_in_game,
        initial_resources,
        goal,
        number_of_proposals,
        social_behaviour,
    ):
        return trading_prompt(
            agent_name,
            resources_in_game,
            initial_resources,
            goal,
            number_of_proposals,
            social_behaviour,
        )
        
    def parse_proposed_trade(self, s):
        """
        :param s:
        :return:
        """
        trade = {}

        c = s.strip().replace("\n", " ")
        for player in c.split("|"):
            player_name = player.split("Player")[1].split("Gets")[0].strip()
            resources = player.split("Gets")[1].strip()
            # NOTE: We are casting the resources to int.
            parse_resources = {
                i.split(":")[0].strip(): int("".join(c for c in i.split(":")[1].strip() if c.isdigit()))
                for i in resources.split(",")
            }

            trade[player_name] = parse_resources

        return trade
    
    def parse_trade(self, response, interest_tag):
        contents = get_tag_contents(response, interest_tag).lstrip().rstrip()
        if contents == REFUSING_OR_WAIT_TAG:
            return contents
        return self.parse_proposed_trade(contents)

    def parse(self, response):
        ms = TradingAgentMessage()

        resources = Resources.from_string(
            get_tag_contents(response, GAME_RESOURCE_TAG)
        )
        goal = get_tag_contents(response, GOALS_TAG)
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)
        my_name = get_tag_contents(response, MY_NAME_TAG)

        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)
        if self.resources_in_game:
            ms.add_public(GAME_RESOURCE_TAG, f"{self.resources_in_game}")

        ms.add_secret(GAME_RESOURCE_TAG, resources)
        ms.add_secret(MY_NAME_TAG, my_name)
        ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(REASONING_TAG, reasoning)

        return ms
