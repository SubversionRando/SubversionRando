# import hacks, because this project is not a python package
import sys
from pathlib import Path
import pytest
from game import Game

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from item_data import Items
from loadout import Loadout
from logicCasual import Casual
from logicCommon import energy_from_tanks, energy_req, varia_or_hell_run
from logicExpert import Expert
from logic_shortcut import LogicShortcut


def test_energy_from_tanks() -> None:
    assert energy_from_tanks(0) == 99
    assert energy_from_tanks(1) == 199
    assert energy_from_tanks(2) == 299
    assert energy_from_tanks(3) == 399
    assert energy_from_tanks(4) == 499
    assert energy_from_tanks(7) == 799
    assert energy_from_tanks(10) == 1099
    assert energy_from_tanks(11) == 1199
    assert energy_from_tanks(12) == 1299
    assert energy_from_tanks(13) == 1349
    assert energy_from_tanks(14) == 1399
    assert energy_from_tanks(15) == 1449
    assert energy_from_tanks(16) == 1499


def test_energy_req() -> None:
    game = Game(Casual, [], False, [])
    loadout = Loadout(game, (Items.Energy for _ in range(10)))

    assert energy_req(900) in loadout
    assert energy_req(1100) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert energy_req(1100) in loadout

    loadout = Loadout(game)  # empty

    assert energy_req(900) not in loadout

    game = Game(Expert, [], False, [])
    loadout = Loadout(game)  # empty

    assert energy_req(700) not in loadout

    loadout.append(Items.Energy)

    assert energy_req(700) not in loadout

    for _ in range(7):
        loadout.append(Items.Energy)

    assert energy_req(700) in loadout
    assert energy_req(500) in loadout
    assert energy_req(900) not in loadout


def test_varia_or_hell_run() -> None:
    game = Game(Expert, [], False, [])
    loadout = Loadout(game)

    assert varia_or_hell_run(400) not in loadout
    assert varia_or_hell_run(800) not in loadout
    assert varia_or_hell_run(1200) not in loadout

    for _ in range(10):
        loadout.append(Items.Energy)

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert varia_or_hell_run(1200) in loadout

    loadout.append(Items.Varia)  # varia and energy

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout
    assert varia_or_hell_run(1400) in loadout

    loadout = Loadout(game)
    loadout.append(Items.Varia)  # only varia, no energy

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout
    assert varia_or_hell_run(1400) in loadout


def test_use_as_bool() -> None:
    """
    `LogicShortcut` must have a connection to a `Loadout`,
    so it must be used with `in loadout`

    It will be easy to forget the `in loadout`,
    so this test is to make sure it raises an exception if it's used without it.
    """
    can_bomb_jump = LogicShortcut(lambda loadout: (
        (Items.GravityBoots in loadout) and
        (Items.Bombs in loadout) and
        (Items.Morph in loadout)
    ))
    game = Game(Casual, [], False, [])
    loadout = Loadout(game)

    with pytest.raises(TypeError):
        _ = (
            can_bomb_jump and (Items.Charge in loadout)
        )

    with pytest.raises(TypeError):
        _ = (
            can_bomb_jump or (Items.Screw in loadout)
        )


if __name__ == "__main__":
    test_use_as_bool()
