import sys
try:  # Literal 3.8
    from typing import Literal
except ImportError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
import argparse
import time

from subversion_rando.game import CypherItems, GameOptions
from subversion_rando.logic_presets import casual, expert, medium
from subversion_rando.main_generation import generate, write_rom, write_spoiler_file


def commandLineArgs(sys_args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--casual', action="store_true",
                        help='Casual logic, easy setting matching the vanilla Subversion experience, Default')
    parser.add_argument('-u', '--logicmedium', action="store_true",
                        help='Medium logic, medium setting between casual and expert')
    parser.add_argument('-e', '--expert', action="store_true",
                        help='Expert logic, hard setting comparable to Varia.run Expert difficulty')
    parser.add_argument('-q', '--logiccustom', action="store_true",
                        help='use the gui to customize logic')

    parser.add_argument('-s', '--speedrun', action="store_true",
                        help='Speedrun fill, fast setting comparable to Varia.run Speedrun fill algorithm')
    parser.add_argument('-d', '--assumedfill', action="store_true",
                        help='Assumed fill, standard slower progression fill algorithm, Default')
    parser.add_argument(
        '-m', '--medium', action="store_true",
        help='Medium fill, medium speed setting that places low-power items first for increased exploration'
    )
    parser.add_argument('-mm', '--majorminor', action="store_true",
                        help='Major-Minor fill, using unique majors and locations')
    parser.add_argument('-b', '--majorminorbias', action="store_true",
                        help='unique items have high probability to be in unique item locations')

    parser.add_argument('-a', '--area', action="store_true",
                        help='Area rando shuffles major areas of the game, expert logic only')

    parser.add_argument('-o', '--smallspaceport', action="store_true",
                        help='cuts out some parts of the space port to make it smaller')

    parser.add_argument('-r', '--escapeshortcuts', action="store_true",
                        help='shortens the escape paths - (final escape shortened only if not area rando)')

    parser.add_argument('--daphne_gate', action="store_true",
                        help='???')

    parser.add_argument('--open_escape', action="store_true",
                        help='Allows open access to the whole world during the final escape sequence')

    args = parser.parse_args(sys_args)
    # print(args)
    return args


# main program
def Main(argv: list[str]) -> None:
    """ generate from command line """
    workingArgs = commandLineArgs(argv[1:])

    logic = casual  # default
    if workingArgs.expert :
        logic = expert
    elif workingArgs.logicmedium:
        logic = medium

    fillChoice: Literal["M", "MM", "D", "S", "B"]
    if workingArgs.medium:
        fillChoice = "M"
    elif workingArgs.majorminor:
        fillChoice = "MM"
    elif workingArgs.speedrun:
        fillChoice = "S"
    elif workingArgs.majorminorbias:
        fillChoice = "B"
    else:
        fillChoice = "D"

    area_rando = False
    if workingArgs.area:
        area_rando = True
        # if fillChoice == "MM":
        #     fillChoice = "D"
        #     print("Cannot use Major-Minor in Area rando currently. Using assumed fill instead.")

    small_spaceport = False
    if workingArgs.smallspaceport:
        small_spaceport = True

    escape_shortcuts = False
    if workingArgs.escapeshortcuts:
        escape_shortcuts = True

    daphne_gate = False
    if workingArgs.daphne_gate:
        daphne_gate = True

    open_escape = False
    if workingArgs.open_escape:
        open_escape = True

    options = GameOptions(logic, area_rando, fillChoice, small_spaceport, escape_shortcuts, CypherItems.NotRequired, daphne_gate, open_escape)
    game = generate(options)
    rom_name = write_rom(game)
    write_spoiler_file(game, rom_name)


if __name__ == "__main__":
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")
