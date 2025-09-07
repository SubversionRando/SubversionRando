"""
for generating lots of seeds in a batch for statistical analysis

just update `game_source` function
and `desc` with the description of what's in the `game_source` function (for the file name)
and `game_count` for how many you want
"""

import datetime
import os
import pickle
import sys
from typing import Iterator, Literal, Optional

from subversion_rando.area_rando_types import AreaDoor
from subversion_rando.game import Exclude, Game, GameOptions
from subversion_rando.hint_types import Hint
from subversion_rando.location_data import Location
from subversion_rando.logic_presets import casual, expert, medium
from subversion_rando.main_generation import generate
from subversion_rando.trick_data import trick_name_lookup


desc = "ECU-w-and-wo-area-rando-D-T-F-cypher-anything"
game_count = 1000


def game_source() -> Iterator[Game]:
    while True:
        yield generate(GameOptions(expert, False, "D", True, False, Exclude.nothing))
        yield generate(GameOptions(casual, False, "D", True, False, Exclude.nothing))
        yield generate(GameOptions(medium, False, "D", True, False, Exclude.nothing))
        yield generate(GameOptions(expert, True, "D", True, False, Exclude.nothing))
        yield generate(GameOptions(casual, True, "D", True, False, Exclude.nothing))
        yield generate(GameOptions(medium, True, "D", True, False, Exclude.nothing))


class GameData:
    """ picklable version of Game """
    # TODO: use Game.to_jsonable()

    logic: list[str]
    all_locations: dict[str, Location]
    area_rando: bool
    connections: list[tuple[AreaDoor, AreaDoor]]
    fill_choice: Literal["M", "MM", "D", "S", "B"]
    seed: int
    small_spaceport: bool
    escape_shortcuts: bool
    item_placement_spoiler: str = ""
    hint_data: Optional[Hint] = None

    def __init__(self, g: Game) -> None:
        self.logic = [trick_name_lookup[t] for t in g.options.logic]
        self.all_locations = g.all_locations
        self.area_rando = g.options. area_rando
        self.connections = list(g.door_pairs.connections())
        self.fill_choice = g.options.fill_choice
        self.seed = g.seed
        self.small_spaceport = g.options.small_spaceport
        self.escape_shortcuts = g.options.escape_shortcuts
        self.item_placement_spoiler = g.item_placement_spoiler
        self.hint_data = g.hint_data


def generate_games(count: int) -> None:
    now = datetime.datetime.now()
    file_name = f'data{os.sep}{desc}-{now.strftime("%Y-%m-%d-%H-%M-%S")}.dat'
    games_buffer: list[Game] = []
    game_source_iter = game_source()
    saved_stdout = sys.stdout
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    for _ in range(count):

        games_buffer.append(next(game_source_iter))

        if len(games_buffer) > 15:
            saved_stdout.write(".")
            saved_stdout.flush()
            with open(file_name, "ab") as file:
                for g in games_buffer:
                    pickle.dump(GameData(g), file)
                games_buffer.clear()

    with open(file_name, "ab") as file:
        for g in games_buffer:
            pickle.dump(GameData(g), file)
        games_buffer.clear()

    sys.stdout = saved_stdout
    print()


if __name__ == "__main__":
    generate_games(game_count)
