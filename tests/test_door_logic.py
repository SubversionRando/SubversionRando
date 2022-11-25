# import hacks, because this project is not a python package
import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from connection_data import area_doors
from door_logic import canOpen
from item_data import Items
from loadout import Loadout
from logicCasual import Casual


def test_area_rando() -> None:
    area_rando = True
    loadout = Loadout(Casual, area_rando)

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout


def test_area_rando_with_items() -> None:
    area_rando = True
    loadout = Loadout(Casual, area_rando, (Items.PowerBomb, Items.Super))

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout


def test_non_area_rando_locked() -> None:
    area_rando = False
    loadout = Loadout(Casual, area_rando)

    assert canOpen(area_doors["CraterR"]) not in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) not in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) not in loadout
    assert canOpen(area_doors["FoyerR"]) not in loadout


def test_non_area_rando_open() -> None:
    area_rando = False
    loadout = Loadout(Casual, area_rando, (Items.PowerBomb, Items.Super))

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout
