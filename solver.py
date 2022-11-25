from connection_data import SunkenNestL
from game import Game
from item_data import Items
from loadout import Loadout
from location_data import spacePortLocs
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


def solve(game: Game) -> tuple[bool, list[str]]:
    """ returns (whether completable, spoiler lines) """
    for loc in game.all_locations:
        loc['inlogic'] = False

    unused_locations = game.all_locations.copy()
    used_locs: set[str] = set()

    loadout = Loadout(game)

    log_lines = [" - spaceport -"]
    # this loop just for spaceport
    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        log_lines.append("sphere:")
        updateAreaLogic(loadout)
        updateLogic(unused_locations, loadout)
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
        print("solver: couldn't get out of spaceport")
        for loc in unused_locations:
            if loc['inlogic'] and loc['fullitemname'] not in spacePortLocs:
                print("solver: found another way out of spaceport besides Ridley")
                print(loadout)
                print("but logic doesn't support that yet")
        return False, log_lines
    loadout.append(Items.spaceDrop)
    loadout.append(SunkenNestL)  # assuming this is where we land
    log_lines.append(" - fall from spaceport -")

    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        log_lines.append("sphere:")
        updateAreaLogic(loadout)
        updateLogic(unused_locations, loadout)
        for loc in unused_locations:
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

    return len(unused_locations) == 0, log_lines
