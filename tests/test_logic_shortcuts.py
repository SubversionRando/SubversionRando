# import hacks, because this project is not a python package
import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from item_data import Items
from loadout import Loadout
from logic import LogicLevel, energy_req, varia_or_hell_run, energy_from_tanks


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
    loadout = Loadout((Items.Energy for _ in range(10)))
    loadout.logic_level = LogicLevel.CASUAL

    assert energy_req(900, 1100) in loadout
    assert energy_req(900, 700) in loadout
    assert energy_req(1100, 700) not in loadout
    assert energy_req(1100, 1700) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert energy_req(1100, 700) in loadout
    assert energy_req(1100, 1700) in loadout

    loadout = Loadout()  # empty

    assert energy_req(900, 1100) not in loadout

    loadout.logic_level = LogicLevel.EXPERT

    assert energy_req(900, 700) not in loadout

    loadout.append(Items.Energy)

    assert energy_req(900, 700) not in loadout

    for _ in range(7):
        loadout.append(Items.Energy)

    assert energy_req(900, 700) in loadout
    assert energy_req(1100, 700) in loadout
    assert energy_req(500, 1100) in loadout, "expert can play like casual"
    assert energy_req(1100, 500) in loadout
    assert energy_req(1100, 900) not in loadout


def test_varia_or_hell_run() -> None:
    loadout = Loadout((Items.Energy for _ in range(10)))
    loadout.logic_level = LogicLevel.CASUAL

    assert varia_or_hell_run(400) not in loadout
    assert varia_or_hell_run(800) not in loadout
    assert varia_or_hell_run(1200) not in loadout

    loadout.append(Items.Varia)

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout

    loadout = Loadout((Items.Energy for _ in range(10)))
    loadout.logic_level = LogicLevel.EXPERT

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert varia_or_hell_run(1200) in loadout

    loadout.append(Items.Varia)

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout
    assert varia_or_hell_run(1400) in loadout


if __name__ == "__main__":
    test_energy_req()
