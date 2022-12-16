# import hacks, because this project is not a python package
import sys
from pathlib import Path
from typing import Type
import pytest

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from connection_data import SunkenNestL, VanillaAreas, area_doors
from game import Game
from item_data import Items, items_unpackable
from loadout import Loadout
from location_data import Location, pullCSV
from logicCasual import Casual
from logicExpert import Expert
from logicInterface import LogicInterface
from logic_updater import updateLogic


def setup(logic: Type[LogicInterface]) -> tuple[Game, Loadout]:
    """ returns (all locations, vanilla connections, a new loadout) """
    all_locations = pullCSV()
    game = Game(logic, all_locations, False, VanillaAreas())
    loadout = Loadout(game)
    return game, loadout


def test_start_logic() -> None:
    game, loadout = setup(Casual)

    def update_acc() -> list[Location]:
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

    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    # 121 because Colosseum requires Varia for expert
    assert len(accessible) >= 121, (
        "expert can't get these without varia: "
        f"{[loc['fullitemname'] for loc in game.all_locations.values() if not loc['inlogic']]}"
    )


def test_crypt_no_bomb_no_wave() -> None:
    """ test hitting switch in Crypt by following bullet with speedball """
    game, loadout = setup(Expert)

    loadout.append(area_doors["RuinedConcourseBL"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Morph)
    loadout.append(Items.PowerBomb)
    loadout.append(Items.Missile)
    loadout.append(Items.HiJump)
    loadout.append(Items.Ice)
    loadout.append(Items.GravitySuit)

    updateLogic(game.all_locations.values(), loadout)

    assert not game.all_locations["Crypt"]["inlogic"]

    loadout.append(Items.Speedball)

    updateLogic(game.all_locations.values(), loadout)

    assert game.all_locations["Crypt"]["inlogic"]


def test_warrior_shrine_speedball() -> None:
    """ test hitting switch in Crypt by following bullet with speedball """
    game, loadout = setup(Casual)

    loadout.append(area_doors["RuinedConcourseBL"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Morph)
    loadout.append(Items.PowerBomb)
    loadout.append(Items.Missile)
    loadout.append(Items.HiJump)
    loadout.append(Items.Ice)
    loadout.append(Items.GravitySuit)

    updateLogic(game.all_locations.values(), loadout)

    assert not game.all_locations["Warrior Shrine: ETank"]["inlogic"]

    loadout.append(Items.Speedball)

    updateLogic(game.all_locations.values(), loadout)

    assert game.all_locations["Warrior Shrine: ETank"]["inlogic"]


def test_norak_perimeters() -> None:
    """ test hitting switch in Crypt by following bullet with speedball """
    game, loadout = setup(Expert)

    loadout.append(area_doors["NorakPerimeterTR"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Screw)

    updateLogic(game.all_locations.values(), loadout)

    assert area_doors["NorakPerimeterBL"] not in loadout


_unique_items = [
    Items.Missile,
    Items.Morph,
    Items.GravityBoots,
    Items.Super,
    Items.Grapple,
    Items.PowerBomb,
    Items.Speedball,
    Items.Bombs,
    Items.HiJump,
    Items.GravitySuit,
    Items.DarkVisor,
    Items.Wave,
    Items.SpeedBooster,
    Items.Spazer,
    Items.Varia,
    Items.Ice,
    Items.MetroidSuit,
    Items.Plasma,
    Items.Screw,
    Items.SpaceJump,
    Items.Charge,
    Items.Hypercharge,
    Items.Xray,
]


def test_hard_required_items() -> None:
    for logic in (Casual, Expert):
        print(f" - {logic.__name__}")
        for excluded_item in _unique_items:
            game, loadout = setup(logic)
            loadout.append(SunkenNestL)
            loadout.append(Items.spaceDrop)
            for item in items_unpackable:
                if item != excluded_item:
                    loadout.append(item)

            # some of the non-unique that can help in logic
            for _ in range(12):
                loadout.append(Items.Energy)
                loadout.append(Items.LargeAmmo)
            loadout.append(Items.SpaceJumpBoost)

            updateLogic(game.all_locations.values(), loadout)

            if logic.can_win(loadout):
                assert excluded_item not in logic.hard_required_items, \
                    f"{excluded_item[0]} in {logic.__name__} hard required items"
                print(f"{excluded_item[0]} not")
            else:
                assert excluded_item in logic.hard_required_items, \
                    f"{excluded_item[0]} missing from {logic.__name__} hard required items"
                print(f"{excluded_item[0]}  - - - - hard required")


if __name__ == "__main__":
    test_hard_required_items()
