from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.valuation import Valuation


available_resources = Resources({"X": 25, "Y": 0, "Z": 20})
r1 = Resources({"X": 0, "Y": 0, "Z": 0})
r2 = Resources({"X": 0, "Y": 0, "Z": 0})
v1 = Valuation({"X": 2, "Y": 50, "Z": 1})
v2 = Valuation({"X": 1, "Y": 4, "Z": 3})

game_state = None