from subversion_rando.game import Exclude, GameOptions
from subversion_rando.item_marker import ItemMarkersOption
from subversion_rando.logic_presets import expert
from subversion_rando.main_generation import generate, get_spoiler, write_rom
from subversion_rando.romWriter import RomWriter


def test_default_generate() -> None:
    """ without writing to disk """
    game = generate(GameOptions(frozenset(), False, "D", True))
    rw = RomWriter.fromBlankIps()
    write_rom(game, rw)  # doesn't write a file if it's IPS
    rw.getFinalIps()  # returns bytearray
    get_spoiler(game)  # returns str


def test_some_other_options() -> None:
    options = GameOptions(
        expert,
        area_rando=True,
        fill_choice="B",
        small_spaceport=False,
        escape_shortcuts=True,
        exclude=Exclude.blitz,
        daphne_gate=True,
        item_markers=ItemMarkersOption.ThreeTiered,
        objective_rando=3,
    )
    game = generate(options)
    rw = RomWriter.fromBlankIps()
    write_rom(game, rw)  # doesn't write a file if it's IPS
    rw.getFinalIps()  # returns bytearray
    get_spoiler(game)  # returns str
