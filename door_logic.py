from connection_data import AreaDoor, area_doors
from logic_shortcut import LogicShortcut


def canOpen(door: AreaDoor) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (loadout.area_rando and door[3] in area_doors) or
        loadout.door_data[door] in loadout
    ))
