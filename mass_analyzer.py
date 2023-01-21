

from collections import Counter
import pickle

from item_data import Items
from mass_generator import GameData


file_name = "data/ECU-w-and-wo-area-rando-D-T-F-2023-01-17-10-41-50.dat"


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

    counts: Counter[str] = Counter()
    for g in games:
        for loc_name, loc in g.all_locations.items():
            if loc["item"] == Items.GravityBoots:
                counts[loc_name] += 1
                break

    for b in counts:
        print(f"{b}: {counts[b]}")


if __name__ == "__main__":
    main()
