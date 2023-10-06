from subversion_rando.game import GameOptions
from subversion_rando.main_generation import generate, get_spoiler, write_rom
from subversion_rando.romWriter import RomWriter


def test_default_generate() -> None:
    """ without writing to disk """
    game = generate(GameOptions(frozenset(), False, "D", True))
    rw = RomWriter.fromBlankIps()
    write_rom(game, rw)  # doesn't write a file if it's IPS
    rw.getFinalIps()  # returns bytearray
    get_spoiler(game)  # returns str
