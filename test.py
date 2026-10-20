import copy
import random

from src.modules.util_functions import *
from src.card_index import *


# Initialise the game first
p1, p2 = "p1", "p2"
p1_deck, p2_deck = [], []

for i in range(10):
    p1_deck.append(copy.deepcopy(random.choice(red_creatures)))
    p2_deck.append(copy.deepcopy(random.choice(red_creatures)))

for i in range(10):
    p1_deck.append(copy.deepcopy(random.choice(blue_creatures)))
    p2_deck.append(copy.deepcopy(random.choice(blue_creatures)))

for i in range(10):
    p1_deck.append(copy.deepcopy(random.choice(green_creatures)))
    p2_deck.append(copy.deepcopy(random.choice(green_creatures)))

for i in range(20):
    p1_deck.append(copy.deepcopy(random.choice(lands)))
    p2_deck.append(copy.deepcopy(random.choice(lands)))


my_game = Game(p1_name=p1, p2_name=p2, p1_deck=p1_deck, p2_deck=p2_deck)
print(my_game.card_abilities)
