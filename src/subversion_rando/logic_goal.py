from subversion_rando.item_data import Items
from .goals import Goals
from .logic_boss_reach import reach_and_kill
from .logic_shortcut import LogicShortcut
from .logic_shortcut_data import can_crash_spaceport


_goal_logic: dict[str, LogicShortcut] = {
    "KRAID": reach_and_kill("kraid"),
    "SPORE SPAWN": reach_and_kill("spore_spawn"),
    "BOMB TORIZO": reach_and_kill("bomb_torizo"),
    "DRAYGON": reach_and_kill("draygon"),
    "DUST TORIZO": reach_and_kill("dust_torizo"),
    "GOLD TORIZO": reach_and_kill("gold_torizo"),
    "CROCOMIRE": reach_and_kill("crocomire"),
    "RIDLEY": reach_and_kill("ridley"),
    "PHANTOON": reach_and_kill("phantoon"),
    "HYPER TORIZO": reach_and_kill("hyper_torizo"),
    "SPACE PORT": can_crash_spaceport,
    "BOTWOON": reach_and_kill("botwoon"),
    "POWER OFF": LogicShortcut(lambda loadout: (
        # Saying we need basically everything is a workaround because we don't have power off logic.
        loadout.has_all(
            Items.Aqua, Items.Charge, Items.DarkVisor, Items.Grapple,
            Items.GravityBoots, Items.Hypercharge, Items.MetroidSuit,
            Items.Morph, Items.PowerBomb, Items.Screw, Items.Speedball,
            Items.SpeedBooster, Items.Super
        )
    )),
}


def goal_logic(goals: Goals) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        all(_goal_logic[obj[1]] in loadout
            for obj in goals.objectives)
    ))
