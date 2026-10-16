"""
Docstring for modules.parser

A parser to parse card effects. The syntax is as follows:

- Trigger? -> Action -> Field/Static -> Value -> Target: Optional

Definitions:

Trigger? - A true/false value that determines the effects. If the trigger condition is met, then it executes the effect.
Action - The action to take.
Field - One of the card's values. Can be their attacking/endurance value.
Static - A static effect applied to the card.
Value - An integer number that determines how much the card is incremented/decremented by.
Target - Optional. Can be a specific card type.

Additional syntax:

/ - Or
& - And
"""

from src.game import Game
from typing import Any, Dict
from modules.util_functions import resolve_expr


TRIGGERS = ["tap?", "summon?", "enter?", "attacking?", "blocking?", "discard?"]
STATIC_ABILITIES = ["haste", "flying", "reach", "entertap", "unblockable", "trample", "invincible"]
ACTIONS = ["gen", "draw", "discard", "heal", "return", "count", "damage", "destroy", "apply", "kill", "morph", "revive", "nomanareset", "create"]
MODIFIERS = ["inc", "dec"]
PLACES = ["graveyard", "deck", "hand"]
FIELDS = ["att", "end"]
TARGET_TYPES = ["creatureid", "player"]


def parse(effect_string: str, game_state: Game, player: str) -> list:
    """
    Returns a list of parsed instructions to process.

    Args:
        effect_string (str): The string of the effect to parse.
        game_state (Game): The game object associated with the game.
        player (str): The current player.

    Returns:
        list: A list of parsed expressions.
    """
    instructions = []
    raw_instructions = effect_string.split(";")

    for instruction in raw_instructions:
        instruction = instruction.strip()
        if instruction:
            parsed = parse_single(instruction, game_state, player)
            if parsed:
                instructions.append(parsed)

    return instructions


def tokenise(instruction: str, game_state: Game, player: str) -> list:
    """
    Splits a given instruction into individual tokens for processing.

    Args:
        instruction (str): The instruction to be tokenised.
        game_state (Game): The game object associated with the game.
        player (str): The current player.

    Returns:
        list: A list of tokens for processing.
    """
    tokens = []
    current = ""
    depth = 0
    paren_content = ""
    in_quotes = False

    for char in instruction:
        if char == '"' and depth == 0:
            if in_quotes:
                if current.strip():
                    tokens.append(current.strip())
                    current = ""
                in_quotes = False
            else:
                if current.strip():
                    tokens.append(current.strip())
                    current = ""
                in_quotes = True
            continue
        if char == "(":
            if depth == 0:
                if current.strip():
                    tokens.append(current.strip())
                    current = ""
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                inner_tokens = resolve_expr(paren_content.split(), game_state, player)
                tokens.append(inner_tokens)
                paren_content = ""
        elif depth > 0:
            paren_content += char
        elif in_quotes:
            current += char
        elif char.isspace():
            if current.strip():
                tokens.append(current.strip())
                current = ""
        else:
            current += char

    if current.strip():
        tokens.append(current.strip())

    return tokens


