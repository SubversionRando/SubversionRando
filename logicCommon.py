from typing import TYPE_CHECKING

from item_data import Item, Items
from logic_shortcut import LogicShortcut
from trick_data import Tricks

if TYPE_CHECKING:
    from loadout import Loadout

# TODO: Does some logic around Ocean Shore need to be different
# if Metroid Suit and Supers are in early spaceport?
# If the ship is crashed,
# for example, getting from OceanShoreR to Sandy Gully, is harder.

STARTING_ENERGY = 99
ENERGY_PER_TANK = 100
FOR_N_TANKS = 12
LATER_ENERGY_PER_TANK = 50

canUsePB = LogicShortcut(lambda loadout: (
    loadout.has_all(Items.Morph, Items.PowerBomb)
))
""" might only have enough ammo for 1 power bomb - can use `can_use_pbs(pbs_needed)` instead """

canBomb = LogicShortcut(lambda loadout: (
    (Items.Morph in loadout) and loadout.has_any(Items.Bombs, Items.PowerBomb)
))
""" might only have enough ammo for 1 power bomb - can use `can_bomb(pbs_needed)` instead """


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
    loadout.has_all(Items.Morph, Items.PowerBomb, ammo_req(100))
))


def _hell_run_energy(min_energy: int, loadout: Loadout) -> int:
    """ based on tricks """
    if Tricks.hell_run_hard in loadout:
        return min_energy
    if Tricks.hell_run_medium in loadout:
        return (min_energy * 3) // 2
    if Tricks.hell_run_easy in loadout:
        return min_energy * 2
    return 9001


def varia_or_hell_run(energy: int) -> LogicShortcut:
    """ needs varia or energy or (less energy and crystal flash) """
    return LogicShortcut(lambda loadout: (
        (Items.Varia in loadout) or
        (energy_req(_hell_run_energy(energy, loadout)) in loadout) or
        (
            (energy_req(_hell_run_energy((energy + 100) // 2, loadout)) in loadout) and
            (crystal_flash in loadout)
        )
    ))


def can_use_pbs(pbs_needed: int) -> LogicShortcut:
    """ How many PBs do you need between opportunities to refill ammo? """
    return LogicShortcut(lambda loadout: (
        (Items.Morph in loadout) and
        (Items.PowerBomb in loadout) and
        (ammo_req(pbs_needed * 10) in loadout)
    ))


def can_bomb(pbs_needed: int) -> LogicShortcut:
    """
    If you don't have bombs, how many PBs do you need?
    (between opportunities to refill ammo)
    """
    return LogicShortcut(lambda loadout: (
        (Items.Morph in loadout) and
        ((Items.Bombs in loadout) or (
            (Items.PowerBomb in loadout) and
            (ammo_req(pbs_needed * 10) in loadout)
        ))
    ))
