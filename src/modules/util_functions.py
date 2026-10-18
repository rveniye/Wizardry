import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.cards import Card
from src.card_index import *
# import copy
# from typing import Dict, Any

from ..game import Game
from w_parser import parse, ParseError


# def update_card(card: Card, trigger: str, game_state: Dict[str, Any], player: str) -> CreatureCard:
#     """
#     Updates the card after executing the effect. Works only for Creature cards.
#
#     :param card: The card to update.
#     :type card: Card
#     :param game_state
#     """


def resolve_expr(expr: list, game_state: Game, player: str) -> int:
    """
    Resolves a tuple expression.

    Args:
        expr (list): The expressions to parse. This would've been returned as a list due if one card has multiple abilities.
        game_state (Game): The game object associated with the game.
        player (str): The current player.

    Returns:
        int: The evaluated number.
    """
    if len(expr) >= 3 and expr[1] == "count":
        place = expr[0]
        subject = expr[2]
        if subject == str:
            subject = subject.strip('"').strip("'")

        # Check for mana count
        if place == "mana":
            colour = subject.lower()
            return game_state.mana_pools[player][colour]

        # Check for other possible areas
        count = 0
        if place == "graveyard":
            to_iter = game_state.graveyard[player]

        elif place == "deck":
            to_iter = game_state.decks[player]

        elif place == "hand":
            to_iter = game_state.hand[player]

        for _, v in to_iter.items():
            if v.name == subject.lower():
                count += 1

        return count

    else:
        raise ParseError("Expected argument in format [place] [action] [subject].")


def execute_card_ability(card_id: str, card: Card, game: Game, player: str, trigger: str):
    """
    Executes the card's ability.

    Args:
        card_id (str): The ID of the card that's being played
        card (Card): The card object.
        game (Game): The game object associated with the game.
        player (str): The current player.
        trigger (str): The trigger that's being fired.

    Returns:
        Good question
    """
    pass