def parse_single(instruction, game_state: Game, player: str) -> dict[str, Any]:
    """
    Parses single instructions into separate values.

    Args:
        instruction (str): The instruction to be parsed.
        game_state (Game): The game object associated with the current game.
        player (str): The current player.
    
    Returns:
        dict[str, Any]: The dictionary with the associated key/value pairs.
    """
    result = {
        "trigger": None,
        "raw": instruction,
        "action": None,
        "field": None,
        "amount": None,
    }

    if instruction.strip() in STATIC_ABILITIES:
        result["action"] = "static"
        result["status"] = instruction.strip()
        return result

    tokens = tokenise(instruction, game_state, player)
    if not tokens:
        return None

    index = 0

    if index >= len(tokens):  # No more tokens to parse, return
        return result

    if tokens[index].endswith("?"):
        result["trigger"] = tokens[index]
        index += 1

    # Tap for colour
    if tokens[index] == "for":
        result["require"] = True
        index += 1
        result["require_number"] = tokens[index]
        index += 1
        result["require_colour"] = tokens[index]
        index += 1

    action = tokens[index]
    result["action"] = action
    index += 1

    # Is it a modifier-based action?
    if action in MODIFIERS:
        result["field"] = tokens[index]
        index += 1

        # Check for integer value to increment by
        if index < len(tokens):
            if isinstance(tokens[index], tuple):
                result["amount"] = tokens[index]  # Resolve expression later
            else:
                result["amount"] = int(tokens[index])
            index += 1

        # Check for a specific target name
        if index < len(tokens):
            name = tokens[index]
            if name not in TARGET_TYPES and "/" not in name:
                result["name"] = name
                index += 1

        # Check for whether a target is required
        if index < len(tokens):
            if tokens[index] == "creatureid":
                result["creatureid"] = True
                index += 1
            else:
                target_token = tokens[index]
                if '/' in target_token:
                    result["target_type"] = target_token.split('/')
                    index += 1
                elif target_token in TARGET_TYPES:
                    result["target_type"] = target_token
                    index += 1

        # Check whether or not global/all is included
        if index < len(tokens):
            if tokens[index] == "all":  # All means EVERY single active creature
                result["all"] = True
            elif tokens[index] == "global":
                result["global"] = True # Global means ONLY the player's creatures (16.10.26 what was I thinking with this naming convention)

    # Generates mana
    elif action == 'gen':
        amount = 1
        colors = []
        if index < len(tokens):
            if isinstance(tokens[index], tuple):
                result["amount"] = tokens[index]
                index += 1
            else:
                amount = int(tokens[index])
                index += 1
            if index < len(tokens):
                colors = tokens[index].split('/')

        result['field'] = 'mana'
        result['value'] = colors
        result['amount'] = amount

    # General commands
    elif action in ["draw", "discard", "heal", "revive", "nomanareset", "invuln"]:
        if index < len(tokens):
            if isinstance(tokens[index], tuple):
                result["amount"] = tokens[index]
                index += 1

            elif tokens[index] == "creatureid":
                result["creatureid"] = True
                index += 1

            elif tokens[index] == "global":
                result["global"] = True
                index += 1

            elif tokens[index] == "all":
                result["all"] = True
                index += 1

            elif tokens[index].isdigit():
                result["amount"] = tokens[index]
                index += 1

    # Creates a card
    elif action == "create":
        if index < len(tokens):
            if isinstance(tokens[index], tuple):
                result["amount"] = tokens[index]
                index += 1
            else:
                amount = int(tokens[index])
                index += 1

            result["name"] = tokens[index]
            index += 1

        if action == "nomanareset":
            result["amount"] = True

    # Applies an effect onto a card
    elif action == "apply":
        if index < len(tokens):
            result['status'] = tokens[index]
            index += 1

            if tokens[index] == "creatureid":
                result["creatureid"] = True
                index += 1

            else:
                target_token = tokens[index]
                if '/' in target_token:
                    result['target_type'] = target_token.split('/')
                    index += 1

    # Increase/decrease stats for spell cards
    # Syntax should be something like castinc creatureid att 4
    # Permanent increase as opposed to a temporary increase
    elif action in ["castinc", "castdec"]:
        if index < len(tokens):
            if tokens[index] == "creatureid":
                result["creatureid"] = True
                index += 1

            result["field"] = tokens[index]
            index += 1
            result["amount"] = tokens[index]
            index += 1

    # Morphs a creature
    elif action == "morph":
        if index < len(tokens):
            if tokens[index] == "creatureid":
                result["creatureid"] = True
                index += 1

            result["amount"] = tokens[index]

    # Return the parsed result for any action branch
    return result


################## 
# ERROR HANDLING #
##################

class ParseError(Exception):
    """An exception that occurs when handling parsing."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
