import random
from subversion_rando.game import CypherItems, GameOptions
from subversion_rando.goal import generate_goals, map_stations


def test_exclude_suzi() -> None:
    SUZI_MAPS = (0x3FDB9C, 0x3FD894)

    for _ in range(60):  # because random could pass test when broken
        options = GameOptions(frozenset(),
                              random.choice((True, False)),
                              random.choice(("B", "D", "MM")),  # type: ignore
                              # type ignore because mypy doesn't see Literal in random.choice
                              random.choice((True, False)),
                              random.choice((True, False)),
                              CypherItems.SmallAmmo,
                              objective_rando=random.randrange(0, 20))
        goals = generate_goals(options)

        assert len(goals.objectives) <= len(map_stations) - len(SUZI_MAPS), (
            f"{len(goals.objectives)=} {len(map_stations)=}"
        )

        for map_addr in SUZI_MAPS:
            assert map_addr in map_stations, f"{map_addr=}"
            assert map_addr in goals.map_station_order[-2:], f"{map_addr=} {goals.map_station_order=}"
            assert map_addr not in goals.map_station_order[:-2], f"{map_addr=} {goals.map_station_order=}"
