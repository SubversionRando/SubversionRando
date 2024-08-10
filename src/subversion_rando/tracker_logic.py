from typing import Dict, List, Mapping

from subversion_rando.door_logic import vanilla_doors
from subversion_rando.area_rando_types import DoorPairs
from subversion_rando.connection_data import vanilla_areas
from subversion_rando.game import Game, GameOptions
from subversion_rando.item_data import Item, all_items
from subversion_rando.loadout import Loadout
from subversion_rando.location_data import Location, new_locations
from subversion_rando.solver import solve


class TrackerLogic:
    options: GameOptions
    door_pairs: DoorPairs = vanilla_areas()  # TODO: area rando support

    def __init__(self) -> None:
        self.options = GameOptions(
            frozenset(),  # TODO: custom logic support
            False,  # TODO: area rando support
            "D",
            True
        )

    def items_to_locations(self, items: Mapping[Item, int]) -> List[Location]:
        game = Game(
            self.options,
            new_locations(),
            self.door_pairs,
            0,
            door_data=vanilla_doors  # TODO: area rando support
        )
        loadout = Loadout(game, items)
        _, _, locations = solve(game, loadout)
        return locations

    def item_names_to_location_names(self, items: Mapping[str, int]) -> List[str]:
        """ returns empty list if invalid item names are given (list should never be empty otherwise) """
        items_converted: Dict[Item, int] = {}
        for item_name, number in items.items():
            item = all_items.get(item_name)
            if item is None:
                return []
            items_converted[item] = number

        locations = self.items_to_locations(items_converted)
        return [loc["fullitemname"] for loc in locations]
