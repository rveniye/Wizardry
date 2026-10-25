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

Card effects are written as a dict. Each key is a trigger and each value is the
ability (or a list of abilities) that fires on it, without the trigger itself.
Static abilities go under the key "None?"

    effect={"None?": "entertap", "tap?": ["for 1 blue gen 2 green", "gen 1 blue"]}

A plain "trigger? ability; ..." string is still accepted, so older effects keep working.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Union
from error_handling import ParseError

if TYPE_CHECKING:
    from src.game import Game


STATIC_TRIGGER = "None?"
EffectDict = Dict[str, Union[str, List[str]]]

TRIGGERS = ["tap?", "summon?", "enter?", "attack?", "block?", "discard?"]
STATIC_ABILITIES = [
    "haste", "flying", "reach", "entertap", "unblockable", "trample", "invincible", "vigilant"
]
ACTIONS = [
    "gen", "draw", "discard", "heal", "return", "count", "damage", "destroy",
    "apply", "kill", "morph", "revive", "nomanareset", "create", "invuln",
    "castinc", "castdec",
]
MODIFIERS = ["inc", "dec"]
PLACES = ["graveyard", "deck", "hand"]
FIELDS = ["att", "end"]
TARGET_TYPES = ["creatureid", "player"]


def parse(effect: Union[EffectDict, str], game_state: Game, player: str) -> list[dict[str, Any]]:
    """
    Parse an effect into a list of normalised instruction dictionaries.
    
    Args:
        effect (Union [EffectDict, str]): The effect to be parsed.
        game_state (Game): The current game object.
        player (str): The current player.

    Returns:
        list[dict[str, Any]]
    """
    instructions: list[dict[str, Any]] = []
    for instruction in _instructions_from(effect):
        parsed = parse_single(instruction, game_state, player)
        if parsed is not None:
            instructions.append(parsed)
    return instructions


def _instructions_from(effect: Union[EffectDict, str]) -> Iterator[str]:
    """
    Yield individual instruction strings, retaining legacy string support.
    
    Args:
        effect (Union[EffectDict, str]): The effect that needs to be yielded.

    Returns:
        Iterator[str]
    """
    if not effect:
        return

    if isinstance(effect, str):
        for instruction in effect.split(";"):
            if instruction.strip():
                yield instruction.strip()
        return

    if not isinstance(effect, dict):
        raise ParseError(f"Expected the effect to be a dict, got {type(effect).__name__}.")

    for trigger, abilities in effect.items():
        if not isinstance(trigger, str):
            raise ParseError(
                f"Trigger keys must be strings, got {trigger!r}. "
                f'Use "{STATIC_TRIGGER}" for static abilities.'
            )

        is_static = trigger == STATIC_TRIGGER
        if not is_static and trigger not in TRIGGERS:
            raise ParseError(f"Unknown trigger {trigger!r}. Expected one of {TRIGGERS!r} or {STATIC_TRIGGER!r}.")

        if isinstance(abilities, str):
            abilities = [abilities]
        elif not isinstance(abilities, list):
            raise ParseError(f"Abilities for trigger {trigger!r} must be a string or list of strings.")

        for ability in abilities:
            if not isinstance(ability, str):
                raise ParseError(f"Ability values must be strings, got {type(ability).__name__}.")
            ability = ability.strip()
            if not ability:
                continue

            if ability.split()[0].endswith("?"):
                raise ParseError(f"{ability!r} starts with a trigger. Put the trigger in the dict key instead.")
            yield ability if is_static else f"{trigger} {ability}"


def tokenise(instruction: str, game_state: Game, player: str) -> list[Any]:
    """
    Split an instruction into tokens.
    
    Args:
        instruction (str): The instruction to be tokenised.
        game_state (Game): The game object.
        player (str): The current player.

    Returns:
        list[Any]
    """
    tokens: list[Any] = []
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

        if in_quotes:
            current += char
            continue

        if char == "(":
            if depth == 0:
                if current.strip():
                    tokens.append(current.strip())
                    current = ""
                paren_content = ""
            else:
                paren_content += char
            depth += 1
            continue

        if char == ")":
            if depth == 0:
                raise ParseError(f"Unexpected ')' in instruction {instruction!r}.")
            depth -= 1
            if depth == 0:
                # Avoid circular import.
                from src.modules.util_functions import resolve_expr

                tokens.append(resolve_expr(paren_content.split(), game_state, player))
                paren_content = ""
            else:
                paren_content += char
            continue

        if depth > 0:
            paren_content += char
        elif char.isspace():
            if current.strip():
                tokens.append(current.strip())
                current = ""
        else:
            current += char

    if in_quotes:
        raise ParseError(f"Unclosed quote in instruction {instruction!r}.")
    
    if depth:
        raise ParseError(f"Unclosed parenthesis in instruction {instruction!r}.")
    
    if current.strip():
        tokens.append(current.strip())

    return tokens


def _require_token(tokens: list[Any], index: int, instruction: str, purpose: str) -> Any:
    """Return a token or raise a readable parse error instead of IndexError."""
    if index >= len(tokens):
        raise ParseError(f"Missing {purpose} in instruction {instruction!r}.")
    return tokens[index]


