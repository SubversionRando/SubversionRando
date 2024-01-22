from subversion_rando.location_data import get_location_ids, pullCSV
from subversion_rando.map_icon_data import data as map_icon_data


def test_location_ids() -> None:
    """
    make sure all the location ids are present in the csv,
    either as primary or alternate
    """
    locs = pullCSV()
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
    locs = pullCSV()
    for loc in locs.values():
        loc_ids = get_location_ids(loc)
        for loc_id in loc_ids:
            assert loc_id in map_icon_data, f"loc {loc['fullitemname']} id {loc_id} not in map_icon_data"


if __name__ == "__main__":
    test_location_ids()
