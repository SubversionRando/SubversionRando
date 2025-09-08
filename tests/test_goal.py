import itertools
import random
from subversion_rando.area_blitz import choose_excluded_locs
from subversion_rando.game import Exclude, GameOptions
from subversion_rando.goal import (
    event_to_location, events, generate_goals, map_stations, map_stations_reverse, map_to_location,
)
from subversion_rando.location_data import new_locations

_locations = new_locations()


def test_exclude_suzi() -> None:
    SUZI_MAPS = (0x3FDB9C, 0x3FD894)

    for _ in range(60):  # because random could pass test when broken
        options = GameOptions(frozenset(),
                              random.choice((True, False)),
                              random.choice(("B", "D", "MM")),  # type: ignore
                              # type ignore because mypy doesn't see Literal in random.choice
                              random.choice((True, False)),
                              random.choice((True, False)),
                              Exclude.suzi,
                              objective_rando=random.randrange(0, 20))
        excluded_locs = set(choose_excluded_locs(options, random.Random(), force_normal_sand_land=True))
        goals = generate_goals(options, excluded_locs, random.randrange(1073741824))

        assert len(goals.objectives) <= len(map_stations) - len(SUZI_MAPS), (
            f"{len(goals.objectives)=} {len(map_stations)=}"
        )

        for map_addr in SUZI_MAPS:
            assert map_addr in map_stations, f"{map_addr=}"
            assert map_addr in goals.map_station_order[-2:], f"{map_addr=} {goals.map_station_order=}"
            assert map_addr not in goals.map_station_order[:-2], f"{map_addr=} {goals.map_station_order=}"


def test_event_mapping_names() -> None:
    """ checking for typos in strings in this event mapping """
    event_names = {ev[1] for ev in itertools.chain(*events)}
    for event_name, loc_name in event_to_location.items():
        assert event_name in event_names, event_name
        assert loc_name in _locations.keys(), loc_name


def test_station_mapping_names() -> None:
    """ checking for typos in strings in this map station mapping """
    for station_name, loc_name in map_to_location.items():
        assert station_name in map_stations_reverse, station_name
        assert loc_name in _locations.keys(), loc_name
