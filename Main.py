import random
import sys
try:  # Literal 3.8
    from typing import Literal, Optional, Type
except ImportError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
import argparse

try:  # container type annotations 3.9
    from connection_data import SunkenNestL, VanillaAreas, area_doors, misc_doors
except TypeError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
from fillInterface import FillAlgorithm
from game import CypherItems, Game, GameOptions
from hints import choose_hint_location, get_hint_spoiler_text, write_hint_to_rom
from item_data import Item, Items
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logic_presets import casual, expert, medium
import logic_updater
import fillMedium
import fillMajorMinor
import fillAssumed
import fillSpeedrun
import areaRando
from romWriter import RomWriter
from solver import hard_required_locations, required_tricks, solve, spoil_play_through
from spaceport_door_data import shrink_spaceport, spaceport_doors
from terrain_patch import subterranean
from trick import Trick
from trick_data import Tricks


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
    args = parser.parse_args(sys_args)
    # print(args)
    return args


def plmidFromHiddenness(itemArray: Item, hiddenness: str) -> bytes:
    if hiddenness == "open":
        plmid = itemArray[1]
    elif hiddenness == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    return plmid


def write_location(romWriter: RomWriter, location: Location) -> None:
    """
    provide a location with an ['item'] value, such as Missile, Super, etc
    write all rom locations associated with the item location
    """
    item = location["item"]
    assert item, f"{location['fullitemname']} didn't get an item"
    # TODO: support locations with no items?
    plmid = plmidFromHiddenness(item, location['hiddenness'])
    for address in location['locids']:
        romWriter.writeItem(address, plmid, item[4])
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness
            # as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(item, location['alternateroomdifferenthiddenness'])
        romWriter.writeItem(address, plmid_altroom, item[4])


fillers: dict[str, Type[FillAlgorithm]] = {
    "M": fillMedium.FillMedium,
    "MM": fillMajorMinor.FillMajorMinor,
    "S": fillSpeedrun.FillSpeedrun,
    "AF": fillAssumed.FillAssumed,
}

logics: dict[Literal["E", "U", "C", "Q"], frozenset[Trick]] = {
    "E": expert,
    "U": medium,
    "C": casual,
}


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
        if fillChoice == "MM":
            fillChoice = "D"
            print("Cannot use Major-Minor in Area rando currently. Using assumed fill instead.")

    small_spaceport = False
    if workingArgs.smallspaceport:
        small_spaceport = True

    escape_shortcuts = False
    if workingArgs.escapeshortcuts:
        escape_shortcuts = True

    options = GameOptions(logic, area_rando, fillChoice, small_spaceport, escape_shortcuts, CypherItems.NotRequired)
    game = generate(options)
    write_rom(game)


def verify_cypher_not_required(seedComplete: bool, game: Game) -> bool:
    saved_animate = game.all_locations["Shrine Of The Animate Spark"]["item"]
    saved_enervation = game.all_locations["Enervation Chamber"]["item"]
    game.all_locations["Shrine Of The Animate Spark"]["item"] = None
    game.all_locations["Enervation Chamber"]["item"] = None
    completable, _, _ = solve(game)
    game.all_locations["Shrine Of The Animate Spark"]["item"] = saved_animate
    game.all_locations["Enervation Chamber"]["item"] = saved_enervation
    if not completable:
        print("cypher requirement missing")
    return seedComplete and completable


