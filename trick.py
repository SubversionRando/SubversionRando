from typing import Iterator, NoReturn
from item_data import Item


class Trick:
    """ items: all the items needed to do this trick """
    _items: tuple[Item, ...]
    __slots__ = "_items",

    def __init__(self, *items: Item) -> None:
        self._items = items

    def __hash__(self) -> int:
        return hash(id(self))

    def __eq__(self, __o: object) -> bool:
        return __o is self

    def __iter__(self) -> Iterator[Item]:
        for item in self._items:
            yield item

    def __bool__(self) -> NoReturn:
        # TODO: unit test for this like the one for logic shortcut
        raise TypeError("cannot interpret Trick as bool - did you forget `in loadout`?")
