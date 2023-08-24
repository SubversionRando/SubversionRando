from typing import Iterable, Optional

from logic_area import area_logic
from logic_locations import location_logic
from connection_data import AreaDoor, area_doors
from loadout import Loadout
from location_data import Location


def otherDoor(door: AreaDoor, Connections: list[tuple[AreaDoor, AreaDoor]]) -> AreaDoor:
    for pair in Connections :
        if (door in pair) :
            other = pair[0]
            if door == other :
                other = pair[1]
            return other
    raise ValueError(f"door {door} is not in Connections {[(c0.name, c1.name) for c0, c1 in Connections]}")


def _updateAreaLogic(loadout: Loadout, excluded_door: Optional[AreaDoor] = None) -> None:
    stuck = False  # check if loadout keeps increasing
    while not stuck:
        prev_loadout = loadout.copy()
        for _area, paths in area_logic.items():
            for path, access in paths.items():
                origin, destination = path
                if area_doors[destination] not in loadout:
                    other = otherDoor(area_doors[destination], loadout.game.connections)
                    if area_doors[destination] == excluded_door or other == excluded_door:
                        continue
                    if other in loadout:
                        loadout.append(area_doors[destination])
                    elif (area_doors[origin] in loadout) and access(loadout):
                        loadout.append(area_doors[destination])
                        loadout.append(other)
        if loadout == prev_loadout :
            stuck = True


def updateLogic(unusedLocations: Iterable[Location],
                loadout: Loadout,
                excluded_door: Optional[AreaDoor] = None) -> Iterable[Location]:
    _updateAreaLogic(loadout, excluded_door)
    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = location_logic[thisLoc['fullitemname']](loadout)

    return unusedLocations