def generate(options: GameOptions) -> Game:
    # hudFlicker=""
    # while hudFlicker != "Y" and hudFlicker != "N" :
    #     hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #     hudFlicker = hudFlicker.title()
    seeeed = random.randint(1000000, 9999999)
    random.seed(seeeed)
    # you must include Subversion 1.2 in your roms folder with this name^

    all_locations = pullCSV()

    seedComplete = False
    randomizeAttempts = 0
    game = Game(options,
                all_locations,
                VanillaAreas(),
                seeeed)
    while not seedComplete :
        if game.options.area_rando:  # area rando
            game.connections = areaRando.RandomizeAreas()
            # print(Connections) #test
        randomizeAttempts += 1
        if randomizeAttempts > 1000 :
            print("Giving up after 1000 attempts. Help?")
            break
        print("Starting randomization attempt:", randomizeAttempts)
        game.item_placement_spoiler = f"Starting randomization attempt: {randomizeAttempts}\n"
        # now start randomizing
        if options.fill_choice in {"D", "B"}:
            seedComplete = assumed_fill(game)
        else:
            seedComplete = forward_fill(game)

        if game.options.cypher_items == CypherItems.NotRequired:
            seedComplete = verify_cypher_not_required(seedComplete, game)

    # make this optional?
    # If someone doesn't want hints, they can just not look at the log.
    # That doesn't work for competitive play,
    # but we can handle that if people start playing this competitively and want no hints.
    choose_hint_location(game)

    return game


