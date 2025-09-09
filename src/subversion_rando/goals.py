from collections.abc import Sequence
from dataclasses import dataclass

Event = tuple[int, str, str]


@dataclass
class Goals:
    """ choices made for objective rando """
    objectives: Sequence[Event] = ()
    map_station_order: Sequence[int] = ()
