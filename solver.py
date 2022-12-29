from typing import Optional

from connection_data import AreaDoor, SunkenNestL
from game import Game
from item_data import Items
from loadout import Loadout
from location_data import Location, spacePortLocs
from logicCommon import ammo_req, energy_req
from logic_shortcut_data import can_fall_from_spaceport, can_win
from logic_updater import updateLogic
from trick import Trick
from trick_data import Tricks

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
    Items.Energy,
    Items.SmallAmmo,
    Items.LargeAmmo,
])


def solve(game: Game, starting_items: Optional[Loadout] = None) -> tuple[bool, list[str], list[Location]]:
    """ returns (whether completable, spoiler lines, accessible locations) """
    for loc in game.all_locations.values():
        loc['inlogic'] = False

    unused_locations = list(game.all_locations.values())
    used_locs: set[str] = set()
    doors_accessed: set[AreaDoor] = set()

    loadout = Loadout(game, starting_items)

    log_lines = [" - spaceport -"]

    def check_for_new_area_doors() -> None:
        new_area_doors: list[str] = []
        for thing in loadout:
            if isinstance(thing, AreaDoor) and thing not in doors_accessed:
                new_area_doors.append(thing.name)
                doors_accessed.add(thing)
        if len(new_area_doors):
            log_lines.append(f"  new area doors: {', '.join(new_area_doors)}")

    # this loop just for spaceport
    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        updateLogic(unused_locations, loadout)
        check_for_new_area_doors()
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

    if can_fall_from_spaceport not in loadout:
        # print("solver: couldn't get out of spaceport")
        # for loc in unused_locations:
        #     if loc['inlogic'] and loc['fullitemname'] not in spacePortLocs:
        #         print("solver: found another way out of spaceport besides Ridley")
        #         print(loadout)
        #         print("but logic doesn't support that yet")
        return False, log_lines, [loc for loc in game.all_locations.values() if loc["fullitemname"] in used_locs]
    loadout.append(Items.spaceDrop)
    loadout.append(SunkenNestL)  # assuming this is where we land
    log_lines.append(" - fall from spaceport -")

    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        updateLogic(unused_locations, loadout)
        check_for_new_area_doors()
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
                        # don't need to log more than 9 energy tanks or more than 100 ammo
                        if not (
                            (item == Items.Energy and energy_req(1000) in loadout) or
                            (item in (Items.SmallAmmo, Items.LargeAmmo) and ammo_req(110) in loadout)
                        ):
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
        (can_win in loadout),
        # len(unused_locations) == 0,
        log_lines,
        [loc for loc in game.all_locations.values() if loc["fullitemname"] in used_locs]
    )


def hard_required_locations(game: Game) -> list[str]:
    """ list of names of hard required locations in progression order """
    completable, log_lines, _ = solve(game)
    if not completable:
        # not sure what I want to do with this function if I pass a game that isn't completable
        # maybe exception
        return []

    locations: list[str] = []
    for line in log_lines:
        if line.startswith("    get "):
            _beg, loc_name = line.split(" from ")
            locations.append(loc_name)

    log_locations = frozenset(locations)
    for loc in game.all_locations.values():
        if loc['fullitemname'] not in log_locations:
            locations.append(loc['fullitemname'])

    req_locs: list[str] = []
    for excluded_loc_name in locations:
        excluded_loc = game.all_locations[excluded_loc_name]
        saved_item = excluded_loc['item']
        excluded_loc['item'] = None
        completable, _, _ = solve(game)
        if not completable:
            req_locs.append(excluded_loc_name)
        excluded_loc['item'] = saved_item

    return req_locs


def _excluded_tricks(t: Trick) -> set[Trick]:
    """
    all of the tricks that should be excluded to exclude this trick

    "If you can't do the easier one, then you can't do the harder one."
    """
    data = {
        Tricks.hell_run_easy:
            {Tricks.hell_run_easy, Tricks.hell_run_medium, Tricks.hell_run_hard},
        Tricks.hell_run_medium:
            {Tricks.hell_run_medium, Tricks.hell_run_hard},

        Tricks.dark_easy:
            {Tricks.dark_easy, Tricks.dark_medium, Tricks.dark_hard},
        Tricks.dark_medium:
            {Tricks.dark_medium, Tricks.dark_hard},

        Tricks.movement_moderate:
            {Tricks.movement_moderate, Tricks.movement_zoast},

        Tricks.sbj_underwater_w_hjb:
            {Tricks.sbj_underwater_w_hjb, Tricks.sbj_underwater_no_hjb},

        Tricks.wall_jump_precise:
            {Tricks.wall_jump_precise, Tricks.wall_jump_delayed},

        Tricks.morph_jump_4_tile:
            {Tricks.morph_jump_4_tile, Tricks.morph_jump_3_tile},

        Tricks.crouch_or_downgrab:
            {Tricks.crouch_or_downgrab, Tricks.crouch_precise},

        Tricks.short_charge_2:
            {Tricks.short_charge_2, Tricks.short_charge_3, Tricks.short_charge_4}
    }
    if t in data:
        return data[t]
    return {t}


def obsoletes(t: str) -> set[str]:
    data = {
        "hell_run_hard": {"hell_run_medium", "hell_run_easy"},
        "hell_run_medium": {"hell_run_easy"},
        "dark_hard": {"dark_medium", "dark_easy"},
        "dark_medium": {"dark_easy"},
        "movement_zoast": {"movement_moderate"},
    }
    if t in data:
        return data[t]
    return set()


def required_tricks(game: Game) -> tuple[list[str], list[str]]:
    """ lists of names of (tricks required to win, tricks required to get all locations) """
    completable, _, _ = solve(game)
    if not completable:
        # not sure what I want to do with this function if I pass a game that isn't completable
        # maybe exception
        return [], []

    req_for_win: list[str] = []
    req_for_locs: list[str] = []
    all_tricks = {t: n for n, t in vars(Tricks).items() if isinstance(t, Trick)}
    tricks_allowed = game.logic
    for excluded_trick in tricks_allowed:
        game.logic = tricks_allowed - _excluded_tricks(excluded_trick)
        completable, _, locs = solve(game)
        if not completable:
            req_for_win.append(all_tricks[excluded_trick])
        if len(locs) != 122:
            req_for_locs.append(all_tricks[excluded_trick])

    obsoleted: set[str] = set()
    for trick_name in req_for_win:
        obsoleted.update(obsoletes(trick_name))
    req_for_win = [trick_name for trick_name in req_for_win if trick_name not in obsoleted]

    obsoleted = set()
    for trick_name in req_for_locs:
        obsoleted.update(obsoletes(trick_name))
    req_for_locs = [trick_name for trick_name in req_for_locs if trick_name not in obsoleted]

    return req_for_win, req_for_locs
