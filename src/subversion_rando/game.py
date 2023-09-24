from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal, Mapping, Optional, Union

from .connection_data import AreaDoor, vanilla_doors
from .daphne_gate_types import DaphneBlocks
from .goals import Goals
from .item_data import Item, Items
from .location_data import Location
from .logic_shortcut import LogicShortcut
if TYPE_CHECKING:
    from .trick import Trick


def door_factory() -> "dict[AreaDoor, Union[Item, LogicShortcut]]":
    return vanilla_doors


def daphne_factory() -> DaphneBlocks:
    return DaphneBlocks("Screw", "Screw", LogicShortcut(lambda loadout: (
        Items.Screw in loadout
    )))


class CypherItems(Enum):
    Anything = "Anything"
    NotRequired = "Something Not Required"
    SmallAmmo = "Small Ammo Tanks"
    """ also restricts Suzi map stations from being required in objective rando """


@dataclass
class GameOptions:
    logic: "frozenset[Trick]"
    area_rando: bool
    fill_choice: Literal["M", "MM", "D", "S", "B"]
    small_spaceport: bool
    escape_shortcuts: bool = False
    cypher_items: CypherItems = CypherItems.NotRequired
    daphne_gate: bool = False
    objective_rando: int = 0
    _skip_crash_option_set: bool = False
    """ protected because objective rando auto-enables this """

    def skip_crash(self) -> bool:
        """ objective rando automatically includes skip crash space port """
        return self._skip_crash_option_set or self.objective_rando > 0


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
    daphne_blocks: DaphneBlocks = field(default_factory=daphne_factory)
    goals: Goals = field(default_factory=Goals)
