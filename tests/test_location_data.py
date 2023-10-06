from subversion_rando.location_data import pullCSV
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
        this_id = loc['plmparamlo']
        if loc['fullitemname'] == "Sandy Burrow: Bottom":
            # TestRunner: "I actually have no idea why that one has such a weird ID, pretty sure that was a mistake"
            # But it works, so it's ok.
            assert this_id == 0xc6
            continue
        all_ids.append(this_id)
        if this_id > highest:
            highest = this_id
        alt = loc['alternateplmparamlo']
        if alt:
            all_ids.append(alt)
            if alt > highest:
                highest = alt

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
        plm_param_lo = loc['plmparamlo']
        assert plm_param_lo in map_icon_data, f"loc {loc['fullitemname']} id {plm_param_lo} not in map_icon_data"

        alt = loc["alternateplmparamlo"]
        if alt:
            assert alt in map_icon_data, f"loc {loc['fullitemname']} alt id {alt} not in map_icon_data"


if __name__ == "__main__":
    test_location_ids()
