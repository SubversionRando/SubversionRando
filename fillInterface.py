import abc
from typing import Optional, Union

from connection_data import Connection
from item_data import Item
from location_data import Location

# `abc`` means the algorithm isn't implemented here
# This is just defining what the algorithm needs to implement.


class FillAlgorithm(abc.ABC):
    @abc.abstractmethod
    def choose_placement(self,
                         availableLocations: list[Location],
                         locArray: list[Location],
                         loadout: list[Union[Item, Connection]]) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

    @abc.abstractmethod
    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
