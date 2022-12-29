from dataclasses import dataclass, field
from typing import Mapping, Union

from connection_data import AreaDoor, vanilla_doors
from item_data import Item
from location_data import Location
from logic_shortcut import LogicShortcut
from trick import Trick


def door_factory() -> dict[AreaDoor, Union[Item, LogicShortcut]]:
    return vanilla_doors


@dataclass
class Game:
    """ a composition of all the components that make up the generated seed """
    logic: frozenset[Trick]
    all_locations: dict[str, Location]
    area_rando: bool
    connections: list[tuple[AreaDoor, AreaDoor]]
    door_data: Mapping[AreaDoor, Union[Item, LogicShortcut]] = field(default_factory=door_factory)
