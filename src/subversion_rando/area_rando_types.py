from typing import Iterable, Iterator, NamedTuple


class AreaDoor(NamedTuple):
    address: str
    data: str
    """ the data of the vanilla door that goes here """
    area_name: str
    name: str
    region: int


class DoorPairs:
    _list: list[tuple[AreaDoor, AreaDoor]]
    _pairs: dict[AreaDoor, AreaDoor]

    def __init__(self, connections: Iterable[tuple[AreaDoor, AreaDoor]]) -> None:
        self._list = list(connections)
        self._pairs = {}
        for door_1, door_2 in connections:
            self._pairs[door_1] = door_2
            self._pairs[door_2] = door_1

    def other(self, door: AreaDoor) -> AreaDoor:
        return self._pairs[door]

    def connections(self) -> Iterator[tuple[AreaDoor, AreaDoor]]:
        yield from self._list
