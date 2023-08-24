from pathlib import Path
import random
try:  # Literal 3.8
    from typing import Literal, Optional, Type
except ImportError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
import time

try:  # container type annotations 3.9
    from .connection_data import SunkenNestL, VanillaAreas, area_doors, misc_doors
except TypeError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
from .daphne_gate import get_daphne_gate, get_air_lock_bytes
from .fillForward import fill_major_minor
from .fillInterface import FillAlgorithm
from .game import CypherItems, Game, GameOptions
from .hints import choose_hint_location, get_hint_spoiler_text, write_hint_to_rom
from .item_data import Item, Items
from .loadout import Loadout
from .location_data import Location, pullCSV, spacePortLocs
from .logic_presets import casual, expert, medium
from . import logic_updater
from . import fillMedium
from . import fillMajorMinor
from . import fillAssumed
from . import fillSpeedrun
from . import areaRando
from .new_terrain_writer import TerrainWriter
from .romWriter import RomWriter
from .solver import hard_required_locations, required_tricks, solve, spoil_play_through
from .spaceport_door_data import shrink_spaceport, spaceport_doors
from .terrain_patch import subterranean
from .trick import Trick
from .trick_data import Tricks

ORIGINAL_ROM_NAME = "Subversion12.sfc"


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
    """ if generation fails, game.hint_data will be None """
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
    start_time = time.perf_counter()
    game = Game(options,
                all_locations,
                VanillaAreas(),
                seeeed)
    while not seedComplete :
        if game.options.daphne_gate:
            daphne_blocks = get_daphne_gate(game.options)
            game.daphne_blocks = daphne_blocks

        if game.options.area_rando:  # area rando
            force_normal_early = (
                (
                    Tricks.movement_moderate not in game.options.logic or
                    Tricks.wave_gate_glitch not in game.options.logic
                ) and game.options.fill_choice == "MM"
            )
            game.connections = areaRando.RandomizeAreas(force_normal_early)
            # print(Connections) #test
        if time.perf_counter() - start_time > 70:
            print(f"Giving up after {randomizeAttempts} attempts. Help?")
            return game
        randomizeAttempts += 1
        print("Starting randomization attempt:", randomizeAttempts)
        game.item_placement_spoiler = f"Starting randomization attempt: {randomizeAttempts}\n"
        # now start randomizing
        if options.fill_choice in {"D", "B", "MM"}:
            if options.fill_choice == "MM" and randomizeAttempts > 15:
                seedComplete = fill_major_minor(game)
            else:
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


def resolve_one_up_if_needed(rel_dir: Path, file_check: Optional[str] = None) -> Path:
    """
    looks for `rel_dir` either in the current working directory or in the parent (..)

    If `file_check` is given, it will also require that file to be in that directory.

    returns the relative directory found

    raises `FileNotFoundError` if not found
    """
    if rel_dir.exists() and (
        file_check is None or rel_dir.joinpath(file_check).exists()
    ):
        return rel_dir

    up_one = Path("..").joinpath(rel_dir)
    if up_one.exists() and (
        file_check is None or up_one.joinpath(file_check).exists()
    ):
        return up_one

    raise FileNotFoundError(f"can't find: {rel_dir if file_check is None else rel_dir.joinpath(file_check)}")


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

    roms_path = resolve_one_up_if_needed(Path("roms"), ORIGINAL_ROM_NAME)
    rom_name = f"Sub{logicChoice}{game.options.fill_choice}{areaA}{game.seed}.sfc"
    rom1_path = roms_path.joinpath(rom_name)
    rom_clean_path = roms_path.joinpath(ORIGINAL_ROM_NAME)

    if romWriter is None:
        romWriter = RomWriter.fromFilePaths(origRomPath=rom_clean_path)
    else :
        # remove .sfc extension and dirs
        romWriter.setBaseFilename(rom1_path.stem)
        # This is untested, currently not used for anything.
        # (all calls to `write_rom` give no `romWriter`)

    if game.hint_data:
        hint_loc_name, hint_loc_marker = game.hint_data
        write_hint_to_rom(hint_loc_name, hint_loc_marker, romWriter)

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

    tw = TerrainWriter(romWriter)

    tw.write(subterranean, [0x7dac7, 0x7daad])

    if game.options.daphne_gate:
        wrecked_bytes, non_default_bytes, default_bytes = get_air_lock_bytes(game.daphne_blocks)
        tw.write(non_default_bytes, [0x7eb2d])
        tw.write(default_bytes, [0x7eb13])
        tw.write(wrecked_bytes, [0x782ab, 0x782c5])

        # harder to go left through speed blocks
        if (game.daphne_blocks.one == "Speed" and not (  # speed on top
            # horizontal shinespark from broken platform before door
            Tricks.short_charge_2 in game.options.logic and
            Tricks.movement_moderate in game.options.logic
        )) or (game.daphne_blocks.two == "Speed" and not (  # speed on bottom
            # mockball over broken platform before door
            Tricks.short_charge_3 in game.options.logic and
            Tricks.mockball_hard in game.options.logic
        )):
            romWriter.connect_doors(misc_doors["WreckedCrewQuartersAccessL"], misc_doors["RockyRidgeR"], one_way=True)

    # lower the water slightly in norak brook, to get up without aqua suit
    # (because it's too easy to go down without thinking about it)
    # This is the lower byte of "Base Y position"
    # in the FX (18ea0) of the State Headers of Norak Brook (8be5)
    romWriter.writeBytes(0x18ea2, b'\xbb')  # changed from a7

    # rotate save files
    romWriter.writeBytes(
        0xff60,          # some empty space
        b'\xad\x52\x09'  # lda $0952  # save slot
        b'\xc9\x02\x00'  # cmp #$0002
        b'\x30\x03'      # bmi 03
        b'\xa9\xff\xff'  # lda #$ffff
        b'\x1a'          # inc
        b'\x8d\x52\x09'  # sta $0952
        b'\x4c\x35\xef'  # jmp $ef35  # the place where 818000 originally jumped to
    )
    romWriter.writeBytes(
        0x8000,          # save code
        b'\x4c\x60\xff'  # jmp that code above  (changed from jmp $ef35)
    )

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

    return rom_name