def parse_single(instruction: str, game_state: Game, player: str) -> dict[str, Any] | None:
    """Parse one instruction into a normalised dictionary."""
    instruction = instruction.strip()
    if not instruction:
        return None

    result: dict[str, Any] = {
        "trigger": STATIC_TRIGGER,
        "raw": instruction,
        "action": None,
        "field": None,
        "amount": None,
    }

    if instruction in STATIC_ABILITIES:
        result["action"] = "static"
        result["status"] = instruction
        return result

    tokens = tokenise(instruction, game_state, player)
    if not tokens:
        return None

    index = 0
    if tokens[index].endswith("?"):
        trigger = tokens[index]
        if trigger not in TRIGGERS:
            raise ParseError(f"Unknown trigger {trigger!r} in instruction {instruction!r}.")
        result["trigger"] = trigger
        index += 1

    action = _require_token(tokens, index, instruction, "action")
    index += 1
    result["action"] = action

    if action in MODIFIERS:
        result["field"] = _require_token(tokens, index, instruction, "field")
        index += 1
        if result["field"] not in FIELDS:
            raise ParseError(f"Unknown field {result['field']!r} in instruction {instruction!r}.")

        amount_token = _require_token(tokens, index, instruction, "amount")
        result["amount"] = amount_token if isinstance(amount_token, tuple) else _parse_int(amount_token, instruction)
        index += 1

        # if index < len(tokens):
        #     name = tokens[index]
        #     if name not in TARGET_TYPES and "/" not in str(name):
        #         result["name"] = name
        #         index += 1

        if index < len(tokens):
            target_token = tokens[index]
            if target_token == "creatureid":
                result["creatureid"] = True
                index += 1
            elif "/" in str(target_token):
                result["target_type"] = str(target_token).split("/")
                index += 1
            elif target_token in TARGET_TYPES:
                result["target_type"] = target_token
                index += 1

        if index < len(tokens):
            if tokens[index] == "all":
                result["all"] = True
                index += 1
            elif tokens[index] == "global":
                result["global"] = True
                index += 1

    elif action == "gen":
        result["field"] = "mana"
        result["value"] = []
        result["amount"] = 1

        if index < len(tokens):
            amount_token = tokens[index]
            if isinstance(amount_token, tuple):
                result["amount"] = amount_token
                index += 1
            else:
                result["amount"] = _parse_int(amount_token, instruction)
                index += 1

        if index < len(tokens):
            result["value"] = str(tokens[index]).split("/")
            index += 1

    elif action in {"draw", "discard", "heal", "revive", "invuln"}:
        if index < len(tokens):
            token = tokens[index]
            if isinstance(token, tuple):
                result["amount"] = token
                index += 1

            elif token == "creatureid":
                result["creatureid"] = True
                index += 1

            elif token in {"global", "all"}:
                result[token] = True
                index += 1

            elif str(token).isdigit():
                result["amount"] = int(token)
                index += 1

    elif action == "create":
        amount_token = _require_token(tokens, index, instruction, "creation amount")
        if isinstance(amount_token, tuple):
            result["amount"] = amount_token

        else:
            result["amount"] = _parse_int(amount_token, instruction)

        index += 1
        result["name"] = _require_token(tokens, index, instruction, "card name")
        index += 1

    elif action == "nomanareset":
        # This used to be nested under the 'create' branch, making it unreachable.
        result["amount"] = True

    elif action == "apply":
        result["status"] = _require_token(tokens, index, instruction, "status")
        index += 1

        if index < len(tokens):
            target_token = tokens[index]

            if target_token == "creatureid":
                result["creatureid"] = True
                index += 1

            elif "/" in str(target_token):
                result["target_type"] = str(target_token).split("/")
                index += 1

            elif target_token in TARGET_TYPES:
                result["target_type"] = target_token
                index += 1

    elif action in {"castinc", "castdec"}:
        if index < len(tokens) and tokens[index] == "creatureid":
            result["creatureid"] = True
            index += 1

        result["field"] = _require_token(tokens, index, instruction, "field")
        index += 1

        if result["field"] not in FIELDS:
            raise ParseError(f"Unknown field {result['field']!r} in instruction {instruction!r}.")
        
        amount_token = _require_token(tokens, index, instruction, "amount")
        result["amount"] = amount_token if isinstance(amount_token, tuple) else _parse_int(amount_token, instruction)
        index += 1

    elif action == "morph":
        if index < len(tokens) and tokens[index] == "creatureid":
            result["creatureid"] = True
            index += 1

        result["amount"] = _require_token(tokens, index, instruction, "morph value")
        index += 1

    elif action not in ACTIONS:
        raise ParseError(f"Unknown action {action!r} in instruction {instruction!r}.")

    return result


def _parse_int(value: Any, instruction: str) -> int:
    """Parse an integer token with a domain-specific error message."""
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ParseError(f"Expected an integer amount, got {value!r} in {instruction!r}.") from exc


print(parse("summon? inc att 2 global", None, None))