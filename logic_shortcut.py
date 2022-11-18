from typing import Callable, TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from loadout import Loadout


class LogicShortcut:
    def __init__(self, access: "Callable[[Loadout], bool]") -> None:
        self.access: "Callable[[Loadout], bool]" = access

    def __bool__(self) -> NoReturn:
        raise TypeError("cannot interpret LogicShortcut as bool - did you forget `in loadout`?")
