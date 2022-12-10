from typing import TYPE_CHECKING

from item_data import Item, Items
from logic_shortcut import LogicShortcut

if TYPE_CHECKING:
    from loadout import Loadout

STARTING_ENERGY = 99
ENERGY_PER_TANK = 100
FOR_N_TANKS = 12
LATER_ENERGY_PER_TANK = 50

canUsePB = LogicShortcut(lambda loadout: (
    loadout.has_all(Items.Morph, Items.PowerBomb)
))


def energy_from_tanks(n: int) -> int:
    first_tanks = min(FOR_N_TANKS, n) * ENERGY_PER_TANK
    later_tanks = max(0, n - FOR_N_TANKS) * LATER_ENERGY_PER_TANK
    return STARTING_ENERGY + first_tanks + later_tanks


def energy_req(amount: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        energy_from_tanks(loadout.count(Items.Energy)) >= amount
    ))


_item_to_ammo: dict[Item, int] = {
    Items.Missile: 10,
    Items.Super: 10,
    Items.PowerBomb: 10,
    Items.LargeAmmo: 10,
    Items.SmallAmmo: 5,
}


def ammo_in_loadout(loadout: "Loadout") -> int:
    total = 0
    for item, value in _item_to_ammo.items():
        total += loadout.count(item) * value
    return total


def ammo_req(amount: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        ammo_in_loadout(loadout) >= amount
    ))


crystal_flash = LogicShortcut(lambda loadout: (
    loadout.has_all(canUsePB, ammo_req(100))
))


def varia_or_hell_run(energy: int) -> LogicShortcut:
    """ needs varia or energy """
    return LogicShortcut(lambda loadout: (
        loadout.has_any(Items.Varia, energy_req(energy))
    ))
