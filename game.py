from dataclasses import dataclass, field
from typing import Mapping, Type

from connection_data import AreaDoor, vanilla_doors
from item_data import Item
from location_data import Location
from logicInterface import LogicInterface


def door_factory() -> dict[AreaDoor, Item]:
    return vanilla_doors


@dataclass
class Game:
    """ a composition of all the components that make up the generated seed """
    logic: Type[LogicInterface]
    all_locations: list[Location]
    area_rando: bool
    connections: list[tuple[AreaDoor, AreaDoor]]
    door_data: Mapping[AreaDoor, Item] = field(default_factory=door_factory)
