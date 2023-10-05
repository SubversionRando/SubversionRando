

from collections import Counter
import pickle

from subversion_rando.item_data import unique_items
from mass_generator import GameData


file_name = "data/ECU-w-and-wo-area-rando-MMB-cypher-anything-before-transform-adjust-2023-04-01-12-07-51.dat"
file_name = "data/ECU-w-and-wo-area-rando-MMB-cypher-anything-2023-04-01-11-12-52.dat"


def read_games() -> list[GameData]:
    games: list[GameData] = []
    with open(file_name, "rb") as file:
        while True:
            try:
                g: GameData = pickle.load(file)
                games.append(g)
            except EOFError:
                break
    return games


def main() -> None:
    games = read_games()

    loc_counts: Counter[str] = Counter()
    item_counts: Counter[str] = Counter()
    for g in games:
        for loc_name, loc in g.all_locations.items():
            if loc["item"] in unique_items:
                loc_counts[loc_name] += 1

        item = g.all_locations["Docking Port 4"]["item"]
        assert item
        item_counts[item[0]] += 1

    for b, c in loc_counts.most_common():
        print(f"{b}: {c}")
    print()
    for b, c in item_counts.most_common():
        print(f"{b}: {c}")


if __name__ == "__main__":
    main()
