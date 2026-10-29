# from src.cards import Card
from src.game import Game
from src.modules.error_handling import CardNotFound


def increment_att(game: Game, card_id: str, amount: int, scope: list | None=None):
    if scope is None:
        if game.active_creatures[game.p1_name].get(card_id) is not None:
            game.active_creatures[game.p1_name][card_id].att += amount
        else:
            if game.active_creatures[game.p2_name].get(card_id) is not None: game.active_creatures[game.p2_name][card_id].att += amount
            else: raise CardNotFound(f"Error: {card_id} does not exist.")

    elif scope[1] == "all":
        for key, _ in game.active_creatures[game.p1_name].items():
            game.active_creatures[game.p1_name][key].att += amount
        for key, _ in game.active_creatures[game.p2_name].items():
            game.active_creatures[game.p2_name][key].att += amount

    elif scope[1] == "global":
        for key, _ in game.active_creatures[scope[0]].items(): game.active_creatures[scope[0]][key].att += amount
        

def decrement_att(game: Game, card_id: str, amount: int, scope: list | None=None):
    if scope is None:
        if game.active_creatures[game.p1_name].get(card_id) is not None:
                game.active_creatures[game.p1_name][card_id].att -= amount
        else:
            if game.active_creatures[game.p2_name].get(card_id) is not None: game.active_creatures[game.p2_name][card_id].att -= amount
            else: raise CardNotFound(f"Error: {card_id} does not exist.")

    elif scope[1] == "all":
            for key, _ in game.active_creatures[game.p1_name].items():
                game.active_creatures[game.p1_name][key].att -= amount
            for key, _ in game.active_creatures[game.p2_name].items():
                game.active_creatures[game.p2_name][key].att -= amount
    
    elif scope[1] == "global":
        for key, _ in game.active_creatures[scope[0]].items(): game.active_creatures[scope[0]][key].att -= amount
        
