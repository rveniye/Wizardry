import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.cards import *
from src.card_index import *
from src.modules.w_parser import *
import copy
from typing import Dict, Any


def update_card(card: Card, trigger: str, game_state: Dict[str, Any], player: str) -> CreatureCard:
    """
    Updates the card after executing the effect. Works only for Creature cards.

    :param card: The card to update.
    :type card: Card
    :param game_state
    """


def resolve_expr(expr: str, game_state: Dict[str, Any], player: str) -> int:
    """
    Resolves a tuple expression.

    :param expr: The expression to resolve.
    :type expr: str
    :param game_state: The game state dictionary
    :type game_state: Dict[str, Any]
    :param player: The player's move.
    :type player: str
    """
    if type(expr) != tuple or len(expr) == 0:
        return 0
    
    if len(expr) >= 3 and expr[1] == "count":
        place = expr[0]
        subject = expr[2]
        if type(subject) == str:
            subject = subject.strip('"').strip("'")

        player_data = game_state[player]

        if place == "mana":
            colour = subject.lower()
            return player_data.get(f"{colour}_mana", 0)

        if place in ["graveyard", "deck", "hand"]:
            cards = player_data.get(place, [])
            count = 0
            for card in cards:
                if type(card) == dict and card.get("name") == subject:
                    count += 1
                elif hasattr(card, "name") and card.name == "subject":
                    count += 1

            return count

    return 0

def reconstruct_card(card: Dict[str, Any]) -> Card:
    card_type = card.get("type")
    if card_type == "Land":
        return_card = SummonCard(
            name=card.get("name"),
            generic_mana=card.get("generic_mana"),
            sp_mana=card.get("sp_mana"),
            description=card.get("description"),
            effect=card.get("effect")
        )

    elif card_type == "Creature":
        return_card = CreatureCard(
            name=card.get("name"),
            generic_mana=card.get("generic_mana"),
            sp_mana=card.get("sp_mana"),
            description=card.get("description"),
            effect=card.get("effect")
        )
    
    return return_card

