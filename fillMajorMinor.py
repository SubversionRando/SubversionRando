from typing import Optional, Union
import random
from connection_data import Connection

from fillInterface import FillAlgorithm
from item_data import Item, items_unpackable
from location_data import Location

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


majorLocs = ["Ocean Vent Supply Depot",  # start of unique majors
             "Sandy Cache",
             "Shrine Of The Penumbra",
             "Subterranean Burrow",
             "Archives: SpringBall",
             "Arena",
             "Grand Vault",
             "Harmonic Growth Enhancer",
             "West Spore Field",
             "Electromechanical Engine",
             "Fire's Bane Shrine",
             "Greater Inferno",
             "Magma Chamber",
             "Antelier",
             "Chamber Of Wind",
             "Crocomire's Lair",
             "Equipment Locker",
             "Weapon Research",
             "Armory Cache 2",
             "Syzygy Observatorium",
             "Shrine Of The Animate Spark",
             "Extract Storage",
             "Torpedo Bay",  # end of unique majors
             "Sandy Burrow: ETank",  # E Tanks
             "Sediment Flow",
             "Epiphreatic Crag",
             "Mezzanine Concourse",
             "Sensor Maintenance: ETank",
             "Trophobiotic Chamber",
             "Vulnar Caves Entrance",
             "Warrior Shrine: ETank",
             "Depressurization Valve",
             "Gymnasium",
             "Mining Cache",
             "Containment Area",
             "Water Garden",
             "Reliquary Access",
             "Summit Landing",
             "Ready Room"]


class FillMajorMinor(FillAlgorithm):
    earlyItemList: list[Item]
    progressionItemList: list[Item]
    eTankList: list[Item]
    extraItemList: list[Item]

    itemLists: list[list[Item]]

    def __init__(self) -> None:
        self.earlyItemList = [
            Missile,
            Morph,
            GravityBoots
        ]
        self.progressionItemList = [
            Super,
            Grapple,
            PowerBomb,
            Speedball,
            Bombs,
            HiJump,
            GravitySuit,
            DarkVisor,
            Wave,
            SpeedBooster,
            Spazer,
            Varia,
            Ice,
            MetroidSuit,
            Plasma,
            Screw,
            SpaceJump,
            Charge,
            Hypercharge,
            Xray,
            Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy
        ]
        self.eTankList = [Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy]
        self.extraItemList = [
            Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
            DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp,
            ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo
        ]
        self.itemLists = [self.earlyItemList, self.progressionItemList, self.eTankList, self.extraItemList]

    def choose_placement(self,
                         availableLocations: list[Location],
                         locArray: list[Location],
                         loadout: list[Union[Item, Connection]]) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        assert len(availableLocations), "placement algorithm received 0 available locations"

        for torpedoSearch in availableLocations :
            # print("Searching for Torpedo Bay: ", torpedoSearch['fullitemname'])
            if torpedoSearch['fullitemname'] == "Torpedo Bay" :
                # print("          found Torpedo Bay")
                placeItem = random.choice([Missile, Morph])
                # print(availableLocations[0], " - - - ", placeItem)
                placeLocation = torpedoSearch
                return placeLocation, placeItem

        from_items = (
            self.earlyItemList if len(self.earlyItemList) else (
                self.progressionItemList if len(self.progressionItemList) else (
                    self.eTankList if len(self.eTankList) else (
                        self.extraItemList
                    )
                )
            )
        )

        if from_items is self.extraItemList:
            valid_locations = availableLocations
        else:  # not extraItemList
            # load majors
            valid_locations = [
                loc
                for loc in availableLocations
                if (loc['fullitemname'] in majorLocs)
            ]
            if from_items is self.earlyItemList and len(valid_locations) == 0 and (Morph in loadout):
                for sandySearch in locArray:
                    # print("Searching for Sandy Cache: ", sandySearch['fullitemname'])
                    if sandySearch['fullitemname'] == "Sandy Cache":
                        # print("   ---   appending sandy cache")
                        valid_locations.append(sandySearch)
                        availableLocations.append(sandySearch)
                        break
            if len(valid_locations) == 0:
                return None  # fail

        return random.choice(valid_locations), random.choice(from_items)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        for each_list in self.itemLists:
            try:
                i = each_list.index(item)
                each_list.pop(i)
                break
            except ValueError:
                # not in this list
                pass
