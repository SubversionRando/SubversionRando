from collections import defaultdict, deque
from copy import deepcopy
from difflib import get_close_matches
import os
import sys

from connection_data import AreaDoor, VanillaAreas, area_doors
from game import Game
from item_data import Item, Items, all_items
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logic_presets import casual, expert, medium
from solver import solve
from trick import Trick

# TODO: archives right and left, front and back
# TODO: sensor maintenance top and bottom (sensor top, sensor bot)
# TODO: docking port 4 omega o, and 3 is gamma y g
# TODO: spore spawn, kraid, draygon
# TODO: impact crater (doesn't need "Accel Charge" - there's only 1 item in that room)
# TODO: mining site alpha a
# TODO: armory cache b beta, gamma g y
# TODO: sandy burrow top and bottom
# TODO: shrines last word (penumbra, fervor)
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
    undo_stack: deque[tuple[Location, Item]]

    def __init__(self) -> None:
        logic = casual
        area_rando = False
        area_connections = VanillaAreas()

        self.empty_locations = pullCSV()
        self.game_state_locations = deepcopy(self.empty_locations)
        game = Game(logic, self.empty_locations, area_rando, area_connections)
        self.loadout = Loadout(game)

        self.undo_stack = deque()

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
        logic: frozenset[Trick]
        if file_only[3] == "C":
            logic = casual
        elif file_only[3] == "E":
            logic = expert
        else:
            print(f"can't find logic letter in filename {file_only}")
            logic = expert

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
            print(f" - {loc_name} was not in logic - ")
        item = self.game_state_locations[loc_name]["item"]
        if item:
            self.loadout.append(item)
            self.game_state_locations[loc_name]["item"] = None
            # save undo information
            self.undo_stack.append((self.game_state_locations[loc_name], item))
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

    def undo(self) -> None:
        if len(self.undo_stack):
            loc, item = self.undo_stack.pop()
            loc["item"] = item
            self.loadout.contents[item] -= 1
            print(f"put {item[0]} back in {loc['fullitemname']}")
        else:
            print("nothing to undo")

    def switch_logic(self, logic: frozenset[Trick]) -> None:
        self.loadout.game.logic = logic


def main() -> None:
    t = Tracker()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        t.set_spoiler(sys.argv[1])
    else:
        print("give path to spoiler: python tracker.py spoilers/SubEDA4939087.sfc.spoiler.txt")
        exit(1)

    print("commands: list, exit, q <loc_name>, <loc_name>, undo, logic")
    command = ""
    while command.lower() != "exit":
        command = input("> ")
        if command.lower() == "list":
            results = t.list_locations()
            for loc_name in results:
                print(loc_name)
        elif command.lower() == "exit":
            pass
        elif command.lower() == "undo":
            t.undo()
        elif command.lower().startswith("logic ") and len(command) > 6:
            if command[6].lower() == "c":
                print("switching logic to casual")
                t.switch_logic(casual)
            elif command[6].lower() == "e":
                print("switching logic to expert")
                t.switch_logic(expert)
            elif command[6].lower() in {"m", "u"}:
                print("switching logic to medium")
                t.switch_logic(medium)
            else:
                print(f"unknown logic: {command[6:]}")
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
