from typing import Any, Iterable

from subversion_rando import logic_boss_reach
from subversion_rando.connection_data import vanilla_areas
from subversion_rando.game import Game, GameOptions
from subversion_rando.goal import generate_goals
from subversion_rando.hints import hint_data
from subversion_rando.loadout import Loadout
from subversion_rando.location_data import pullCSV
from subversion_rando.logic_boss_reach import reach_and_kill
from subversion_rando.logic_goal import goal_logic
from subversion_rando.logic_shortcut import LogicShortcut


def test_reach_and_kill_typing() -> None:
    _BossName = getattr(logic_boss_reach, "_BossName")
    keys: Iterable[Any] = _BossName.__dict__["__args__"]  # Any so it counts as Literal
    for key in keys:
        assert isinstance(reach_and_kill(key), LogicShortcut)


def test_hint_logic() -> None:
    locations = pullCSV()
    loadout = Loadout(Game(GameOptions(frozenset(), False, "B", True), locations, vanilla_areas(), 0))
    for _, _, logic in hint_data.values():
        assert isinstance(logic, LogicShortcut)
        _ = (logic in loadout)


def test_goal_logic() -> None:
    options = GameOptions(frozenset(), False, "D", True, objective_rando=999)  # all the objectives
    locations = pullCSV()
    goals = generate_goals(options)
    loadout = Loadout(Game(options, locations, vanilla_areas(), 0))
    _ = (goal_logic(goals) in loadout)
