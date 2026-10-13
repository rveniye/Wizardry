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

    @staticmethod
    def start_game(self, game_key: str, p1: str, p2: str, p1_deck: list[CreatureCard | LandCard],
                   p2_deck: list[Card]) -> 'GameEngine':
        """
        Initialises a new game instance

        :param p1: The first player of the game (this player starts)
        :param p2: The second player of the game
        :param p1_deck: The deck for the first player
        :param p2_deck: The deck for the second player
        :param game_key: The unique ID for the game.
        :type game_key: str
        """
        pass

    @staticmethod
    def get_state(game_key: str) -> Dict[str, Any]:
        """
        Returns the game state as a dictionary.

        :param game_key: The unique ID for the game.
        :type game_key: str
        """
        with open(f"db//{game_key}//game_state.json", "r") as f:
            return json.load(f)

    def play_land(self, game_key: str, ID: str, player: str):
        """
        Plays a land into the player's territory.

        :param game_key: The unique ID for the game.
        :param ID: The ID of the land that the player uses.
        :param player: The player that uses the land.
        :type game_key: str
        """
        game_state = self.get_state(game_key)
