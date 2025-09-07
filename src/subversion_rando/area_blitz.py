from collections.abc import Mapping, Set as AbstractSet
from random import Random
from typing import TYPE_CHECKING, Literal

from subversion_rando.fillAssumed import FillAssumed
from subversion_rando.item_data import Items

from .area_rando_types import AreaName, area_names
from .game import Exclude, GameOptions
from .location_data import Location, new_locations

# TODO: spoiler

# TODO: in-game log book "SUPERTERRAN CLASS"

# TODO: remove areas from area rando if we can match left and right doors

# TODO: don't choose boss in excluded area for hint


def choose_excluded_locs(options: GameOptions, random: Random) -> list[str]:
    if options.exclude is Exclude.nothing:
        return []

    if options.exclude is Exclude.thunder_lab:
        return ["Shrine Of The Animate Spark", "Enervation Chamber"]

    def locs_in_areas(areas: AbstractSet[AreaName]) -> list[str]:
        """ never exclude Torpedo Bay """
        locs = new_locations()
        return [
            loc_name
            for loc_name, loc in locs.items()
            if loc["rando_area"] in areas and loc_name != "Torpedo Bay"
        ]

    if options.exclude is Exclude.suzi:
        return locs_in_areas({"Suzi"})

    if TYPE_CHECKING:
        from typing_extensions import assert_type
        assert_type(options.exclude, Literal[Exclude.blitz])
    assert options.exclude is Exclude.blitz, options.exclude

    choices: list[AreaName] = [
        area_name
        for area_name in area_names
        if area_name not in ("ServiceSector", "Daphne", "Early")
    ]
    chosen = set(random.sample(choices, 4))
    if "Geothermal" in chosen:
        chosen.add("ServiceSector")
        assert len(chosen) == 5, chosen
    return locs_in_areas(chosen)


def remove_excluded_item_pool(fill: FillAssumed, excluded_locs: list[str]) -> None:
    n = len(excluded_locs)

    small_extra_count = fill.extra_items.count(Items.SmallAmmo)
    refuel_extra_count = fill.extra_items.count(Items.Refuel)
    assert refuel_extra_count == 7, refuel_extra_count
    assert small_extra_count + refuel_extra_count == len(fill.extra_items), fill.extra_items
    small_prog_count = fill.prog_items.count(Items.SmallAmmo)
    large_prog_count = fill.prog_items.count(Items.LargeAmmo)

    # first remove small ammo from extra
    remaining_small_for_extra = small_extra_count - n
    if remaining_small_for_extra >= 0:
        n = 0
        small_extra_count = remaining_small_for_extra

        # change prog small to large
        large_prog_count += small_prog_count
        small_prog_count = 0
    else:
        n -= small_extra_count
        small_extra_count = 0

        # then remove small ammo from prog
        remaining_small_for_prog = small_prog_count - n
        if remaining_small_for_prog >= 0:
            n = 0
            large_prog_count += remaining_small_for_prog
            small_prog_count = 0
        else:
            # still need to remove more
            n -= small_prog_count
            small_prog_count = 0

            # start removing refuel tanks
            remaining_refuel = refuel_extra_count - n
            if remaining_refuel >= 0:
                n = 0
                refuel_extra_count = remaining_refuel
            else:
                # now we've removed all small ammo and refuel
                n -= refuel_extra_count
                refuel_extra_count = 0

                # gotta start removing good stuff...
                n -= 1
                large_prog_count -= 1

                if n > 0:
                    n -= 1
                    large_prog_count -= 1

                    if n > 0:
                        n -= 1
                        fill.prog_items.remove(Items.DamageAmp)

                        if n > 0:
                            n -= 1
                            large_prog_count -= 1

                            if n > 0:
                                n -= 1
                                fill.prog_items.remove(Items.SpaceJumpBoost)

                                if n > 0:
                                    n -= 1
                                    fill.prog_items.remove(Items.DamageAmp)

                                    assert n == 0, f"too many locations excluded {excluded_locs}"

    fill.set_extra([Items.Refuel] * refuel_extra_count + [Items.LargeAmmo] * small_extra_count)
    new_prog = [
        item
        for item in fill.prog_items
        if item not in (Items.SmallAmmo, Items.LargeAmmo)
    ]
    new_prog.extend([Items.LargeAmmo] * large_prog_count)
    if TYPE_CHECKING:
        from typing_extensions import assert_type
        assert_type(small_prog_count, Literal[0])
    assert small_prog_count == 0, "small ammo should have been converted to large"
    fill.set_prog(new_prog)


def place_excluded(all_locations: Mapping[str, Location], excluded_locs: list[str]) -> None:
    for loc_name in excluded_locs:
        all_locations[loc_name]["item"] = Items.SmallAmmo
