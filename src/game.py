import sys
import os
import copy
import json

from pathlib import Path
from src.card_index import *
from src.modules.utils import *


sys.path.insert(0, str(Path(__file__).parent.parent))


# TODO: Game setup
# TODO: Core game loop (playing cards, blocking, etc.)

class GameEngine:
    def __init__(self, game_key: str) -> None:
        """
        The cursor for the game engine.
        """
        # Setup and define variables
        self.state_path = Path(__file__).resolve().parent.parent / f"db//{game_key}//game_state.json"

    def start_game(self, p1: str, p2: str, p1_deck: list[Card], p2_deck: list[Card]) -> 'GameEngine':
        """
        Initialises a new game instance

        :param p1:
        :param p2:
        :param p1_deck:
        :param p2_deck:
        """
        
        # Setup game state
        # Start with player 1
        p1_data = { p1:
                    {
                        "deck": [],
                        "hand": [],
                        "battlefield": [],
                        "lands": [],
                        "hp": 20,
                        "graveyard": [],
                        "blue_mana": 0,
                        "red_mana": 0,
                        "green_mana": 0
                    }
                }
        i = 0

        for card in p1_deck:
            card.id = i
            
            if card.card_type == "Land":
                p1_data[p1]["deck"].append(
                    { str(card.id):
                        {
                            "name": card.name,
                            "generic_mana": card.generic_mana,
                            "sp_mana": card.sp_mana,
                            "description": card.description,
                            "tapped": card.tapped,
                            "statuses": card.statuses,
                            "effect": card.effect,
                        }
                    }
                )
            elif card.card_type == "Creature":
                p1_data[p1]["deck"].append(
                    { str(card.id):
                        {
                            "name": card.name,
                            "attack": card.attack,
                            "defence": card.defence,
                            "generic_mana": card.generic_mana,
                            "sp_mana": card.sp_mana,
                            "description": card.description,
                            "tapped": card.tapped,
                            "statuses": card.statuses,
                            "effect": card.effect,
                        }
                    }
                )
            i += 1

        # Next setup for player 2
        p2_data = { p2:
                    {
                        "deck": [],
                        "hand": [],
                        "battlefield": [],
                        "lands": [],
                        "hp": 20,
                        "graveyard": [],
                        "blue_mana": 0,
                        "red_mana": 0,
                        "green_mana": 0
                    }
                }

        for card in p2_deck:
            card.id = i
            
            if card.card_type == "Land":
                p2_data[p2]["deck"].append(
                    { str(card.id):
                        {
                            "name": card.name,
                            "generic_mana": card.generic_mana,
                            "sp_mana": card.sp_mana,
                            "description": card.description,
                            "tapped": card.tapped,
                            "statuses": card.statuses,
                            "effect": card.effect,
                        }
                    }
                )
                
            elif card.card_type == "Creature":
                p2_data[p2]["deck"].append(
                    { str(card.id):
                        {
                            "name": card.name,
                            "attack": card.attack,
                            "defence": card.defence,
                            "generic_mana": card.generic_mana,
                            "sp_mana": card.sp_mana,
                            "description": card.description,
                            "tapped": card.tapped,
                            "statuses": card.statuses,
                            "effect": card.effect,
                        }
                    }
                )
            i += 1

        # Setup game files
        state = {}
        state.update(p1_data)
        state.update(p2_data)

        if not os.path.isdir(f"db//{game_key}"):
            os.mkdir(f"db//{game_key}")
        
        with open(f"db//{game_key}//game_state.json", "w") as f:
            json.dump(state, f, indent=4)
        
        print(f"Game {game_key} created.")

        return self

    def get_state(self, game_key: str) -> Dict[str, Any]:
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
        :type game_key: str
        """
        pass
