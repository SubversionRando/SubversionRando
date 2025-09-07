from collections import defaultdict

from subversion_rando.area_rando_types import AreaName, area_names
from subversion_rando.connection_data import area_doors
from subversion_rando.location_data import area_location_count, get_location_ids, new_locations
from subversion_rando.logic_presets import expert
from subversion_rando.map_icon_data import data as map_icon_data

from utils import load_everything_except, setup


def test_location_ids() -> None:
    """
    make sure all the location ids are present in the csv,
    either as primary or alternate
    """
    locs = new_locations()
    highest = -1
    all_ids: list[int] = []
    for loc in locs.values():
        loc_ids = get_location_ids(loc)
        if loc['fullitemname'] == "Sandy Burrow: Bottom":
            # TestRunner: "I actually have no idea why that one has such a weird ID, pretty sure that was a mistake"
            # But it works, so it's ok.
            assert loc_ids[0] == 0xc6
            continue
        for each_id in loc_ids:
            all_ids.append(each_id)
            if each_id > highest:
                highest = each_id

    assert len(all_ids) == 130, f"{len(all_ids)=}"  # 131 with sandy burrow bottom
    print(f"{len(all_ids)=}")
    assert highest == 0x81, f"{hex(highest)=}"  # 129
    print(f"{hex(highest)=}")
    sorted_ids = sorted(all_ids)
    assert sorted_ids[0] == 0, f"{sorted_ids[0]=}"
    print(sorted_ids)


def test_map_icon_data() -> None:
    locs = new_locations()
    for loc in locs.values():
        loc_ids = get_location_ids(loc)
        for loc_id in loc_ids:
            assert loc_id in map_icon_data, f"loc {loc['fullitemname']} id {loc_id} not in map_icon_data"


def test_loc_data() -> None:
    """
    test that the rando areas in the location data
    match where logic sees them
    """
    from subversion_rando.logic_locations import location_logic

    loc_to_areas: dict[str, set[AreaName]] = defaultdict(set)

    # Is this location in logic from this area door?
    # If so, associate the location with the area.
    for area_door in area_doors.values():
        _game, loadout = setup(expert)
        loadout.append(area_door)
        load_everything_except(loadout, ())
        for loc_name, rule in location_logic.items():
            if rule(loadout):
                loc_to_areas[loc_name].add(area_door.area_name)

    for loc_name, area in loc_to_areas.items():
        if len(area) != 1:
            # Most of the SpacePort locations have all the areas
            # (because of the falling from SpacePort logic).
            print(len(area))
            assert len(area) == 13, area
            area.intersection_update({"SpacePort"})
            assert len(area) == 1, area
        else:
            # Loading Dock is the only exception.
            assert "SpacePort" not in area or loc_name.startswith("Loading Dock"), (loc_name, area)

    # import pprint
    # pprint.pp(loc_to_areas)

    loc_to_area = {
        loc_name: next(iter(areas))
        for loc_name, areas in loc_to_areas.items()
    }

    locations = new_locations()

    for loc in locations.values():
        loc_name = loc["fullitemname"]
        assert loc["rando_area"] in area_names, loc
        assert loc_to_area[loc_name] == loc["rando_area"], (loc_to_area[loc_name], loc)

    area_to_loc: dict[AreaName, set[str]] = defaultdict(set)
    for loc in locations.values():
        area_to_loc[loc["rando_area"]].add(loc["fullitemname"])
    for area_name, locs in area_to_loc.items():
        print(f'    "{area_name}": {len(locs)},')

    for area_name in area_names:
        assert area_location_count[area_name] == len(area_to_loc[area_name]), (area_name, area_to_loc)


if __name__ == "__main__":
    test_loc_data()
