from collections import defaultdict
import sys
from pathlib import Path
import pytest

# import hacks, because this project is not a python package
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from connection_data import SunkenNestL, VanillaAreas, area_doors
from game import Game, GameOptions
from item_data import Items, items_unpackable
from loadout import Loadout
from location_data import Location, pullCSV
from logic_presets import casual, medium, expert
from logic_shortcut_data import can_win
from logic_updater import updateLogic
from trick import Trick

# TODO: test that all locations are obtainable with no tricks


def setup(logic: frozenset[Trick]) -> tuple[Game, Loadout]:
    """ returns (all locations, vanilla connections, a new loadout) """
    all_locations = pullCSV()
    options = GameOptions(logic, False, "D", True)
    game = Game(options, all_locations, VanillaAreas(), 0)
    loadout = Loadout(game)
    return game, loadout


def test_start_logic() -> None:
    game, loadout = setup(casual)

    def update_acc() -> list[Location]:
        updateLogic(game.all_locations.values(), loadout)

        return [loc for loc in game.all_locations.values() if loc['inlogic']]

    accessible = update_acc()
    assert len(accessible) == 1, f"accessible len {len(accessible)}"
    assert accessible[0]['fullitemname'] == "Torpedo Bay", f"not Torpedo Bay: {accessible}"

    loadout.append(Items.Missile)
    accessible = update_acc()
    print("  with missile")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 3, "add Gantry and Weapon Locker"

    loadout.append(SunkenNestL)
    accessible = update_acc()
    print("  with planet")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 5, "add Subterranean Burrow and Ocean Shore: Bottom"

    game, _ = setup(expert)
    loadout = Loadout(game, loadout.contents)

    accessible = update_acc()
    print("  with expert")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 5, "nothing else? really?"

    loadout.append(Items.Morph)
    accessible = update_acc()
    print("  with morph")
    for loc in accessible:
        print(loc["fullitemname"])
    assert len(accessible) == 7


@pytest.mark.parametrize("logic", (casual, expert))
def test_all_locations(logic: frozenset[Trick]) -> None:
    game, loadout = setup(logic)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        loadout.append(item)
    for _ in range(10):
        loadout.append(Items.Energy)

    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    assert len(accessible) == 122, f"acc len {len(accessible)}"


def test_casual_no_hell_runs() -> None:
    game, loadout = setup(casual)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        if item != Items.Varia:
            loadout.append(item)
    for _ in range(16):
        loadout.append(Items.Energy)

    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    assert len(accessible) < 110, f"acc len {len(accessible)}"


def test_expert_hell_runs() -> None:
    game, loadout = setup(expert)

    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    for item in items_unpackable:
        if item != Items.Varia:
            loadout.append(item)
    for _ in range(16):
        loadout.append(Items.Energy)

    updateLogic(game.all_locations.values(), loadout)

    accessible = [loc for loc in game.all_locations.values() if loc['inlogic']]

    # 121 because Colosseum requires Varia for expert
    assert len(accessible) >= 121, (
        "expert can't get these without varia: "
        f"{[loc['fullitemname'] for loc in game.all_locations.values() if not loc['inlogic']]}"
    )