def get_spoiler(game: Game) -> str:
    """ the text in the spoiler file """

    spoilerSave = game.item_placement_spoiler + '\n'

    # add area transitions to spoiler
    if game.options.area_rando:
        for door1, door2 in game.connections:
            spoilerSave += f"{door1.area_name} {door1.name} << >> {door2.area_name} {door2.name}\n"
        spoilerSave += "\n"
        spoilerSave += " --- possible escape path ---\n"
        path = areaRando.escape_path(game.connections)
        if path is None:
            spoilerSave += "path error\n"
        else:
            for door in path:
                spoilerSave += f"  {door}\n"

    if game.hint_data:
        hint_loc_name, hint_loc_marker = game.hint_data
        spoilerSave += get_hint_spoiler_text(hint_loc_name, hint_loc_marker)

    _completable, play_through, _locs = solve(game)
    solve_lines = spoil_play_through(play_through)

    s = f"RNG Seed: {game.seed}\n\n"
    s += "\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n"
    s += spoilerSave
    s += '\n\n'
    for solve_line in solve_lines:
        s += solve_line + '\n'
    s += '\n\n'
    s += required_locations_spoiler(game)
    s += '\n'
    s += daphne_gate_spoiler(game)
    s += '\n'
    s += required_tricks_spoiler(game)
    s += '\n'
    s += logic_tricks_spoiler(game)
    s += '\n'

    return s


def write_spoiler_file(game: Game, rom_name: str) -> None:
    text = get_spoiler(game)
    spoiler_dir = resolve_one_up_if_needed(Path("spoilers"))
    spoiler_file_name = f"{rom_name}.spoiler.txt"
    spoiler_path = spoiler_dir.joinpath(spoiler_file_name)
    with open(spoiler_path, "w") as spoiler_file:
        spoiler_file.write(text)
    print(f"Spoiler file is {spoiler_path}")


def required_locations_spoiler(game: Game) -> str:
    spoiler_text = "hard required locations:\n"
    req_locs, _ = hard_required_locations(game)
    for loc_name in req_locs:
        item = game.all_locations[loc_name]['item']
        item_name = item[0] if item else "Nothing"
        spoiler_text += f"  {loc_name}  --  {item_name}\n"
    return spoiler_text


def daphne_gate_spoiler(game: Game) -> str:
    return f"wrecked daphne gate requires: {game.daphne_blocks.one} or {game.daphne_blocks.two}\n"


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

    if game.options.cypher_items == CypherItems.SmallAmmo and game.options.fill_choice != "MM":
        game.all_locations["Shrine Of The Animate Spark"]["item"] = Items.SmallAmmo
        game.all_locations["Enervation Chamber"]["item"] = Items.SmallAmmo
        fill_algorithm.extra_items.remove(Items.SmallAmmo)
        fill_algorithm.extra_items.remove(Items.SmallAmmo)
        game.item_placement_spoiler += f"Shrine Of The Animate Spark - - - {Items.SmallAmmo[0]}\n"
        game.item_placement_spoiler += f"Enervation Chamber - - - {Items.SmallAmmo[0]}\n"

    if game.options.fill_choice == "MM":  # major/minor
        first, second = Items.Missile, Items.GravityBoots
        if Tricks.wave_gate_glitch in game.options.logic and random.random() < 0.5:
            first, second = second, first
        game.all_locations["Torpedo Bay"]["item"] = first
        game.all_locations["Subterranean Burrow"]["item"] = second
        fill_algorithm.prog_items.remove(first)
        fill_algorithm.prog_items.remove(second)
        game.item_placement_spoiler += f"Torpedo Bay - - - {first[0]}\n"
        game.item_placement_spoiler += f"Subterranean Burrow - - - {second[0]}\n"

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
        # if placeItem in {Items.Morph, Items.Bombs, Items.Speedball, Items.PowerBomb}:
        #     print(f"DEBUG: placing {placeItem[0]} in {placeLocation['fullitemname']}")
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
