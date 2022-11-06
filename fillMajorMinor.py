from typing import Optional
import random

from fillInterface import ItemLists
from item_data import Item, items_unpackable
from location_data import Location

# this will not update any of the parameters it is given
# but it will return an item to place at a location

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


def initItemLists() -> ItemLists:
    earlyItemList = [Missile,
                     Morph,
                     GravityBoots]
    progressionItemList = [Super,
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
                           Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy]
    eTankList = [Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy]
    extraItemList = [Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
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
                     LargeAmmo, LargeAmmo, LargeAmmo]
    return earlyItemList, progressionItemList, eTankList, extraItemList


def placementAlg(availableLocations: list[Location],
                 locArray: list[Location],
                 loadout: list[Item],
                 itemLists: ItemLists) -> Optional[tuple[Location, Item]]:

    assert len(availableLocations), "placement algorithm received 0 available locations"

    earlyItemList, progressionItemList, eTankList, extraItemList = itemLists
    for torpedoSearch in availableLocations :
        # print("Searching for Torpedo Bay: ",torpedoSearch['fullitemname'])
        if torpedoSearch['fullitemname'] == "Torpedo Bay" :
            # print("          found Torpedo Bay")
            placeItem = random.choice([Missile, Morph])
            # print(availableLocations[0][0]," - - - ",placeItem[0])
            placeLocation = torpedoSearch
            return placeLocation, placeItem

    from_items = (
        earlyItemList if len(earlyItemList) else (
            progressionItemList if len(progressionItemList) else (
                eTankList if len(eTankList) else (
                    extraItemList
                )
            )
        )
    )

    if from_items is extraItemList:
        valid_locations = availableLocations
    else:  # not extraItemList
        # load majors
        valid_locations = [
            loc
            for loc in availableLocations
            if (loc['fullitemname'] in majorLocs)
        ]
        if len(valid_locations) == 0 and (Morph in loadout):
            for sandySearch in locArray:
                # print("Searching for Sandy Cache: ", sandySearch['fullitemname'])
                if sandySearch['fullitemname'] == "Sandy Cache":
                    valid_locations.append(sandySearch)
                    availableLocations.append(sandySearch)
                    break
        if len(valid_locations) == 0:
            return None  # fail

    return random.choice(valid_locations), random.choice(from_items)