def write_rom(game: Game, romWriter: Optional[RomWriter] = None) -> str:
    logicChoice: Literal["E", "U", "C", "Q"] = "Q"
    if game.options.logic == casual:
        logicChoice = "C"
    elif game.options.logic == medium:
        logicChoice = "U"
    elif game.options.logic == expert:
        logicChoice = "E"

    areaA = ""
    if game.options.area_rando:
        areaA = "A"

    rom_name = f"Sub{logicChoice}{game.options.fill_choice}{areaA}{game.seed}.sfc"
    rom1_path = f"roms/{rom_name}"
    rom_clean_path = "roms/Subversion12.sfc"

    if romWriter is None :
        romWriter = RomWriter.fromFilePaths(origRomPath=rom_clean_path)
    else :
        # remove .sfc extension and dirs
        romWriter.setBaseFilename(rom1_path[:-4].split("/")[-1])

    spoilerSave = game.item_placement_spoiler + '\n'

    # add area transitions to spoiler
    if game.options.area_rando:
        for door1, door2 in game.connections:
            spoilerSave += f"{door1.area_name} {door1.name} << >> {door2.area_name} {door2.name}\n"

    _completable, play_through, _locs = solve(game)
    solve_lines = spoil_play_through(play_through)

    if game.hint_data:
        hint_loc_name, hint_loc_marker = game.hint_data
        write_hint_to_rom(hint_loc_name, hint_loc_marker, romWriter)
        spoilerSave += get_hint_spoiler_text(hint_loc_name, hint_loc_marker)

    if game.options.area_rando:
        areaRando.write_area_doors(game.connections, romWriter)
    # write all items into their locations
    for loc in game.all_locations.values():
        write_location(romWriter, loc)

    # Suit animation skip patch
    romWriter.writeBytes(0x20717, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    # if hudFlicker == "Y" :
    #     writeBytes(0x547a, b"\x02")
    #     writeBytes(0x547f, b"\x00")
    # Morph Ball PLM patch (chozo, hidden)
    romWriter.writeBytes(0x268ce, b"\x04")
    romWriter.writeBytes(0x26e02, b"\x04")
    # skip intro (asm edits) TODO turn this into asm and a proper hook
    romWriter.writeBytes(0x16eda, b"\x1f")  # initial game state set by $82:eeda
    romWriter.writeBytes(0x16ee0, b"\x06\x00")  # initial game area = 6 (ceres)
    romWriter.writeBytes(0x16ee3, b"\x9f\x07")  # $079f Area index
    romWriter.writeBytes(0x16ee5, b"\xa9\x05\x00\x8f\x14\xd9\x7e\xea\xea")  # $7e:d914 = 05 Main
    romWriter.writeBytes(0x16eee, b"\xad\x52\x09\x22\x00\x80\x81")  # jsl save game (param in A: save slot)
    romWriter.writeBytes(0x16ed0, b"\x24")  # adjust earlier branch to go +6 bytes later to rts
    romWriter.writeBytes(0x16ed8, b"\x1c")  # adjust earlier branch to go +6 bytes later to rts
    # disable demos (asm opcode edit). because the demos show items
    romWriter.writeBytes(0x59f29, b"\xad")
    # make always flashing doors out of vanilla gray 'animals saved' doors:
    #   edit in function $84:BE30 'gray door pre: go to link instruction if critters escaped',
    #   which is vanilla and probably not used anyway
    #   use by writing 0x18 to the high byte of a gray door plm param, OR'ed with the low bit of the 9-low-bits id part
    romWriter.writeBytes(0x23e33, b"\x38\x38\x38\x38")  # set the carry bit (a lot)

    # subterranean burrow terrain
    romWriter.writeBytes(0x2f51c4, subterranean)
    p_level_data = b'\xc4\xd1\xde'  # ded1c4
    romWriter.writeBytes(0x7dac7, p_level_data)
    romWriter.writeBytes(0x7daad, p_level_data)

    if game.options.small_spaceport:
        romWriter.writeBytes(0x106283, b'\x71\x01')  # zebetite health
        romWriter.writeBytes(0x204b3, b'\x08')  # fake zebetite hits taken
        shrink_spaceport(romWriter)

    if game.options.escape_shortcuts:
        romWriter.connect_doors(spaceport_doors['BridgeL'], spaceport_doors['StationCorridorBR'], one_way=True)
        if not game.options.area_rando:
            romWriter.connect_doors(misc_doors["AuroraUnitWreckageL"], area_doors["CraterR"], one_way=True)

    romWriter.finalizeRom(rom1_path)

    print("Done!")
    print(f"Filename is {rom_name}")
    with open(f"spoilers/{rom_name}.spoiler.txt", "w") as spoiler_file:
        spoiler_file.write(f"RNG Seed: {game.seed}\n\n")
        spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
        spoiler_file.write(spoilerSave)
        spoiler_file.write('\n\n')
        for solve_line in solve_lines:
            spoiler_file.write(solve_line + '\n')
        spoiler_file.write('\n\n')
        spoiler_file.write(required_locations_spoiler(game))
        spoiler_file.write('\n')
        spoiler_file.write(required_tricks_spoiler(game))
        spoiler_file.write('\n')
        spoiler_file.write(logic_tricks_spoiler(game))
        spoiler_file.write('\n')
    print(f"Spoiler file is spoilers/{rom_name}.spoiler.txt")

    return rom_name


def required_locations_spoiler(game: Game) -> str:
    spoiler_text = "hard required locations:\n"
    req_locs, _ = hard_required_locations(game)
    for loc_name in req_locs:
        item = game.all_locations[loc_name]['item']
        item_name = item[0] if item else "Nothing"
        spoiler_text += f"  {loc_name}  --  {item_name}\n"
    return spoiler_text


def required_tricks_spoiler(game: Game) -> str:
    for_win, for_locs = required_tricks(game)
    spoiler_text = "tricks required to win:\n"
    for trick_name in for_win:
        spoiler_text += f"  {trick_name}\n"
    spoiler_text += "\ntricks required to reach all locations:\n"
    for trick_name in for_locs:
        spoiler_text += f"  {trick_name}\n"
    return spoiler_text


def logic_tricks_spoiler(game: Game) -> str:
    spoiler_text = "tricks allowed in this logic:\n"
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick) and trick in game.options.logic:
            spoiler_text += f'    "{trick_name}",\n'
    return spoiler_text


