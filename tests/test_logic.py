# import hacks, because this project is not a python package
import sys
from pathlib import Path
from typing import Type
import pytest

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from connection_data import SunkenNestL, VanillaAreas
from game import Game
from item_data import Items, items_unpackable
from loadout import Loadout
from location_data import Location, pullCSV
from logicCasual import Casual
from logicExpert import Expert
from logicInterface import LogicInterface
from logic_updater import updateAreaLogic, updateLogic


def setup(logic: Type[LogicInterface]) -> tuple[Game, Loadout]:
    """ returns (all locations, vanilla connections, a new loadout) """
    all_locations = pullCSV()
    game = Game(logic, all_locations, False, VanillaAreas())
    loadout = Loadout(game)
    return game, loadout


def test_start_logic() -> None:
    game, loadout = setup(Casual)

    def update_acc() -> list[Location]:
        updateAreaLogic(loadout)
        updateLogic(game.all_locations.values(), loadout)

        return [loc for loc in game.all_locations.values() if loc['inlogic']]

    accessible = update_acc()
    assert len(accessible) == 1, f"accessible len {len(accessible)}"
    assert accessible[0]['fullitemname'] == "Torpedo Bay", f"not Torpedo Bay: {accessible}"

    loadout.append(Items.Missile)
    accessible = update_acc()
    print("  with missile")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 3, "add Gantry and Weapon Locker"

    loadout.append(SunkenNestL)
    accessible = update_acc()
    print("  with planet")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 4, "add Ocean Shore: bottom"

    game, _ = setup(Expert)
    loadout = Loadout(game, loadout.contents)

    accessible = update_acc()
    print("  with expert")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 4, "nothing else? really?"

    loadout.append(Items.Morph)
    accessible = update_acc()
    print("  with morph")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 7


@pytest.mark.parametrize("logic", (Casual, Expert))
def test_all_locations(logic: Type[LogicInterface]) -> None:
    game, loadout = setup(logic)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        loadout.append(item)
    for _ in range(10):
        loadout.append(Items.Energy)

    updateAreaLogic(loadout)
    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    assert len(accessible) == 122, f"acc len {len(accessible)}"


def test_casual_no_hell_runs() -> None:
    game, loadout = setup(Casual)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        if item != Items.Varia:
            loadout.append(item)
    for _ in range(16):
        loadout.append(Items.Energy)

    updateAreaLogic(loadout)
    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    assert len(accessible) < 110, f"acc len {len(accessible)}"


def test_expert_hell_runs() -> None:
    game, loadout = setup(Expert)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        if item != Items.Varia:
            loadout.append(item)
    for _ in range(16):
        loadout.append(Items.Energy)

    updateAreaLogic(loadout)
    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    # 121 because Colosseum requires Varia for expert
    assert len(accessible) >= 121, (
        "expert can't get these without varia: "
        f"{[loc['fullitemname'] for loc in game.all_locations.values() if not loc['inlogic']]}"
    )


if __name__ == "__main__":
    test_start_logic()
    test_casual_no_hell_runs()
    test_expert_hell_runs()