def test_crypt_no_bomb_no_wave() -> None:
    """ test hitting switch in Crypt by following bullet with speedball """
    game, loadout = setup(expert)

    loadout.append(area_doors["RuinedConcourseBL"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Morph)
    loadout.append(Items.PowerBomb)
    loadout.append(Items.Missile)
    loadout.append(Items.LargeAmmo)
    loadout.append(Items.HiJump)
    loadout.append(Items.Aqua)

    updateLogic(game.all_locations.values(), loadout)
    assert not game.all_locations["Crypt"]["inlogic"]

    loadout.append(Items.Speedball)
    updateLogic(game.all_locations.values(), loadout)
    assert game.all_locations["Crypt"]["inlogic"]

    # mypy bug doesn't end type narrowing, thinks this is unreachable code
    loadout.contents[Items.Speedball] -= 1  # type: ignore
    updateLogic(game.all_locations.values(), loadout)
    assert not game.all_locations["Crypt"]["inlogic"]

    loadout.append(Items.Ice)
    updateLogic(game.all_locations.values(), loadout)
    assert game.all_locations["Crypt"]["inlogic"]


def test_warrior_shrine_speedball() -> None:
    """ test hitting switch in Crypt by following bullet with speedball """
    game, loadout = setup(casual)

    loadout.append(area_doors["RuinedConcourseBL"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Morph)
    loadout.append(Items.PowerBomb)
    loadout.append(Items.Missile)
    loadout.append(Items.HiJump)
    loadout.append(Items.Ice)
    loadout.append(Items.Aqua)

    updateLogic(game.all_locations.values(), loadout)

    assert not game.all_locations["Warrior Shrine: Middle"]["inlogic"]

    loadout.append(Items.Speedball)

    updateLogic(game.all_locations.values(), loadout)

    assert game.all_locations["Warrior Shrine: Middle"]["inlogic"]


def test_norak_perimeters() -> None:
    game, loadout = setup(expert)

    loadout.append(area_doors["NorakPerimeterTR"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Screw)

    updateLogic(game.all_locations.values(), loadout)

    assert area_doors["NorakPerimeterBL"] not in loadout


@pytest.mark.parametrize("logic", (casual, expert))
def test_slag_heap_escape(logic: frozenset[Trick]) -> None:
    """ getting out of slag heap requires getting through ice pods """
    game, loadout = setup(logic)

    loadout.append(area_doors["CollapsedPassageR"])
    loadout.append(Items.spaceDrop)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.MetroidSuit)
    loadout.append(Items.Varia)
    loadout.append(Items.Missile)
    loadout.append(Items.Wave)
    loadout.append(Items.Morph)
    loadout.append(Items.Bombs)
    loadout.append(Items.Speedball)

    updateLogic(game.all_locations.values(), loadout)

    assert not game.all_locations["Slag Heap"]["inlogic"]

    loadout.append(Items.Ice)

    updateLogic(game.all_locations.values(), loadout)

    assert game.all_locations["Slag Heap"]["inlogic"]


_unique_items = [
    Items.Missile,
    Items.Morph,
    Items.GravityBoots,
    Items.Super,
    Items.Grapple,
    Items.PowerBomb,
    Items.Speedball,
    Items.Bombs,
    Items.HiJump,
    Items.Aqua,
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
]


_hard_required_items = {
    "casual": [
        Items.Morph, Items.GravityBoots, Items.MetroidSuit, Items.Super, Items.PowerBomb, Items.Screw, Items.Grapple
    ],
    "medium": [
        Items.Morph, Items.GravityBoots, Items.MetroidSuit, Items.Super, Items.PowerBomb, Items.Screw, Items.Grapple
    ],
    "expert": [
        Items.Morph, Items.GravityBoots, Items.MetroidSuit, Items.Super, Items.PowerBomb, Items.Screw
    ],
}


def test_hard_required_items() -> None:
    for logic in (casual, medium, expert):
        logic_name = 'casual' if logic is casual else ('medium' if logic is medium else 'expert')
        print(f" - {logic_name}")
        for excluded_item in _unique_items:
            game, loadout = setup(logic)
            loadout.append(SunkenNestL)
            loadout.append(Items.spaceDrop)
            for item in items_unpackable:
                if item != excluded_item:
                    loadout.append(item)

            # some of the non-unique that can help in logic
            for _ in range(12):
                loadout.append(Items.Energy)
                loadout.append(Items.LargeAmmo)
            loadout.append(Items.SpaceJumpBoost)

            updateLogic(game.all_locations.values(), loadout)

            if can_win in loadout:
                assert excluded_item not in _hard_required_items[logic_name], \
                    f"{excluded_item[0]} in {logic_name} hard required items"
                print(f"{excluded_item[0]} not")
            else:
                assert excluded_item in _hard_required_items[logic_name], \
                    f"{excluded_item[0]} missing from {logic_name} hard required items"
                print(f"{excluded_item[0]}  - - - - hard required")


_possible_places = {
    Items.Morph: frozenset([
        "Docking Port 3",
        "Docking Port 4",
        "Gantry",
        "Ready Room",
        "Torpedo Bay",
        "Weapon Locker",

        "Ocean Shore: Bottom",
        "Ocean Shore: Top",
        "Sandy Cache",
        "Sandy Gully",
        "Sediment Floor",
        "Sediment Flow",
        "Submarine Nest",
        "Subterranean Burrow",
        "Grand Vault",
        "Vulnar Caves Entrance",
    ]),
    Items.GravityBoots: frozenset([
        "Aft Battery",
        "Docking Port 3",
        "Docking Port 4",
        "Extract Storage",
        "Forward Battery",
        "Gantry",
        "Ready Room",
        "Torpedo Bay",
        "Weapon Locker",

        "Ocean Shore: Bottom",
        "Subterranean Burrow",
    ])
}


@pytest.mark.parametrize("logic", (casual, medium, expert))
def test_restrictive_item_locations(logic: frozenset[Trick]) -> None:
    for excluded_item in _possible_places:
        print(f"  -- {excluded_item[0]}")
        game, loadout = setup(logic)

        for item in items_unpackable:
            if item != excluded_item and item != Items.spaceDrop:
                loadout.append(item)

        # some of the non-unique that can help in logic
        for _ in range(12):
            loadout.append(Items.Energy)
            loadout.append(Items.LargeAmmo)
        loadout.append(Items.SpaceJumpBoost)

        found: dict[str, bool] = defaultdict(bool)

        def this_loadout() -> None:
            updateLogic(game.all_locations.values(), loadout)

            for loc_name, loc in game.all_locations.items():
                if loc["inlogic"]:
                    found[loc_name] = True
                    assert loc_name in _possible_places[excluded_item], \
                        f"logic thinks {excluded_item[0]} can be at {loc_name}"
                    print(loc_name)

        this_loadout()
        print(" -- space drop")
        loadout.append(SunkenNestL)
        loadout.append(Items.spaceDrop)
        this_loadout()

        for loc_name in _possible_places[excluded_item]:
            assert found[loc_name], \
                f"logic thinks {excluded_item[0]} can't be at {loc_name}"


_possible_places_area = {
    "expert": {
        Items.Morph: frozenset([
            "Ocean Shore: Bottom",
            "Ocean Shore: Top",
            "Sandy Cache",
            "Sandy Gully",
            "Sediment Floor",
            "Sediment Flow",
            "Submarine Nest",
            "Subterranean Burrow",
            "Arena",
            "Grand Vault",
            "Hall Of The Elders",
            "Vulnar Caves Entrance",
            "Colosseum",
            "Depressurization Valve",
            "Antelier",
            "Chamber Of Wind",
            "Crocomire's Energy Station",
            "Crocomire's Lair",
            "Equipment Locker",
            "Loading Dock Storage Area",
            "Norak Escarpment",
            "Restricted Area",
            "Containment Area",
            "Shrine Of Fervor",
            "Water Garden",
            "Armory Cache 2",
            "Armory Cache 3",
            "Drawing Room",
            "Glacier's Reach",
            "Grand Promenade",
            "Ice Cave",
            "Icy Flow",
            "Reliquary Access",
            "Syzygy Observatorium",
            "Portico",
            "Saline Cache",
            "Tower Rock Lookout",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
        ]),
        Items.GravityBoots: frozenset([
            "Ocean Shore: Bottom",
            "Subterranean Burrow",
            "Loading Dock Storage Area",
            # can be in these spaceport locations AFTER falling from spaceport
            "Aft Battery",
            "Forward Battery",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
            "Extract Storage",
        ])
    },
    "medium": {
        Items.Morph: frozenset([
            "Ocean Shore: Bottom",
            "Ocean Shore: Top",
            "Sandy Cache",
            "Sandy Gully",
            "Sediment Floor",
            "Sediment Flow",
            "Submarine Nest",
            "Subterranean Burrow",
            "Arena",
            "Grand Vault",
            "Hall Of The Elders",
            "Vulnar Caves Entrance",
            "Colosseum",
            "Depressurization Valve",
            "Antelier",
            "Chamber Of Wind",
            "Crocomire's Energy Station",
            "Crocomire's Lair",
            "Equipment Locker",
            "Loading Dock Storage Area",
            "Norak Escarpment",
            "Restricted Area",
            "Containment Area",
            "Shrine Of Fervor",
            "Water Garden",
            "Glacier's Reach",
            "Grand Promenade",
            "Ice Cave",
            "Icy Flow",
            "Portico",
            "Saline Cache",
            "Tower Rock Lookout",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
        ]),
        Items.GravityBoots: frozenset([
            "Ocean Shore: Bottom",
            "Subterranean Burrow",
            "Loading Dock Storage Area",
            # can be in these spaceport locations AFTER falling from spaceport
            "Aft Battery",
            "Forward Battery",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
            "Extract Storage",
        ])
    },
    "casual": {
        Items.Morph: frozenset([
            "Ocean Shore: Bottom",
            "Ocean Shore: Top",
            "Sandy Cache",
            "Sandy Gully",
            "Sediment Floor",
            "Sediment Flow",
            "Submarine Nest",
            "Subterranean Burrow",
            "Arena",
            "Grand Vault",
            "Hall Of The Elders",
            "Vulnar Caves Entrance",
            "Colosseum",
            "Depressurization Valve",
            "Antelier",
            "Crocomire's Energy Station",
            "Crocomire's Lair",
            "Equipment Locker",
            "Loading Dock Storage Area",
            "Norak Escarpment",
            "Restricted Area",
            "Containment Area",
            "Shrine Of Fervor",
            "Water Garden",
            "Glacier's Reach",
            "Grand Promenade",
            "Ice Cave",
            "Icy Flow",
            "Portico",
            "Saline Cache",
            "Tower Rock Lookout",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
        ]),
        Items.GravityBoots: frozenset([
            "Ocean Shore: Bottom",
            "Subterranean Burrow",
            "Loading Dock Storage Area",
            # can be in these spaceport locations AFTER falling from spaceport
            "Aft Battery",
            "Forward Battery",
            "Docking Port 3",
            "Docking Port 4",
            "Gantry",
            "Ready Room",
            "Torpedo Bay",
            "Weapon Locker",
            "Extract Storage",
        ])
    },
}


@pytest.mark.parametrize("logic", (casual, medium, expert))
def test_restrictive_item_locations_area_rando(logic: frozenset[Trick]) -> None:
    logic_name = 'casual' if logic is casual else ('medium' if logic is medium else 'expert')
    print(f" - {logic_name}")
    for excluded_item in _possible_places_area[logic_name]:
        print(f"  -- {excluded_item[0]}")
        game, loadout = setup(logic)

        for item in items_unpackable:
            if item != excluded_item and item != Items.spaceDrop:
                loadout.append(item)

        # some of the non-unique that can help in logic
        for _ in range(12):
            loadout.append(Items.Energy)
            loadout.append(Items.LargeAmmo)
        loadout.append(Items.SpaceJumpBoost)

        for door in area_doors.values():
            loadout.append(door)

        loadout.append(Items.spaceDrop)

        found: dict[str, bool] = defaultdict(bool)

        def this_loadout() -> None:
            updateLogic(game.all_locations.values(), loadout)

            for loc_name, loc in game.all_locations.items():
                if loc["inlogic"]:
                    found[loc_name] = True
                    assert loc_name in _possible_places_area[logic_name][excluded_item], \
                        f"logic thinks {excluded_item[0]} can be at {loc_name}"
                    print(loc_name)

        this_loadout()

        for loc_name in _possible_places_area[logic_name][excluded_item]:
            assert found[loc_name], f"logic thinks {excluded_item[0]} can't be at {loc_name}"


_no_bombing = frozenset([
    "Aft Battery",
    "Docking Port 3",
    "Docking Port 4",
    "Forward Battery",
    "Gantry",
    "Ready Room",
    "Torpedo Bay",
    "Weapon Locker",
    "Eddy Channels",
    "Impact Crater",
    "Ocean Shore: Bottom",
    "Ocean Shore: Top",
    "Ocean Vent Supply Depot",
    "Sandy Burrow: Bottom",
    "Sandy Burrow: Top",
    "Sandy Cache",
    "Sandy Gully",
    "Sediment Floor",
    "Sediment Flow",
    "Shrine Of The Penumbra",
    "Submarine Alcove",
    "Submarine Nest",
    "Subterranean Burrow",
    "Archives: Back",
    "Archives: Front",
    "Arena",
    "Grand Vault",
    "Hall Of The Elders",
    "Mezzanine Concourse",
    "Monitoring Station",
    "Path Of Swords",
    "Sensor Maintenance: Top",
    "Trophobiotic Chamber",
    "Vulnar Caves Entrance",
    "Warrior Shrine: Bottom",
    "Warrior Shrine: Top",
    # "Warrior Shrine: Middle",
    "West Spore Field",
    "Colosseum",
    "Magma Lake Cache",
    "Mining Cache",
    "Antelier",
    "Briar: Bottom",
    "Chamber Of Wind",
    "Containment Area",
    "Crocomire's Energy Station",
    "Crocomire's Lair",
    "Equipment Locker",
    "Foundry",
    "Hydrodynamic Chamber",
    "Loading Dock Storage Area",
    "Norak Escarpment",
    "Restricted Area",
    "Shrine Of Fervor",
    "Water Garden",
    "Weapon Research",
    "Armory Cache 2",
    "Armory Cache 3",
    "Drawing Room",
    "Glacier's Reach",
    "Grand Promenade",
    "Summit Landing",
    "Ice Cave",
    "Icy Flow",
    "Reliquary Access",
    "Syzygy Observatorium",
    "Aft Battery",
    "Docking Port 3",
    "Docking Port 4",
    "Forward Battery",
    "Gantry",
    "Ready Room",
    "Torpedo Bay",
    "Weapon Locker",
])


@pytest.mark.parametrize("logic", (casual, medium, expert))
def test_no_bombing_locations(logic: frozenset[Trick]) -> None:
    game, loadout = setup(logic)

    for item in items_unpackable:
        if item not in {Items.Bombs, Items.PowerBomb, Items.spaceDrop}:
            loadout.append(item)

    # some of the non-unique that can help in logic
    for _ in range(12):
        loadout.append(Items.Energy)
        loadout.append(Items.LargeAmmo)
    loadout.append(Items.SpaceJumpBoost)

    found: dict[str, bool] = defaultdict(bool)

    def this_loadout() -> None:
        updateLogic(game.all_locations.values(), loadout)

        for loc_name, loc in game.all_locations.items():
            if loc["inlogic"]:
                found[loc_name] = True
                assert loc_name in _no_bombing, \
                    f"logic thinks no bombing is needed for {loc_name}"
                print(loc_name)

    this_loadout()
    print(" -- space drop")
    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    this_loadout()

    for loc_name in _no_bombing:
        assert (
            found[loc_name] or
            (logic is casual and loc_name == "Warrior Shrine: Top")  # or
            # (logic in {casual, medium} and loc_name == "Warrior Shrine: Middle")
        ), f"logic thinks bombing is needed for {loc_name}"


_no_bomb_blocks = frozenset([
    "Aft Battery",
    "Docking Port 3",
    "Docking Port 4",
    "Forward Battery",
    "Gantry",
    "Ready Room",
    "Torpedo Bay",
    "Weapon Locker",
    "Eddy Channels",
    "Impact Crater",
    "Ocean Shore: Bottom",
    "Ocean Shore: Top",
    "Ocean Vent Supply Depot",
    "Sandy Burrow: Bottom",
    "Sandy Cache",
    "Sandy Gully",
    "Sediment Floor",
    "Sediment Flow",
    "Shrine Of The Penumbra",
    "Submarine Alcove",
    "Submarine Nest",
    "Subterranean Burrow",
    "Archives: Back",
    "Archives: Front",
    "Arena",
    "Grand Vault",
    "Hall Of The Elders",
    "Mezzanine Concourse",
    "Monitoring Station",
    "Sensor Maintenance: Top",
    "Trophobiotic Chamber",
    "Vulnar Caves Entrance",
    "Warrior Shrine: Bottom",
    "Mining Cache",
    "Antelier",
    "Equipment Locker",
    "Hydrodynamic Chamber",
    "Loading Dock Storage Area",
    "Drawing Room",
    "Glacier's Reach",
    "Grand Promenade",
    "Ice Cave",
    "Icy Flow",
    "Reliquary Access",
    "Syzygy Observatorium",
])

_more_no_bomb_blocks_for_expert = frozenset([
    "West Spore Field",
    "Containment Area",
    "Foundry",
    "Restricted Area",
    "Weapon Research",
    "Norak Escarpment",
    "Briar: Bottom",
    "Shrine Of Fervor",
    "Water Garden",
    "Crocomire's Energy Station",
    "Crocomire's Lair",
])


@pytest.mark.parametrize("logic", (casual, medium, expert))
def test_no_bomb_blocks(logic: frozenset[Trick]) -> None:
    """ no bombs or PBs or Screw Attack (Speedbooster might be used to break bomb blocks) """
    game, loadout = setup(logic)

    for item in items_unpackable:
        if item not in {Items.Bombs, Items.PowerBomb, Items.Screw, Items.spaceDrop}:
            loadout.append(item)

    # some of the non-unique that can help in logic
    for _ in range(12):
        loadout.append(Items.Energy)
        loadout.append(Items.LargeAmmo)
    loadout.append(Items.SpaceJumpBoost)

    found: dict[str, bool] = defaultdict(bool)

    def this_loadout() -> None:
        updateLogic(game.all_locations.values(), loadout)

        for loc_name, loc in game.all_locations.items():
            if loc["inlogic"]:
                found[loc_name] = True
                assert loc_name in _no_bomb_blocks or (
                    logic is expert and loc_name in _more_no_bomb_blocks_for_expert
                ), f"logic thinks no bomb blocks are needed for {loc_name}"
                print(loc_name)

    this_loadout()
    print(" -- space drop")
    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    this_loadout()

    for loc_name in _no_bomb_blocks:
        assert found[loc_name], f"logic thinks bomb blocks are needed for {loc_name}"

    if logic is expert:
        for loc_name in _more_no_bomb_blocks_for_expert:
            assert found[loc_name], f"expert logic thinks bomb blocks are needed for {loc_name}"


_no_bomb_blocks_or_speed = frozenset([
    "Aft Battery",
    "Docking Port 3",
    "Docking Port 4",
    "Forward Battery",
    "Gantry",
    "Ready Room",
    "Torpedo Bay",
    "Weapon Locker",
    "Eddy Channels",
    "Impact Crater",
    "Ocean Shore: Bottom",
    "Ocean Shore: Top",
    "Ocean Vent Supply Depot",
    "Sandy Burrow: Bottom",
    "Sandy Cache",
    "Sandy Gully",
    "Sediment Floor",
    "Sediment Flow",
    "Shrine Of The Penumbra",
    "Submarine Alcove",
    "Submarine Nest",
    "Subterranean Burrow",
    "Archives: Front",
    "Arena",
    "Grand Vault",
    "Hall Of The Elders",
    "Monitoring Station",
    "Sensor Maintenance: Top",
    "Trophobiotic Chamber",
    "Vulnar Caves Entrance",
    "Warrior Shrine: Bottom",
    "Mining Cache",
])


_no_bomb_blocks_or_speed_expert = frozenset([
    "Mezzanine Concourse",
    "West Spore Field",

    # all of this group enabled by getting through causeway without (bombs, pbs, screw, speed)
    "Antelier",
    "Briar: Bottom",
    "Containment Area",
    "Equipment Locker",
    "Foundry",
    "Hydrodynamic Chamber",
    "Loading Dock Storage Area",
    "Norak Escarpment",
    "Restricted Area",
    "Shrine Of Fervor",
    "Weapon Research",

    "Drawing Room",
    "Glacier's Reach",
    "Grand Promenade",
    "Ice Cave",
    "Reliquary Access",
    "Syzygy Observatorium",
])


@pytest.mark.parametrize("logic", (casual, medium, expert))
def test_no_bomb_blocks_or_speed(logic: frozenset[Trick]) -> None:
    """ no bombs or PBs or Screw Attack or speed """
    game, loadout = setup(logic)

    for item in items_unpackable:
        if item not in {Items.Bombs, Items.PowerBomb, Items.Screw, Items.SpeedBooster, Items.spaceDrop}:
            loadout.append(item)

    # some of the non-unique that can help in logic
    for _ in range(12):
        loadout.append(Items.Energy)
        loadout.append(Items.LargeAmmo)
    loadout.append(Items.SpaceJumpBoost)

    found: dict[str, bool] = defaultdict(bool)

    def this_loadout() -> None:
        updateLogic(game.all_locations.values(), loadout)

        for loc_name, loc in game.all_locations.items():
            if loc["inlogic"]:
                found[loc_name] = True
                assert loc_name in _no_bomb_blocks_or_speed or (
                    logic is expert and loc_name in _no_bomb_blocks_or_speed_expert
                ), f"logic thinks no bomb/speed blocks are needed for {loc_name}"
                print(loc_name)

    this_loadout()
    print(" -- space drop")
    loadout.append(SunkenNestL)
    loadout.append(Items.spaceDrop)
    this_loadout()

    for loc_name in _no_bomb_blocks_or_speed:
        assert found[loc_name], f"logic thinks bomb/speed blocks are needed for {loc_name}"

    if logic is expert:
        for loc_name in _no_bomb_blocks_or_speed_expert:
            assert found[loc_name], f"expert logic thinks bomb/speed blocks are needed for {loc_name}"


# TODO: places that I can go with no bombs, pbs, or screw (doesn't include colosseum)
# places that I can go with screw, no bombs, pbs (includes colosseum)

# TODO: sediment floor is a place where supers can be?
# (if you come in from turbid passage and can cross sediment tunnel)

# TODO: make sure I can get sediment flow without speedball (if I have supers)
# (and without movement_zoast or whatever trick is there or'd with speedball)

# TODO: sediment floor is in logic from ocean floor with neither supers nor pbs
# (with moonfall_clip and missiles and stuff to go around through sea caves)

# TODO: mining cache without bombs or pbs (screw and speedball and wave)

# TODO: it looks like ocean vent and submarine alcove both require aqua or hi jump


if __name__ == "__main__":
    # test_hard_required_items()
    test_no_bomb_blocks_or_speed(expert)
