from typing import Optional, cast

from connection_data import AreaDoor, SunkenNestL, area_doors
from game import Game
from item_data import Items
from loadout import Loadout
from location_data import Location, spacePortLocs
from logic_updater import updateAreaLogic, updateLogic

_progression_items = frozenset([
    Items.Missile,
    Items.Morph,
    Items.GravityBoots,
    Items.Super,
    Items.Grapple,
    Items.PowerBomb,
    Items.Speedball,
    Items.Bombs,
    Items.HiJump,
    Items.GravitySuit,
    Items.DarkVisor,
    Items.Wave,
    Items.SpeedBooster,
    Items.Spazer,
    Items.Varia,
    Items.Ice,
    Items.MetroidSuit,
    Items.Plasma,
    Items.Screw,
    Items.SpaceJump,
    Items.Charge,
    Items.Hypercharge,
    Items.Xray,
    Items.Energy
])


def solve(game: Game, starting_items: Optional[Loadout] = None) -> tuple[bool, list[str], list[Location]]:
    """ returns (whether completable, spoiler lines, accessible locations) """
    for loc in game.all_locations:
        loc['inlogic'] = False

    unused_locations = game.all_locations.copy()
    used_locs: set[str] = set()
    doors_accessed: set[AreaDoor] = set()

    loadout = Loadout(game, starting_items)

    log_lines = [" - spaceport -"]

    def check_for_new_area_doors() -> None:
        new_area_doors: list[str] = []
        for thing in loadout:
            if thing[3] in area_doors and thing not in doors_accessed:
                thing = cast(AreaDoor, thing)
                new_area_doors.append(thing[3])
                doors_accessed.add(thing)
        if len(new_area_doors):
            log_lines.append(f"  new area doors: {', '.join(new_area_doors)}")

    # this loop just for spaceport
    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        updateAreaLogic(loadout)
        check_for_new_area_doors()
        updateLogic(unused_locations, loadout)
        log_lines.append("sphere:")
        for loc in unused_locations:
            if loc['inlogic']:
                loc_name = loc['fullitemname']
                if loc_name not in spacePortLocs:
                    # debug
                    # print(f"found {loc_name} in logic while still in spaceport")
                    continue
                item = loc['item']
                if item:
                    loadout.append(item)
                    if item in _progression_items:
                        log_lines.append(f"    get {item[0]} from {loc_name}")
                used_locs.add(loc_name)
        # remove used locations
        unused_locations = [loc for loc in unused_locations if loc['fullitemname'] not in used_locs]
        stuck = len(loadout) == prev_loadout_count

    while "sphere:" in log_lines[-1]:
        log_lines.pop()

    if not game.logic.can_fall_from_spaceport(loadout):
        # print("solver: couldn't get out of spaceport")
        # for loc in unused_locations:
        #     if loc['inlogic'] and loc['fullitemname'] not in spacePortLocs:
        #         print("solver: found another way out of spaceport besides Ridley")
        #         print(loadout)
        #         print("but logic doesn't support that yet")
        return False, log_lines, [loc for loc in game.all_locations if loc["fullitemname"] in used_locs]
    loadout.append(Items.spaceDrop)
    loadout.append(SunkenNestL)  # assuming this is where we land
    log_lines.append(" - fall from spaceport -")

    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        updateAreaLogic(loadout)
        check_for_new_area_doors()
        updateLogic(unused_locations, loadout)
        log_lines.append("sphere:")
        for loc in unused_locations:
            # special case: major/minor can put missiles or grav boots in sandy cache even though it's not in logic
            if loc['fullitemname'] == "Sandy Cache" and loc['item'] in {
                Items.GravityBoots, Items.Missile
            }:
                loc['inlogic'] = True
            if loc['inlogic']:
                loc_name = loc['fullitemname']
                item = loc['item']
                if item:
                    loadout.append(item)
                    if item in _progression_items:
                        log_lines.append(f"    get {item[0]} from {loc_name}")
                used_locs.add(loc_name)
        # remove used locations
        unused_locations = [loc for loc in unused_locations if loc['fullitemname'] not in used_locs]
        stuck = len(loadout) == prev_loadout_count

    while "sphere:" in log_lines[-1]:
        log_lines.pop()

    # for line in log_lines:
    #     print(line)

    # note: the reason for making a new list from all_locations rather than used_locs,
    # is that used_locs is a `set`, so iterating through it is not deterministic, so seeds wouldn't be reproducible
    return (
        len(unused_locations) == 0,
        log_lines,
        [loc for loc in game.all_locations if loc["fullitemname"] in used_locs]
    )
