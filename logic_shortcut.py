from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from loadout import Loadout


class LogicShortcut:
    def __init__(self, access: "Callable[[Loadout], bool]") -> None:
        self.access: "Callable[[Loadout], bool]" = access
