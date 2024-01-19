import itertools
from typing import Container

from subversion_rando.area_rando_types import DoorPairs
from subversion_rando.connection_data import vanilla_areas
from subversion_rando.fillAssumed import FillAssumed
from subversion_rando.game import Game, GameOptions
from subversion_rando.item_data import Item
from subversion_rando.loadout import Loadout
from subversion_rando.location_data import pullCSV
from subversion_rando.trick import Trick


def setup(logic: frozenset[Trick]) -> tuple[Game, Loadout]:
    """ returns (all locations, vanilla connections, a new loadout) """
    all_locations = pullCSV()
    options = GameOptions(logic, False, "D", True)
    game = Game(options, all_locations, vanilla_areas(), 0)
    loadout = Loadout(game)
    return game, loadout


def load_everything_except(loadout: Loadout, excluded_items: Container[Item]) -> None:
    """ fill `loadout` with all items except `excluded_items` """
    fa = FillAssumed(DoorPairs([]))
    for item in itertools.chain(*fa.itemLists):
        if item not in excluded_items:
            loadout.append(item)
