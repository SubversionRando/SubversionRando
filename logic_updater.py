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
    raise ValueError(f"door {door} is not in Connections {[(c[0][3], c[1][3]) for c in Connections]}")


def updateAreaLogic(loadout: Loadout,
                    connections: list[tuple[AreaDoor, AreaDoor]]) -> None:
    stuck = False  # check if loadout keeps increasing
    while not stuck:
        prev_loadout = loadout.copy()
        for _area, paths in loadout.logic.area_logic.items():
            for path, access in paths.items():
                origin, destination = path
                if area_doors[destination] not in loadout:
                    other = otherDoor(area_doors[destination], connections)
                    if other in loadout:
                        loadout.append(area_doors[destination])
                    elif (area_doors[origin] in loadout) and access(loadout):
                        loadout.append(area_doors[destination])
                        loadout.append(other)
        if loadout == prev_loadout :
            stuck = True


def updateLogic(unusedLocations: list[Location],
                locArray: list[Location],
                loadout: Loadout) -> list[Location]:
    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = loadout.logic.location_logic[thisLoc['fullitemname']](loadout)

    return unusedLocations
