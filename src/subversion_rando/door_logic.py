from .area_rando_types import AreaDoor
from .connection_data import area_doors
from .logic_shortcut import LogicShortcut


def canOpen(door: AreaDoor) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (loadout.game.options.area_rando and door.name in area_doors) or
        loadout.game.door_data[door] in loadout
    ))
