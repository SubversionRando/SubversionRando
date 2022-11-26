import random
import sys
from typing import Literal, Optional, Type
import argparse

from connection_data import SunkenNestL, VanillaAreas
from fillInterface import FillAlgorithm
from game import Game
from item_data import Item, Items
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logicCasual import Casual
from logicExpert import Expert
import logic_updater
import fillMedium
import fillMajorMinor
import fillAssumed
import fillSpeedrun
import areaRando
from romWriter import RomWriter
from solver import solve


def commandLineArgs(sys_args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--casual', action="store_true",
                        help='Casual logic, easy setting matching the vanilla Subversion experience, Default')
    parser.add_argument('-e', '--expert', action="store_true",
                        help='Expert logic, hard setting comparable to Varia.run Expert difficulty')

    parser.add_argument('-s', '--speedrun', action="store_true",
                        help='Speedrun fill, fast setting comparable to Varia.run Speedrun fill algorithm, Default')
    parser.add_argument('-d', '--assumedfill', action="store_true",
                        help='Assumed fill, standard slower progression fill algorithm')
    parser.add_argument(
        '-m', '--medium', action="store_true",
        help='Medium fill, medium speed setting that places low-power items first for increased exploration'
    )
    parser.add_argument('-mm', '--majorminor', action="store_true",
                        help='Major-Minor fill, using unique majors and locations')

    parser.add_argument('-a', '--area', action="store_true",
                        help='Area rando shuffles major areas of the game, expert logic only')
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


# main program
def Main(argv: list[str], romWriter: Optional[RomWriter] = None) -> None:
    workingArgs = commandLineArgs(argv[1:])

    logicChoice: Literal["E", "C"]
    if workingArgs.expert :
        logicChoice = "E"
    else :
        logicChoice = "C"  # Default to casual logic

    fillChoice: Literal["M", "MM", "D", "S"]
    if workingArgs.medium :
        fillChoice = "M"
    elif workingArgs.majorminor :
        fillChoice = "MM"
    elif workingArgs.assumedfill :
        fillChoice = "D"
    else :
        fillChoice = "S"
    areaA = ""
    if workingArgs.area :
        areaA = "A"
        if fillChoice == "MM" :
            fillChoice = "M"
            print("Cannot use Major-Minor in Area rando currently. Using medium instead.")

    # hudFlicker=""
    # while hudFlicker != "Y" and hudFlicker != "N" :
    #     hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #     hudFlicker = hudFlicker.title()
    seeeed = random.randint(1000000, 9999999)
    random.seed(seeeed)
    rom_name = f"Sub{logicChoice}{fillChoice}{areaA}{seeeed}.sfc"
    rom1_path = f"roms/{rom_name}"
    rom_clean_path = "roms/Subversion12.sfc"
    # you must include Subversion 1.2 in your roms folder with this name^

    csvdict = pullCSV()
    locArray = list(csvdict.values())

    if romWriter is None :
        romWriter = RomWriter.fromFilePaths(
            origRomPath=rom_clean_path, newRomPath=rom1_path)
    else :
        # remove .sfc extension and dirs
        romWriter.setBaseFilename(rom1_path[:-4].split("/")[-1])

    spoilerSave = ""
    seedComplete = False
    randomizeAttempts = 0
    game = Game(Expert if logicChoice == "E" else Casual,
                list(csvdict.values()),
                areaA == "A",
                VanillaAreas())
    while not seedComplete :
        if game.area_rando:  # area rando
            game.connections = areaRando.RandomizeAreas()
            # print(Connections) #test
        randomizeAttempts += 1
        if randomizeAttempts > 1000 :
            print("Giving up after 1000 attempts. Help?")
            break
        print("Starting randomization attempt:", randomizeAttempts)
        spoilerSave = ""
        spoilerSave += f"Starting randomization attempt: {randomizeAttempts}\n"
        # now start randomizing
        if fillChoice == "D":
            seedComplete, spoilerSave = assumed_fill(game, spoilerSave)
        else:
            seedComplete, spoilerSave = forward_fill(game, fillChoice, spoilerSave)

    # add area transitions to spoiler
    if game.area_rando:
        for item in game.connections:
            spoilerSave += f"{item[0][2]} {item[0][3]} << >> {item[1][2]} {item[1][3]}\n"

    _got_all, solve_lines, _locs = solve(game)

    if game.area_rando:
        areaRando.write_area_doors(game.connections, romWriter)
    # write all items into their locations
    for loc in locArray:
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
    romWriter.finalizeRom()
    print("Done!")
    print(f"Filename is {rom_name}")
    with open(f"spoilers/{rom_name}.spoiler.txt", "w") as spoiler_file:
        spoiler_file.write(f"RNG Seed: {seeeed}\n\n")
        spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
        spoiler_file.write(spoilerSave)
        spoiler_file.write('\n\n')
        for solve_line in solve_lines:
            spoiler_file.write(solve_line + '\n')
    print(f"Spoiler file is spoilers/{rom_name}.spoiler.txt")


def assumed_fill(game: Game, spoilerSave: str) -> tuple[bool, str]:
    for loc in game.all_locations:
        loc["item"] = None
    dummy_locations: list[Location] = []
    loadout = Loadout(game)
    fill_algorithm = fillAssumed.FillAssumed(game.connections)
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
            spoilerSave += f'{message}\n'
            break
        placeLocation, placeItem = placePair
        placeLocation["item"] = placeItem
        spoilerSave += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"

        if fill_algorithm.count_items_remaining() == 0:
            # Normally, assumed fill will always make a valid playthrough,
            # but dropping from spaceport can mess that up,
            # so it needs to be checked again.
            completable, _, _ = solve(game)
            if completable:
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
            return completable, spoilerSave

    return False, spoilerSave


def forward_fill(game: Game,
                 fillChoice: Literal["M", "S", "MM"],
                 spoilerSave: str) -> tuple[bool, str]:
    unusedLocations : list[Location] = []
    unusedLocations.extend(game.all_locations)
    availableLocations: list[Location] = []
    # visitedLocations = []
    loadout = Loadout(game)
    loadout.append(SunkenNestL)  # starting area
    # use appropriate fill algorithm for initializing item lists
    fill_algorithm = fillers[fillChoice](game.connections)
    while len(unusedLocations) != 0 or len(availableLocations) != 0:
        # print("loadout contains:")
        # print(loadout)
        # for a in loadout:
        #     print("-",a[0])
        # update logic by updating unusedLocations
        # using helper function, modular for more logic options later
        # unusedLocations[i]['inlogic'] holds the True or False for logic
        logic_updater.updateAreaLogic(loadout)
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
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            # for i in loadout:
            #     print(i[0])
            # for u in unusedLocations :
            #     print("--",u['fullitemname'])

            break

        placePair = fill_algorithm.choose_placement(availableLocations, loadout)
        if placePair is None:
            print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
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
        spoilerSave += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"
        # print(placeLocation['fullitemname']+placeItem[0])

        if availableLocations == [] and unusedLocations == [] :
            print("Item placements successful.")
            spoilerSave += "Item placements successful.\n"
            return True, spoilerSave
    return False, spoilerSave


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")
