from subversion_rando.game import GameOptions
from subversion_rando.main_generation import generate


def test_default_generate() -> None:
    """ without writing to disk """
    generate(GameOptions(frozenset(), False, "D", True))
