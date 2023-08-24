# import hacks, because this project is not a python package
import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from subversion_rando.connection_data import area_doors
from subversion_rando.door_logic import canOpen
from subversion_rando.game import Game, GameOptions
from subversion_rando.item_data import Items
from subversion_rando.loadout import Loadout
from subversion_rando.logic_presets import casual


_test_options = GameOptions(casual, False, "D", True)


def test_area_rando() -> None:
    _test_options.logic = casual
    _test_options.area_rando = True
    game = Game(_test_options, {}, [], 0)
    loadout = Loadout(game)

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout


def test_area_rando_with_items() -> None:
    _test_options.logic = casual
    _test_options.area_rando = True
    game = Game(_test_options, {}, [], 0)
    loadout = Loadout(game, (Items.PowerBomb, Items.Super))

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout


def test_non_area_rando_locked() -> None:
    _test_options.logic = casual
    _test_options.area_rando = False
    game = Game(_test_options, {}, [], 0)
    loadout = Loadout(game)

    assert canOpen(area_doors["CraterR"]) not in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) not in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) not in loadout
    assert canOpen(area_doors["FoyerR"]) not in loadout


def test_non_area_rando_missing_morph() -> None:
    _test_options.logic = casual
    _test_options.area_rando = False
    game = Game(_test_options, {}, [], 0)
    loadout = Loadout(game, (Items.PowerBomb, Items.Super))

    assert canOpen(area_doors["CraterR"]) not in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) not in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) not in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout


def test_non_area_rando_open() -> None:
    _test_options.logic = casual
    _test_options.area_rando = False
    game = Game(_test_options, {}, [], 0)
    loadout = Loadout(game, (Items.Morph, Items.PowerBomb, Items.Super))

    assert canOpen(area_doors["CraterR"]) in loadout
    assert canOpen(area_doors["WestTerminalAccessL"]) in loadout
    assert canOpen(area_doors["VulnarCanyonL"]) in loadout
    assert canOpen(area_doors["FoyerR"]) in loadout
