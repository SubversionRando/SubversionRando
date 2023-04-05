import random
from typing import Optional

from connection_data import AreaDoor
from fillInterface import FillAlgorithm
from item_data import Item, Items
from loadout import Loadout
from location_data import Location, spacePortLocs, majorLocs, eTankLocs
from solver import solve

_minor_logic_items = {
    Items.DamageAmp: 6,
    Items.AccelCharge: 6,
    Items.Energy: 16,
    Items.SpaceJumpBoost: 8,
    Items.SmallAmmo: 12,
    Items.LargeAmmo: 18
}
""" minors placed with logic """

_minor_non_logic_items = {
    Items.Refuel: 7,
    Items.SmallAmmo: 26,
}
""" items placed without logic """

_unique_items: frozenset[Item] = frozenset([
    Items.Missile,
    Items.Morph,
    Items.GravityBoots,
    Items.Super,
    Items.Grapple,
    Items.PowerBomb,
    Items.Speedball,
    Items.Bombs,
    Items.HiJump,
    Items.Aqua,
    Items.DarkVisor,
    Items.Wave,
    Items.SpeedBooster,
    Items.Spazer,
    Items.Varia,
    Items.Ice,
    Items.MetroidSuit,
    Items.Plasma,
    Items.Screw,
    Items.SpaceJump,
    Items.Charge,
    Items.Hypercharge,
    Items.Xray,
])


class FillAssumed(FillAlgorithm):
    connections: list[tuple[AreaDoor, AreaDoor]]

    prog_items: list[Item]
    extra_items: list[Item]
    itemLists: list[list[Item]]

    def __init__(self,
                 connections: list[tuple[AreaDoor, AreaDoor]]) -> None:
        self.connections = connections

        self.prog_items = sorted(_unique_items)  # sort because iterating through set will not be the same every time
        assert len(self.prog_items) == len(set(self.prog_items)), "duplicate majors?"
        for it, n in _minor_logic_items.items():
            self.prog_items.extend([it for _ in range(n)])

        self.extra_items = []
        for it, n in _minor_non_logic_items.items():
            self.extra_items.extend([it for _ in range(n)])

        self.itemLists = [self.prog_items, self.extra_items]

    def _get_accessible_locations(self, loadout: Loadout) -> list[Location]:
        _, _, locs = solve(loadout.game, loadout)
        return locs

    def _get_available_locations(self, loadout: Loadout) -> list[Location]:
        return [loc for loc in self._get_accessible_locations(loadout) if loc["item"] is None]

    def _get_empty_locations(self, all_locations: dict[str, Location]) -> list[Location]:
        return [loc for loc in all_locations.values() if loc["item"] is None]

    def transform_spaceport(self, available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """
        transform the distribution of locations to work against spaceport front-loading

        because 1 progression item in space port
        will lead to more progression items in spaceport
        """
        if item_to_place in _unique_items:
            distribution = available_locations.copy()
            for loc in available_locations:
                if (
                    (loc["fullitemname"] == "Torpedo Bay" and item_to_place == Items.GravityBoots) or

                    # if the locking item is already placed, then it's safe to put progression in spaceport
                    (loc["fullitemname"] == "Extract Storage" and (
                        (Items.PowerBomb not in self.prog_items) or (
                            (Items.MetroidSuit not in self.prog_items) and
                            (Items.Hypercharge not in self.prog_items) and
                            ((Items.Ice not in self.prog_items) or (Items.Super not in self.prog_items))
                        )
                    )) or
                    (loc["fullitemname"] == "Ready Room" and Items.Super not in self.prog_items) or
                    (loc["fullitemname"] in {"Forward Battery", "Aft Battery"} and Items.Morph not in self.prog_items) or
                    (loc["fullitemname"] in {"Docking Port 3", "Docking Port 4"} and Items.Grapple not in self.prog_items) or
                    loc["fullitemname"] not in spacePortLocs
                ):
                    # number of copies can be tuned
                    distribution.append(loc)
                    if item_to_place in {Items.Morph, Items.GravityBoots, Items.Missile}:
                        distribution.append(loc)
                        distribution.append(loc)
            return distribution
        return available_locations

    @staticmethod
    def transform_mmb(available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """ transform the distribution of locations for major minor bias """
        tr: list[Location] = []
        for loc in available_locations:
            if item_to_place in _unique_items and loc["fullitemname"] in majorLocs:
                for _ in range(30):
                    tr.append(loc)
            elif item_to_place not in _unique_items and loc["fullitemname"] not in majorLocs:
                for _ in range(5):
                    tr.append(loc)
            else:
                tr.append(loc)
        return tr

    @staticmethod
    def transform_mm(available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """ transform the distribution of locations for major minor """
        major = item_to_place in _unique_items or item_to_place == Items.Energy
        tr: list[Location] = []
        for loc in available_locations:
            location_major = (loc["fullitemname"] in majorLocs or loc["fullitemname"] in eTankLocs)
            if major and location_major:
                tr.append(loc)
            elif (not major) and (not location_major):
                tr.append(loc)
        return tr

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        from_items = (
            self.prog_items if len(self.prog_items) else (
                self.extra_items
            )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

        if loadout.game.options.fill_choice == "MM" and Items.Morph in from_items:
            # major/minor and haven't placed morph yet
            item_to_place = Items.Morph
        else:
            item_to_place = random.choice(from_items)

        # If Missile is placed before Super, it's very likely that
        # Super will be in Torpedo Bay or some other really early place.
        # So this makes sure that Super is placed before Missile.
        # Consider disabling this in door rando (when Super can't open pink door).
        if item_to_place == Items.Missile:
            if Items.Super in from_items:
                item_to_place = Items.Super
        #         print("Super placed before Missile")
        #     else:
        #         print("Missile placed before Super")

        from_items.remove(item_to_place)

        if from_items is self.prog_items:
            loadout = Loadout(loadout.game)
            for item in from_items:
                loadout.append(item)
            available_locations = self._get_available_locations(loadout)
        else:  # extra
            available_locations = self._get_empty_locations(loadout.game.all_locations)
        if len(available_locations) == 0:
            return None

        if loadout.game.options.fill_choice == "B":
            available_locations = self.transform_mmb(available_locations, item_to_place)
        elif loadout.game.options.fill_choice == "MM":
            available_locations = self.transform_mm(available_locations, item_to_place)
        if len(available_locations) == 0:
            return None

        available_locations = self.transform_spaceport(available_locations, item_to_place)

        # This magic number 2 could be an option for "How loaded do you want the spaceport to be?"
        # (lower number means more progression items in spaceport)
        return random.choice(available_locations), item_to_place

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        pass  # removed in placement function
