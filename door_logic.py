from connection_data import AreaDoor, area_doors
from logic_shortcut import LogicShortcut


def canOpen(door: AreaDoor) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (loadout.game.area_rando and door[3] in area_doors) or
        loadout.game.door_data[door] in loadout
    ))
