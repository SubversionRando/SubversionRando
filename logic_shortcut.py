from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from loadout import Loadout


class LogicShortcut:
    access: "Callable[[Loadout], bool]"

    def __init__(self, access: "Callable[[Loadout], bool]") -> None:
        self.access = access
