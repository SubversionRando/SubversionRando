from collections.abc import Mapping, Set as AbstractSet
from random import Random
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, Literal

from subversion_rando.fillAssumed import FillAssumed
from subversion_rando.item_data import Items
from subversion_rando.romWriter import RomWriter

from .area_rando_types import AreaName, area_names
from .game import Exclude, GameOptions
from .location_data import Location, new_locations

# TODO: spoiler

# TODO: remove areas from area rando if we can match left and right doors

# TODO: don't choose boss in excluded area for hint


def choose_excluded_locs(
    options: GameOptions,
    random: Random,
    *,
    force_normal_sand_land: bool,
) -> set[str]:
    if options.exclude is Exclude.nothing:
        return set()

    if options.exclude is Exclude.thunder_lab:
        return {"Shrine Of The Animate Spark", "Enervation Chamber"}

    def locs_in_areas(areas: AbstractSet[AreaName]) -> set[str]:
        """ never exclude Torpedo Bay """
        locs = new_locations()
        return {
            loc_name
            for loc_name, loc in locs.items()
            if loc["rando_area"] in areas and loc_name != "Torpedo Bay"
        }

    if options.exclude is Exclude.suzi:
        return locs_in_areas({"Suzi"})

    if TYPE_CHECKING:
        from typing_extensions import assert_type
        assert_type(options.exclude, Literal[Exclude.blitz, Exclude.suzi_blitz])
    assert options.exclude in (Exclude.blitz, Exclude.suzi_blitz), options.exclude

    do_not_choose: set[AreaName] = {"ServiceSector", "Daphne", "Early"}
    choose_n = 4
    if force_normal_sand_land:
        do_not_choose.add("SandLand")
    if options.exclude is Exclude.suzi_blitz:
        do_not_choose.add("Suzi")
        choose_n = 3

    choices: list[AreaName] = [
        area_name
        for area_name in area_names
        if area_name not in do_not_choose
    ]
    chosen = set(random.sample(choices, choose_n))
    if options.exclude is Exclude.suzi_blitz:
        chosen.add("Suzi")
    if "Geothermal" in chosen:
        chosen.add("ServiceSector")
        assert len(chosen) == 5, chosen
    return locs_in_areas(chosen)


def remove_excluded_item_pool(fill: FillAssumed, excluded_locs: AbstractSet[str]) -> None:
    n = len(excluded_locs)
    blitz = n > 24

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

        if blitz:
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

    fill.set_extra(
        [Items.Refuel] * refuel_extra_count +
        [Items.LargeAmmo if blitz else Items.SmallAmmo] * small_extra_count
    )
    new_prog = [
        item
        for item in fill.prog_items
        if item not in (Items.SmallAmmo, Items.LargeAmmo)
    ]
    new_prog.extend([Items.LargeAmmo] * large_prog_count)
    new_prog.extend([Items.SmallAmmo] * small_prog_count)
    assert small_prog_count == 0 or not blitz, "small ammo should have been converted to large if blitz"
    fill.set_prog(new_prog)


def place_excluded(all_locations: Mapping[str, Location], excluded_locs: AbstractSet[str]) -> None:
    for loc_name in excluded_locs:
        all_locations[loc_name]["item"] = Items.SmallAmmo


_LOG_AREA_NAMES: Final[Mapping[AreaName, bytes]] = MappingProxyType({
    "SandLand": b"SANDLAND",
    "Early": b"EARLY",
    "Suzi": b"SUZI",
    "PirateLab": b"PIRATE LAB",
    "ServiceSector": b"SERVICE SECTOR",
    "SkyWorld": b"SKY WORLD",
    "Verdite": b"VERDITE",
    "FireHive": b"FIREHIVE",
    "DrayLand": b"DRAYLAND",
    "Geothermal": b"GEOTHERMAL",
    "LifeTemple": b"LIFE TEMPLE",
    "SpacePort": b"SPACE PORT",
    "Daphne": b"DAPHNE",
})


def get_excluded_areas(excluded_locs: AbstractSet[str]) -> list[bytes]:
    locs = new_locations()
    areas: set[AreaName] = {locs[loc_name]["rando_area"] for loc_name in excluded_locs}
    area_strings: set[bytes] = {_LOG_AREA_NAMES[area_name] for area_name in areas}
    if "Suzi" in areas and "Tower Rock Lookout" not in excluded_locs:
        assert "Enervation Chamber" in excluded_locs, excluded_locs
        assert "Shrine Of The Animate Spark" in excluded_locs, excluded_locs
        assert "Reef Nook" not in excluded_locs, excluded_locs
        area_strings.remove(b"SUZI")
        area_strings.add(b"THUNDER LAB")
    return sorted(area_strings)


def write_excluded_areas_to_log(excluded_locs: AbstractSet[str], rom_writer: RomWriter) -> None:
    excluded = get_excluded_areas(excluded_locs)
    included = [
        area_name
        for area_name in _LOG_AREA_NAMES.values()
        if area_name not in excluded and area_name != b"DAPHNE"
    ]

    #                v red    v white                                         pink yellow green ->
    LOC_LOG_DATA = b"\x82TN578\x87 IS A SUPERTERRAN CLASS PLANET WHICH WAS AN ANCIENT HOME FOR THE \x86CHOZO\x87. EVEN THOUGH IT HAS A BREATHABLE ATMOSPHERE AND ABUNDANT WATER, THE \x85INTENSE GRAVITY\x87 PUTS IT ON THE EDGE OF HABITABILITY. IT'S UNCLEAR WHY THE \x84SPACE PIRATES\x87 WOULD BE HERE."  # noqa: E501
    LOC_LOG_INDEX = 0x1e0f2f
    assert rom_writer.rom_data.find(LOC_LOG_DATA) in (-1, LOC_LOG_INDEX), rom_writer.rom_data.find(LOC_LOG_DATA)

    if b"SPACE PORT" in excluded:
        reminder = b"\n\n(\x85TORPEDO BAY IS NEVER EXCLUDED.\x87)"
    else:
        reminder = b""

    message = (
        b"\x82EXCLUDED AREAS\x87:\n- " +
        (b"\n- ".join(excluded)) +
        reminder +
        b"\n\n\x84INCLUDED AREAS\x87:\n- " +
        (b"\n- ".join(included)) +
        b"\x00"
    )
    assert len(message) <= len(LOC_LOG_DATA), "longer than the data we're replacing"
    rom_writer.writeBytes(LOC_LOG_INDEX, message)
