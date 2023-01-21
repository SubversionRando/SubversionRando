from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal, Mapping, Optional, Union

from connection_data import AreaDoor, vanilla_doors
from item_data import Item
from location_data import Location
if TYPE_CHECKING:
    from logic_shortcut import LogicShortcut
    from trick import Trick


def door_factory() -> "dict[AreaDoor, Union[Item, LogicShortcut]]":
    return vanilla_doors


class CypherItems(Enum):
    Anything = "Anything"
    NotRequired = "Something Not Required"
    SmallAmmo = "Small Ammo Tanks"


@dataclass
class GameOptions:
    logic: "frozenset[Trick]"
    area_rando: bool
    fill_choice: Literal["M", "MM", "D", "S", "B"]
    small_spaceport: bool
    escape_shortcuts: bool = False
    cypher_items: CypherItems = CypherItems.NotRequired


@dataclass
class Game:
    """ a composition of all the components that make up the generated seed """
    options: GameOptions
    all_locations: dict[str, Location]
    connections: list[tuple[AreaDoor, AreaDoor]]
    seed: int
    door_data: "Mapping[AreaDoor, Union[Item, LogicShortcut]]" = field(default_factory=door_factory)
    item_placement_spoiler: str = ""
    hint_data: Optional[tuple[str, bytes]] = None
