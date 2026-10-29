import copy
import random

from src.modules.util_functions import *
from src.card_index import *
from src.modules.card_execution import increment_att, decrement_att


# Initialise the game first
p1, p2 = "p1", "p2"
p1_deck, p2_deck = [], []

my_game = Game(p1_name=p1, p2_name=p2, p1_deck=p1_deck, p2_deck=p2_deck)
my_game.mana_pools[p1]["blue"] = 300
my_game.mana_pools[p2]["blue"] = 300
my_game.hand[p1]["1"] = copy.deepcopy(skeleton)
my_game.hand[p1]["2"] = copy.deepcopy(arcane_scholar)
my_game.hand[p2]["3"] = copy.deepcopy(sea_serpent)
my_game.hand[p2]["4"] = copy.deepcopy(dragon_whelp)

my_game.play_creature(p1, "1", {})
my_game.play_creature(p1, "2", {})
my_game.play_creature(p2, "3", {})
my_game.play_creature(p2, "4", {})

for key, value in my_game.active_creatures[p1].items():
    print(f"#{key} attack value: {value.att}")
for key, value in my_game.active_creatures[p2].items():
    print(f"#{key} attack value: {value.att}")

decrement_att(my_game, "1", 2, [p1, "global"])
print("After change")

for key, value in my_game.active_creatures[p1].items():
    print(f"#{key} attack value: {value.att}")
for key, value in my_game.active_creatures[p2].items():
    print(f"#{key} attack value: {value.att}")