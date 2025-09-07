from typing import Any, Iterable

from subversion_rando import logic_boss_reach
from subversion_rando.connection_data import vanilla_areas
from subversion_rando.game import Game, GameOptions
from subversion_rando.goal import generate_goals
from subversion_rando.hints import hint_data
from subversion_rando.loadout import Loadout
from subversion_rando.location_data import new_locations
from subversion_rando.logic_boss_reach import reach_and_kill
from subversion_rando.logic_goal import goal_logic
from subversion_rando.logic_shortcut import LogicShortcut


def test_reach_and_kill_typing() -> None:
    keys: Iterable[Any] = logic_boss_reach.BossName.__dict__["__args__"]  # Any so it counts as Literal
    for key in keys:
        assert isinstance(reach_and_kill(key), LogicShortcut)


def test_hint_logic() -> None:
    locations = new_locations()
    loadout = Loadout(Game(GameOptions(frozenset(), False, "B", True), locations, vanilla_areas(), 0))
    for _, _, logic in hint_data.values():
        assert isinstance(logic, LogicShortcut)
        _ = (logic in loadout)


def test_goal_logic() -> None:
    import random

    options = GameOptions(frozenset(), False, "D", True, objective_rando=999)  # all the objectives
    locations = new_locations()
    goals = generate_goals(options, set(), random.randrange(1073741824))
    loadout = Loadout(Game(options, locations, vanilla_areas(), 0))
    _ = (goal_logic(goals) in loadout)