def assumed_fill(game: Game) -> bool:
    for loc in game.all_locations.values():
        loc["item"] = None
    dummy_locations: list[Location] = []
    loadout = Loadout(game)
    fill_algorithm = fillAssumed.FillAssumed(game.connections)

    if game.options.cypher_items == CypherItems.SmallAmmo:
        game.all_locations["Shrine Of The Animate Spark"]["item"] = Items.SmallAmmo
        game.all_locations["Enervation Chamber"]["item"] = Items.SmallAmmo
        fill_algorithm.extra_items.remove(Items.SmallAmmo)
        fill_algorithm.extra_items.remove(Items.SmallAmmo)

    n_items_to_place = fill_algorithm.count_items_remaining()
    assert n_items_to_place <= len(game.all_locations), \
        f"{n_items_to_place} items to put in {len(game.all_locations)} locations"
    print(f"{fill_algorithm.count_items_remaining()} items to place")
    while fill_algorithm.count_items_remaining():
        placePair = fill_algorithm.choose_placement(dummy_locations, loadout)
        if placePair is None:
            message = ('Item placement was not successful in assumed. '
                       f'{fill_algorithm.count_items_remaining()} items remaining.')
            print(message)
            game.item_placement_spoiler += f'{message}\n'
            break
        placeLocation, placeItem = placePair
        placeLocation["item"] = placeItem
        game.item_placement_spoiler += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"

        if fill_algorithm.count_items_remaining() == 0:
            # Normally, assumed fill will always make a valid playthrough,
            # but dropping from spaceport can mess that up,
            # so it needs to be checked again.
            completable, _, accessible_locations = solve(game)
            done = completable and len(accessible_locations) == len(game.all_locations)
            if done:
                print("Item placements successful.")
                game.item_placement_spoiler += "Item placements successful.\n"
            return done

    return False


def forward_fill(game: Game) -> bool:
    unusedLocations : list[Location] = []
    unusedLocations.extend(game.all_locations.values())
    availableLocations: list[Location] = []
    # visitedLocations = []
    loadout = Loadout(game)
    loadout.append(SunkenNestL)  # starting area
    # use appropriate fill algorithm for initializing item lists
    fill_algorithm = fillers[game.options.fill_choice](game.connections)
    while len(unusedLocations) != 0 or len(availableLocations) != 0:
        # print("loadout contains:")
        # print(loadout)
        # for a in loadout:
        #     print("-",a[0])
        # update logic by updating unusedLocations
        # using helper function, modular for more logic options later
        # unusedLocations[i]['inlogic'] holds the True or False for logic
        logic_updater.updateLogic(unusedLocations, loadout)

        # update unusedLocations and availableLocations
        for i in reversed(range(len(unusedLocations))):  # iterate in reverse so we can remove freely
            if unusedLocations[i]['inlogic'] is True:
                # print("Found available location at",unusedLocations[i]['fullitemname'])
                availableLocations.append(unusedLocations[i])
                unusedLocations.pop(i)
        # print("Available locations sits at:",len(availableLocations))
        # for al in availableLocations :
        #     print(al[0])
        # print("Unused locations sits at size:",len(unusedLocations))
        # print("unusedLocations:")
        # for u in unusedLocations :
        #     print(u['fullitemname'])

        if availableLocations == [] and unusedLocations != [] :
            print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
            game.item_placement_spoiler += \
                f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            # for i in loadout:
            #     print(i[0])
            # for u in unusedLocations :
            #     print("--",u['fullitemname'])

            break

        placePair = fill_algorithm.choose_placement(availableLocations, loadout)
        if placePair is None:
            print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
            game.item_placement_spoiler += \
                f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            break
        # it returns your location and item, which are handled here
        placeLocation, placeItem = placePair
        if (placeLocation in unusedLocations) :
            unusedLocations.remove(placeLocation)
        placeLocation["item"] = placeItem
        availableLocations.remove(placeLocation)
        fill_algorithm.remove_from_pool(placeItem)
        loadout.append(placeItem)
        if not ((placeLocation['fullitemname'] in spacePortLocs) or (Items.spaceDrop in loadout)):
            loadout.append(Items.spaceDrop)
        game.item_placement_spoiler += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"
        # print(placeLocation['fullitemname']+placeItem[0])

        if availableLocations == [] and unusedLocations == [] :
            print("Item placements successful.")
            game.item_placement_spoiler += "Item placements successful.\n"
            return True
    return False


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")
