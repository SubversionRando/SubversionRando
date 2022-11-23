import random
from typing import Optional

from connection_data import AreaDoor
from fillInterface import FillAlgorithm
from item_data import Item, Items
from loadout import Loadout
from location_data import Location, spacePortLocs
from solver import solve

_minor_items = {
    Items.DamageAmp: 6,
    Items.ChargeAmp: 6,
    Items.Energy: 7,
    Items.Refuel: 7,
    Items.SpaceJumpBoost: 8,
    Items.SmallAmmo: 38,
    Items.LargeAmmo: 18
}
# TODO: verify item counts - I think there are not 18 energy tanks in vanilla subversion


class FillAssumed(FillAlgorithm):
    connections: list[tuple[AreaDoor, AreaDoor]]

    # earlyItemList: list[Item]
    prog_items: list[Item]
    extra_items: list[Item]
    itemLists: list[list[Item]]

    def __init__(self,
                 connections: list[tuple[AreaDoor, AreaDoor]]) -> None:
        self.connections = connections

        # self.earlyItemList = [
        #     Missile,
        #     Morph,
        #     GravityBoots
        # ]
        self.prog_items = [
            Items.Missile,
            Items.Morph,
            Items.GravityBoots,
            Items.Super,
            Items.Grapple,
            Items.PowerBomb,
            Items.Speedball,
            Items.Bombs,
            Items.HiJump,
            Items.GravitySuit,
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
            Items.Energy, Items.Energy, Items.Energy, Items.Energy, Items.Energy,
            Items.Energy, Items.Energy, Items.Energy, Items.Energy
        ]
        assert len([it for it in self.prog_items if it != Items.Energy]) + 1 == len(set(self.prog_items)), \
            "duplicate majors?"
        self.extra_items = []
        for it, n in _minor_items.items():
            self.extra_items.extend([it for _ in range(n)])

        self.itemLists = [self.prog_items, self.extra_items]

    def _get_accessible_locations(self, all_locations: list[Location], loadout: Loadout) -> list[Location]:
        _, _, locs = solve(all_locations, loadout.logic, self.connections, loadout)
        return locs

    def _get_available_locations(self, all_locations: list[Location], loadout: Loadout) -> list[Location]:
        return [loc for loc in self._get_accessible_locations(all_locations, loadout) if loc["item"] is None]

    def _get_empty_locations(self, all_locations: list[Location]) -> list[Location]:
        return [loc for loc in all_locations if loc["item"] is None]

    @staticmethod
    def _choose_location(locs: list[Location], spaceport_deprio: int) -> Location:
        """
        to work against spaceport front-loading,
        because 1 progression item in space port
        will lead to more progression items in spaceport
        """
        distribution = locs.copy()
        for _ in range(spaceport_deprio):
            for loc in locs:
                if loc["fullitemname"] not in spacePortLocs:
                    distribution.append(loc)
        return random.choice(distribution)

    def choose_placement(self,
                         availableLocations: list[Location],
                         locArray: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        from_items = (
            # self.earlyItemList if len(self.earlyItemList) else (
            self.prog_items if len(self.prog_items) else (
                self.extra_items
            )
            # )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

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
            loadout = Loadout(loadout.logic)
            for item in from_items:
                loadout.append(item)
            available_locations = self._get_available_locations(locArray, loadout)
        else:  # extra
            available_locations = self._get_empty_locations(locArray)
        if len(available_locations) == 0:
            return None

        # This magic number 2 could be an option for "How loaded do you want the spaceport to be?"
        # (lower number means more progression items in spaceport)
        return self._choose_location(available_locations, 2), item_to_place

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        pass  # removed in placement function
