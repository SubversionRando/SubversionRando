from typing import Callable, Optional

from item_data import Item
from location_data import Location


ItemLists = tuple[list[Item], list[Item], list[Item], list[Item]]

InitItemLists = Callable[[], ItemLists]

Placement = Callable[
    [list[Location], list[Location], list[Item], ItemLists],
    Optional[tuple[Location, Item]]
]
