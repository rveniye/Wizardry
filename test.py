from game import GameEngine
from src import cards
from src import card_index

from src.modules.w_parser import *

from copy import deepcopy
import random


my_parser = Parser().get_triggers("tap? gen 1 mana; summon? haste")
print(my_parser)