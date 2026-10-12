from src.modules.w_parser import parse
import json


with open("db/fsh2848/game_state.json", "r") as f:
    game_state = json.load(f)


my_parser = parse("attacking? inc att (graveyard count skeleton)", game_state, game_state["current_player"])
print(my_parser)
