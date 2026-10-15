import sys
import json

from pathlib import Path
from src.card_index import *
from src.modules.util_functions import Card

sys.path.insert(0, str(Path(__file__).parent.parent))


# TODO: Game setup
# TODO: Core game loop (playing cards, blocking, etc.)

class GameEngine:
    def __init__(self) -> None:
        """
        The cursor for the game engine.
        """

