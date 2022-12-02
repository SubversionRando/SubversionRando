from item_data import Items
from logic_shortcut import LogicShortcut

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


def varia_or_hell_run(energy: int) -> LogicShortcut:
    """ needs varia or energy """
    return LogicShortcut(lambda loadout: (
        loadout.has_any(Items.Varia, energy_req(energy))
    ))
