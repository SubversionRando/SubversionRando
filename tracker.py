from collections import defaultdict
from copy import deepcopy
from difflib import get_close_matches
import os
import sys
from typing import Type

from connection_data import AreaDoor, VanillaAreas, area_doors
from game import Game
from item_data import Items, all_items
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logicCasual import Casual
from logicExpert import Expert
from logicInterface import LogicInterface
from solver import solve

_name_aliases = {
    "Warrior Shrine: Top": "Warrior Shrine: AmmoTank top",
    "Warrior Shrine: Bottom": "Warrior Shrine: AmmoTank bottom",
    "Warrior Shrine: Middle": "Warrior Shrine: ETank",
    "Briar: Bottom": "Briar: AmmoTank",
    "Briar: Top": "Briar: SJBoost",
}
""" alternate name: location name """
# If you add an alias, add a unit test for it in test_tracker.py `test_loc_names_from_input()`

# Use capitalization in the aliases - a lowercase version will be made automatically.

# I thought about including vanilla majors as aliases,
# but I didn't because someone might type in the item they just picked up in the rando.


class Tracker:
    empty_locations: dict[str, Location]
    game_state_locations: dict[str, Location]
    loadout: Loadout

    def __init__(self) -> None:
        logic = Casual
        area_rando = False
        area_connections = VanillaAreas()

        self.empty_locations = pullCSV()
        self.game_state_locations = deepcopy(self.empty_locations)
        game = Game(logic, self.empty_locations, area_rando, area_connections)
        self.loadout = Loadout(game)

    def loc_names_from_input(self, in_text: str) -> list[str]:
        everything: dict[str, set[str]] = defaultdict(set)

        for loc_name in self.empty_locations:
            everything[loc_name].add(loc_name)
            everything[loc_name.lower()].add(loc_name)
            everything[loc_name[:len(in_text) + 1]].add(loc_name)
            everything[loc_name[:len(in_text) + 1].lower()].add(loc_name)
        for alias, loc_name in _name_aliases.items():
            everything[alias].add(loc_name)
            everything[alias.lower()].add(loc_name)
            everything[alias[:len(in_text) + 1]].add(loc_name)
            everything[alias[:len(in_text) + 1].lower()].add(loc_name)
        all_names = list(everything.keys())
        best = get_close_matches(in_text, all_names, n=1, cutoff=0.75)
        return list(everything[best[0]] if len(best) else [])

    def set_spoiler(self, filename: str) -> None:
        file_only = os.path.basename(filename)
        logic: Type[LogicInterface]
        if file_only[3] == "C":
            logic = Casual
        elif file_only[3] == "E":
            logic = Expert
        else:
            print(f"can't find logic letter in filename {file_only}")
            logic = Expert

        area_rando = False
        connections: list[tuple[AreaDoor, AreaDoor]] = []
        with open(filename) as file:
            for line in file:
                if " - - - " in line:
                    # item placement
                    loc_name, item_name = line.strip().split(" - - - ")
                    self.game_state_locations[loc_name]["item"] = all_items[item_name]
                elif " << >> " in line:
                    # area connection
                    area_rando = True
                    door_a, door_b = line.strip().split(" << >> ")
                    _area_a, door_name_a = door_a.split(" ")
                    _area_b, door_name_b = door_b.split(" ")
                    connections.append((area_doors[door_name_a], area_doors[door_name_b]))
        if len(connections) == 0:
            connections = VanillaAreas()

        game = Game(logic, self.empty_locations, area_rando, connections)
        self.loadout = Loadout(game)

    def pickup_location(self, loc_name: str) -> None:
        was_in_logic = self.query(loc_name)
        if not was_in_logic:
            print(f"{loc_name} was not in logic")
        item = self.game_state_locations[loc_name]["item"]
        if item:
            self.loadout.append(item)
            self.game_state_locations[loc_name]["item"] = None
            # TODO: save undo information
            print(f"picked up {item[0]} from {loc_name}")
        else:
            print(f"There was no item in {loc_name}")
        if loc_name not in spacePortLocs:
            self.loadout.append(Items.spaceDrop)

    def list_locations(self) -> list[str]:
        """ accessible locations that still have an item in them """
        tr: list[str] = []
        _, _, accessible_locations = solve(self.loadout.game, self.loadout)
        for loc in accessible_locations:
            if self.game_state_locations[loc["fullitemname"]]["item"]:
                tr.append(loc["fullitemname"])
        return tr

    def query(self, loc_name: str) -> bool:
        """ is this location in logic? """
        _, _, accessible_locations = solve(self.loadout.game, self.loadout)
        return self.loadout.game.all_locations[loc_name] in accessible_locations


def main() -> None:
    t = Tracker()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        t.set_spoiler(sys.argv[1])
    else:
        print("give path to spoiler: python tracker.py spoilers/SubEDA4939087.sfc.spoiler.txt")
        exit(1)

    print("commands: list, exit, q <loc_name>, <loc_name>")
    command = ""
    while command.lower() != "exit":
        command = input("> ")
        if command.lower() == "list":
            results = t.list_locations()
            for loc_name in results:
                print(loc_name)
        elif command.lower() == "exit":
            pass
        elif len(command) > 2 and command.lower().startswith("q "):
            loc_name_input = command[2:]
            name_results = t.loc_names_from_input(loc_name_input)
            if len(name_results) == 1:
                in_logic = t.query(name_results[0])
                print(f"{name_results[0]} is {'not ' if not in_logic else ''}in logic")
            else:
                print(f"unrecognized location name: {command}")
                if len(name_results):
                    print(f"one of these? {', '.join(name_results)}")
        else:
            name_results = t.loc_names_from_input(command)
            if len(name_results) == 1:
                t.pickup_location(name_results[0])
            else:
                print(f"unrecognized location name: {command}")
                if len(name_results):
                    print(f"one of these? {', '.join(name_results)}")


if __name__ == "__main__":
    main()
