from collections import defaultdict, deque
from copy import deepcopy
from difflib import get_close_matches
import os
import sys

from connection_data import AreaDoor, VanillaAreas, area_doors
from game import CypherItems, Game, GameOptions
from item_data import Item, Items, all_items
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logic_presets import casual, expert, medium
from solver import required_doors, solve
from trick import Trick
from trick_data import Tricks, trick_name_lookup

_name_aliases = {
    "Warrior Shrine: AmmoTank Top": "Warrior Shrine: Top",
    "Warrior Top": "Warrior Shrine: Top",
    "Warrior Shrine: AmmoTank Bottom": "Warrior Shrine: Bottom",
    "Warrior Bottom": "Warrior Shrine: Bottom",
    "Warrior Shrine: ETank": "Warrior Shrine: Middle",
    "Warrior Middle": "Warrior Shrine: Middle",
    "Briar: AmmoTank": "Briar: Bottom",
    "Briar: SJBoost": "Briar: Top",
    "Archives: Right": "Archives: Front",
    "Archives: Left": "Archives: Back",
    "Sensor Top": "Sensor Maintenance: Top",
    "Sensor Bottom": "Sensor Maintenance: Bottom",
    "Docking Port: Omega": "Docking Port 4",
    "Docking Port: O": "Docking Port 4",
    "Docking Port: Gamma": "Docking Port 3",
    "Docking Port: G": "Docking Port 3",
    "Docking Port: Y": "Docking Port 3",
    "Spore Spawn": "Harmonic Growth Enhancer",
    "SpoSpo": "Harmonic Growth Enhancer",
    "Kraid": "Shrine Of The Penumbra",
    "Draygon": "Greater Inferno",
    "Mining Site Alpha": "Mining Site 1",
    "Mining Site A": "Mining Site 1",
    "Armory Cache Beta": "Armory Cache 2",
    "Armory Cache B": "Armory Cache 2",
    "Armory Cache Gamma": "Armory Cache 3",
    "Armory Cache G": "Armory Cache 3",
    "Armory Cache Y": "Armory Cache 3",
    "Armory 2": "Armory Cache 2",
    "Armory 3": "Armory Cache 3",
    "Armory B": "Armory Cache 2",
    "Armory C": "Armory Cache 3",
    "Penumbra": "Shrine Of The Penumbra",
    "Fervor": "Shrine Of Fervor",
    "Animate Spark": "Shrine Of The Animate Spark",
    "Burrow Top": "Sandy Burrow: Top",
    "Burrow Bottom": "Sandy Burrow: Bottom",
    "Swords": "Path Of Swords",
    "Central Left": "Central Corridor: Left",
    "Central Right": "Central Corridor: Right",
    "Main Hive Chamber": "Hive Main Chamber",
    "Ocean Top": "Ocean Shore: Top",
    "Ocean Bottom": "Ocean Shore: Bottom",
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
    logic_from_spoiler: frozenset[Trick]

    def __init__(self) -> None:
        logic = casual
        area_rando = False
        area_connections = VanillaAreas()

        self.empty_locations = pullCSV()
        self.game_state_locations = deepcopy(self.empty_locations)
        options = GameOptions(logic, area_rando, "D", True, False, CypherItems.NotRequired)
        game = Game(options, self.empty_locations, area_connections, 0)
        self.loadout = Loadout(game)

        self.undo_stack = deque()
        self.logic_from_spoiler = logic

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
        logic_from_spoiler: set[Trick] = set()

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
                elif line.startswith('    "') and line.strip().endswith('",'):
                    end_quote_i = line.index('"', 6)
                    trick_name = line[5:end_quote_i]
                    logic_from_spoiler.add(getattr(Tricks, trick_name))

        if len(connections) == 0:
            connections = VanillaAreas()

        frz_logic_from_spoiler = frozenset(logic_from_spoiler)
        if frz_logic_from_spoiler == casual:
            print("found logic: casual")
        elif frz_logic_from_spoiler == medium:
            print("found logic: medium")
        elif frz_logic_from_spoiler == expert:
            print("found logic: expert")
        else:
            print("found logic: custom")

        self.logic_from_spoiler = frz_logic_from_spoiler
        options = GameOptions(frz_logic_from_spoiler, area_rando, "D", True, False, CypherItems.NotRequired)
        game = Game(options, self.empty_locations, connections, 0)
        self.loadout = Loadout(game)

    def pickup_location(self, loc_name: str) -> None:
        was_in_logic, _, _ = self.query(loc_name)
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

    def query(self, loc_name: str) -> tuple[bool, list[str], list[str]]:
        """ is this location in logic? """
        _, _, accessible_locations = solve(self.loadout.game, self.loadout)
        in_logic = self.loadout.game.all_locations[loc_name] in accessible_locations

        if in_logic:
            required_tricks: list[str] = []
            original_logic = self.loadout.game.options.logic
            for excluded_trick in self.loadout.game.options.logic:
                temp_logic = original_logic - {excluded_trick}
                self.loadout.game.options.logic = temp_logic
                _, _, accessible_locations = solve(self.loadout.game, self.loadout)
                if self.loadout.game.all_locations[loc_name] not in accessible_locations:
                    required_tricks.append(trick_name_lookup[excluded_trick])
            self.loadout.game.options.logic = original_logic

            req_doors = required_doors(self.loadout, loc_name)

            return True, required_tricks, req_doors
        else:
            return False, [], []

    def undo(self) -> None:
        if len(self.undo_stack):
            loc, item = self.undo_stack.pop()
            loc["item"] = item
            self.loadout.contents[item] -= 1
            print(f"put {item[0]} back in {loc['fullitemname']}")
        else:
            print("nothing to undo")

    def switch_logic(self, logic: frozenset[Trick]) -> None:
        self.loadout.game.options.logic = logic


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
            elif command[6].lower() == "q":
                print("switching logic to spoiler")
                t.switch_logic(t.logic_from_spoiler)
            else:
                print(f"unknown logic: {command[6:]}")
        elif len(command) > 2 and command.lower().startswith("q "):
            loc_name_input = command[2:]
            name_results = t.loc_names_from_input(loc_name_input)
            if len(name_results) == 1:
                in_logic, tricks, doors = t.query(name_results[0])
                print(f"{name_results[0]} is {'not ' if not in_logic else ''}in logic")
                if in_logic:
                    print(f"      tricks required: {tricks}")
                    print(f"      doors required: {doors}")
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
