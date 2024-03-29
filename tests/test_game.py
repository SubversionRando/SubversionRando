import json

from subversion_rando.game import CypherItems, Game, GameOptions
from subversion_rando.main_generation import generate
from subversion_rando.trick_data import Tricks


def test_json() -> None:
    options = GameOptions(
        logic=frozenset([Tricks.dark_easy, Tricks.wave_gate_glitch]),
        area_rando=True,
        fill_choice="D",
        small_spaceport=False,
        escape_shortcuts=True,
        cypher_items=CypherItems.SmallAmmo,
        daphne_gate=True,
        objective_rando=3
    )
    game = generate(options)

    game_dict = game.to_jsonable()
    # from pprint import pprint
    # pprint(game_dict)
    game_str = json.dumps(game_dict)
    return_to_dict = json.loads(game_str)
    # assert game_dict == return_to_dict, f"{game_str=}"  # tuples change to lists
    return_to_game = Game.from_jsonable(return_to_dict)
    assert return_to_game == game, f"{return_to_game=}\n{game=}"
