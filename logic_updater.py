from typing import Iterable
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


def _updateAreaLogic(loadout: Loadout) -> None:
    stuck = False  # check if loadout keeps increasing
    while not stuck:
        prev_loadout = loadout.copy()
        for _area, paths in loadout.game.logic.area_logic.items():
            for path, access in paths.items():
                origin, destination = path
                if area_doors[destination] not in loadout:
                    other = otherDoor(area_doors[destination], loadout.game.connections)
                    if other in loadout:
                        loadout.append(area_doors[destination])
                    elif (area_doors[origin] in loadout) and access(loadout):
                        loadout.append(area_doors[destination])
                        loadout.append(other)
        if loadout == prev_loadout :
            stuck = True


def updateLogic(unusedLocations: Iterable[Location],
                loadout: Loadout) -> Iterable[Location]:
    _updateAreaLogic(loadout)
    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = loadout.game.logic.location_logic[thisLoc['fullitemname']](loadout)

    return unusedLocations
