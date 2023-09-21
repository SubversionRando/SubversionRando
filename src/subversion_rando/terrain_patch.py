from dataclasses import dataclass
from typing import NamedTuple, Optional


class Space(NamedTuple):
    size: int
    location: int


@dataclass
class Patch:
    data: bytes
    pointers: list[int]
    freed_space: Optional[Space] = None
