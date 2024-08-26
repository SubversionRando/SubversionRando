from collections import Counter
from typing import Iterable, Iterator, Optional, Union

from .area_rando_types import AreaDoor
from .game import Game
from .item_data import Item
from .logic_shortcut import LogicShortcut
from .trick import Trick


class ItemCounter(Counter[Union[Item, AreaDoor]]):
    """
    `in` returns false if the count is 0

    With a normal Python `Counter`:
    >>> c = Counter({"a": 0})
    >>> "a" in c
    True

    This changes it to return `False` if the count is less than one.
    """
    def __contains__(self, x: Union[Item, AreaDoor]) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        # The incompatible override will help find usages in code.
        import warnings
        warnings.warn("Don't use `__contains__` on this object, because it will be slow. Do the check inline instead.",
                      DeprecationWarning,
                      stacklevel=2)
        return isinstance(x, Union[Item, AreaDoor]) and self[x] > 0  # pyright: ignore[reportUnnecessaryIsInstance]


class Loadout:
    game: Game
    contents: ItemCounter

    def __init__(self,
                 game: Game,
                 items: Optional[Iterable[Union[Item, AreaDoor]]] = None) -> None:
        self.game = game
        self.contents = ItemCounter(items)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Loadout):
            return False
        return (
            (self.contents == __o.contents) and
            (self.game is __o.game)
        )

    def __contains__(self, x: Union[Item, AreaDoor, LogicShortcut, Trick]) -> bool:
        # using type is instead of isinstance for optimization (this is the most called function in profiler)
        if type(x) is LogicShortcut:
            return x.access(self)
        elif type(x) is Trick:
            if x in self.game.options.logic:
                for item in x.items:
                    if self.contents[item] <= 0:
                        return False
                return True
            return False
        return self.contents[x] > 0  # type: ignore

    def __iter__(self) -> Iterator[Union[Item, AreaDoor]]:
        for item, count in self.contents.items():
            for _ in range(count):
                yield item

    def __len__(self) -> int:
        return sum(self.contents.values())  # `Counter.total()` requires python 3.10

    def __repr__(self) -> str:
        return f"Loadout({self.game}, {self.contents})"

    def count(self, item: Union[Item, AreaDoor]) -> int:
        return self.contents[item]

    def append(self, item: Union[Item, AreaDoor]) -> None:
        self.contents[item] += 1

    def has_all(self, *items: Union[Item, AreaDoor, LogicShortcut, Trick]) -> bool:
        return all(x in self for x in items)

    def has_any(self, *items: Union[Item, AreaDoor, LogicShortcut, Trick]) -> bool:
        return any(x in self for x in items)

    def copy(self) -> "Loadout":
        # TODO: test copy
        return Loadout(self.game, self.contents)
