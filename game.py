from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Mapping, Optional, Union

from connection_data import AreaDoor, vanilla_doors
from item_data import Item
from location_data import Location
if TYPE_CHECKING:
    from logic_shortcut import LogicShortcut
    from trick import Trick


def door_factory() -> "dict[AreaDoor, Union[Item, LogicShortcut]]":
    return vanilla_doors


@dataclass
class Game:
    """ a composition of all the components that make up the generated seed """
    logic: "frozenset[Trick]"
    all_locations: dict[str, Location]
    area_rando: bool
    connections: list[tuple[AreaDoor, AreaDoor]]
    fill_choice: Literal["M", "MM", "D", "S"]
    seed: int
    small_spaceport: bool
    door_data: "Mapping[AreaDoor, Union[Item, LogicShortcut]]" = field(default_factory=door_factory)
    item_placement_spoiler: str = ""
    hint_data: Optional[tuple[str, bytes]] = None
