import pytest

from subversion_rando.area_rando_types import DoorPairs
from subversion_rando.game import Game, GameOptions
from subversion_rando.item_data import Items
from subversion_rando.loadout import ItemCounter, Loadout
from subversion_rando.location_data import new_locations


def test_loadout_from_dict_of_counts() -> None:
    """ make sure `Loadout` ctor works with `Counter` """
    items = {
        Items.Energy: 3
    }

    loadout = Loadout(
        Game(GameOptions(frozenset(), False, "D", False), new_locations(), DoorPairs(()), 0),
        items
    )

    assert loadout.count(Items.Energy) == 3, f"{loadout.count(Items.Energy)=}"


def test_deprecated_counter() -> None:
    with pytest.warns(DeprecationWarning):
        _ = Items.Energy in ItemCounter()
