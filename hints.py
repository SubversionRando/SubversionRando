import random
from typing import Optional

from game import Game
from connection_data import area_doors
from item_data import Item, Items
from loadout import Loadout
from location_data import pullCSV
from logicCommon import varia_or_hell_run, can_bomb
from logic_area_shortcuts import SkyWorld, LifeTemple
from logic_locations import ruinedConcourseBDoorToEldersTop, greaterInferno, railAccess, norakToLifeTemple
from logic_shortcut import LogicShortcut
from logic_shortcut_data import can_crash_spaceport, pinkDoor, missileDamage, shootThroughWalls
from logic_updater import updateLogic
from romWriter import RomWriter
from solver import get_playthrough_locations, hard_required_locations, solve
from trick_data import Tricks


hint_data = {
    b'THE CHOZO HAVE A WEAKNESS IN': ("Torizo", 1, LogicShortcut(lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout)
    ))),
    b'BODY IS COVERED WITH A HARDENED': ("Botwoon", 2, LogicShortcut(lambda loadout: (
        (can_crash_spaceport in loadout) and (area_doors["OceanShoreR"] in loadout)
    ))),
    b'STURDY IN ORDER TO SURVIVE IN': ("Draygon", 4, LogicShortcut(lambda loadout: (
        (greaterInferno in loadout)
    ))),
    b'EXOSKELETON HAS BEEN MODIFIED USING SOME': ("Ridley", 4, LogicShortcut(lambda loadout: (
        (SkyWorld.killRidley in loadout) and
        (Items.Super in loadout) and
        (Items.GravityBoots in loadout) and
        (railAccess in loadout) and
        (SkyWorld.anticipation in loadout) and
        (varia_or_hell_run(90) in loadout)
    ))),
    b'PIRATES\x87. THEIR SKIN IS': ("Kraid", 2, LogicShortcut(lambda loadout: (
        (area_doors["OceanShoreR"] in loadout) and
        (Items.GravityBoots in loadout) and
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))
        (missileDamage in loadout) and
        ((Items.GravitySuit in loadout) or (
            (Tricks.sbj_underwater_w_hjb in loadout) and
            (Tricks.movement_zoast in loadout)
        ))
    ))),
    b'AROUND THEM. IT IS LIKELY THAT': ("Crocomire", 4, LogicShortcut(lambda loadout: (
        (Items.GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (Items.SpeedBooster in loadout) and
        (Items.Super in loadout)  # door to elevator to jungle's heart
    ))),
    b'PHANTOON\x87 CAN CLOAK': ("Phantoon", 3, LogicShortcut(lambda loadout: (
        (Items.Super in loadout) and
        (railAccess in loadout) and
        (SkyWorld.anticipation in loadout) and
        (Items.GravityBoots in loadout) and
        ((SkyWorld.killRidley in loadout) or (
            (can_bomb(1) in loadout) and
            (loadout.has_any(Items.Bombs, Items.Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile))
        )) and
        # get out
        (SkyWorld.killPhantoon in loadout) and
        (can_bomb(3) in loadout) and
        (
            (SkyWorld.meetingHallToLeft in loadout) or
            (SkyWorld.killRidley in loadout)
        )
    ))),
    b'FUNGUS AND CAN CHANGE THE STRUCTURE OF': ("Spore Spawn", 3, LogicShortcut(lambda loadout: (
        ((
            (area_doors["FieldAccessL"] in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ) or (
            (area_doors["TransferStationR"] in loadout) and
            (Items.DarkVisor in loadout) and
            (pinkDoor in loadout)  # between east spore field and ESF access
        )) and
        ((Items.DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
        (can_bomb(1) in loadout) and
        (Items.Morph in loadout) and
        (Items.GravityBoots in loadout) and
        # 5-tile morph jump
        (pinkDoor in loadout)  # between spore collection and spore generator access
    ))),
    b'COMMANDEERED THESE AND BUILT THEM INTO': ("Aurora", 1, LogicShortcut(lambda loadout: (
        loadout.game.all_locations["Weapon Locker"] in solve(loadout.game)[2]
        # only valid if doors don't change color
    ))),
    b'ALMOST ANY LIFEFORM WHILE BEING NEARLY': ("Metroid", 4, LogicShortcut(lambda loadout: (
        loadout.game.all_locations["Extract Storage"] in solve(loadout.game)[2]
    ))),
}


_location_aliases = {
    "Archives: SJBoost": "Archives: back",
    "Archives: SpringBall": "Archives: front",

    "Briar: SJBoost": "Briar: top",
    "Briar: AmmoTank": "Briar: bottom",

    "Sandy Burrow: ETank": "Sandy Burrow: top",
    "Sandy Burrow: AmmoTank": "Sandy Burrow: bottom",

    "Sensor Maintenance: ETank": "Sensor Maintenance: top",
    "Sensor Maintenance: AmmoTank": "Sensor Maintenance: bottom",

    "Warrior Shrine: AmmoTank bottom": "Warrior Shrine: bottom",
    "Warrior Shrine: AmmoTank top": "Warrior Shrine: top",
    "Warrior Shrine: ETank": "Warrior Shrine: middle",

    "Impact Crater: AccelCharge": "Impact Crater",

    "Frozen Lake Wall: DamageAmp": "Frozen Lake Wall"
}


def choose_hint_location(game: Game) -> tuple[str, bytes]:
    hard_locs = hard_required_locations(game)
    hint_loc_name = hard_locs[-1]

    _, log_lines, _ = solve(game)
    spheres = get_playthrough_locations(log_lines)
    sphere_of_hinted_loc_i = 0
    for sphere in spheres:
        if hint_loc_name in sphere:
            for sphere_loc in sphere:
                # if screw is in the same sphere, hint that
                if game.all_locations[sphere_loc]["item"] == Items.Screw:
                    hint_loc_name = sphere_loc
                    break
            break
        sphere_of_hinted_loc_i += 1

    saved_items: dict[str, Optional[Item]] = {}
    for sphere_loc in spheres[sphere_of_hinted_loc_i]:
        item = game.all_locations[sphere_loc]["item"]
        saved_items[sphere_loc] = item
        game.all_locations[sphere_loc]["item"] = None
        # print(f"removing {item[0] if item else 'None'}")

    _, _, restricted_locs = solve(game)

    restricted_loadout = Loadout(game)
    for restricted_loc in restricted_locs:
        item = restricted_loc["item"]
        if item:
            restricted_loadout.append(item)

    restricted_loadout.append(Items.spaceDrop)
    restricted_loadout.append(area_doors["SunkenNestL"])

    updateLogic(game.all_locations.values(), restricted_loadout)

    allowed_bosses: list[bytes] = []
    for text_bytes, hint_info in hint_data.items():
        _name, prob, shortcut = hint_info
        if shortcut in restricted_loadout:
            for _ in range(prob):
                allowed_bosses.append(text_bytes)
            # print(f"can hint: {_name}  {repr(text_bytes)}")

    for saved_loc_name, item in saved_items.items():
        game.all_locations[saved_loc_name]["item"] = item

    return hint_loc_name, random.choice(allowed_bosses)


def write_hint_to_rom(loc_name: str, hint_loc_marker: bytes, rom_writer: RomWriter) -> None:
    assert len(rom_writer.rom_data), "tried to write hints without rom"
    rom = rom_writer.rom_data

    all_locations = tuple(loc["fullitemname"] for loc in pullCSV().values())

    def get_decoy() -> str:
        decoy_target = random.choice(all_locations)
        decoy_chars = [(" " if c == " " else ".") for c in decoy_target]
        return "".join(decoy_chars)

    for each_loc_marker in hint_data:
        destination_i = rom.index(each_loc_marker) + len(each_loc_marker)
        end_i = rom.index(b'\x00', destination_i)
        length_limit = end_i - destination_i

        # make replacement text
        first_dot_length = random.randrange(2, 11)
        second_dot_length = random.randrange(12, 15) - first_dot_length
        to_write = "... " + ("." * first_dot_length) + " " + ("." * second_dot_length) + " " + (
            (
                loc_name
                if loc_name not in _location_aliases
                else _location_aliases[loc_name]
            ).upper()
            if each_loc_marker == hint_loc_marker
            else get_decoy()
        )
        to_write = to_write[:length_limit]

        assert all(32 <= ord(c) < 127 for c in to_write), f"tried to write non-ascii hint {to_write}"

        rom_writer.writeBytes(destination_i, to_write.encode() + b'\x00\x00')


def get_hint_spoiler_text(loc_name: str, hint_loc_marker: bytes) -> str:
    return f"\nhint for {loc_name} at {hint_data[hint_loc_marker][0]}\n"
