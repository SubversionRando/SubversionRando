import random

from item_data import Item, items_unpackable

#this will not update any of the parameters it is given
#but it will return an item to place at a location

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


# itemLists should contain
# [0] earlyItemList
# [1] lowPowerList
# [2] highPowerList
# [3] extraItemList
ItemLists = tuple[list[Item], list[Item], list[Item], list[Item]]


def initItemLists() -> ItemLists:
    earlyItemList = [Missile,
                     Morph,
                     GravityBoots]
    lowPowerList = [Super,
                    Speedball,
                    Bombs,
                    HiJump,
                    GravitySuit,
                    DarkVisor,
                    Wave,
                    SpeedBooster,
                    SpaceJump,
                    Charge,
                    Energy, Energy, Energy, Energy, Energy]
    highPowerList = [Grapple,
                     PowerBomb,
                     Varia,
                     Ice,
                     MetroidSuit,
                     Screw,
                     Spazer,
                     Plasma,
                     Hypercharge]
    extraItemList = [Xray,
                     DamageAmp, DamageAmp, DamageAmp,
                     DamageAmp, DamageAmp, DamageAmp,
                     ChargeAmp, ChargeAmp, ChargeAmp,
                     ChargeAmp, ChargeAmp, ChargeAmp,
                     Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
                     Energy, Energy, Energy, Energy,
                     Energy, Energy, Energy, Energy, Energy,
                     Energy, Energy, Energy, Energy,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
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
                     LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo]
    return earlyItemList, lowPowerList, highPowerList, extraItemList


def placementAlg(availableLocations,
                 locArray,
                 loadout,
                 itemLists: ItemLists) -> tuple[LocationData, Item]:
    earlyItemList, lowPowerList, highPowerList, extraItemList = itemLists

    if earlyItemList != [] and availableLocations != []:
        randomIndex = 0
        if len(earlyItemList) > 1:
            randomIndex = random.randint(0, len(earlyItemList)-1)
        placeItem = earlyItemList[randomIndex]
        randomIndex = 0
        if len(availableLocations) > 1:
            randomIndex = random.randint(0, len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    if earlyItemList == [] and lowPowerList != [] and availableLocations != []:
        randomIndex = 0
        if len(lowPowerList) > 1:
            randomIndex = random.randint(0, len(lowPowerList)-1)
        placeItem = lowPowerList[randomIndex]
        randomIndex = 0
        if len(availableLocations) > 1:
            randomIndex = random.randint(0, len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    if earlyItemList == [] and lowPowerList == [] and highPowerList != [] and availableLocations != []:
        randomIndex = 0
        if len(highPowerList) > 1:
            randomIndex = random.randint(0, len(highPowerList)-1)
        placeItem = highPowerList[randomIndex]
        randomIndex = 0
        if len(availableLocations) > 1:
            randomIndex = random.randint(0, len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    if earlyItemList == [] and lowPowerList == [] and highPowerList == [] and availableLocations != []:
        randomIndex = 0
        if len(extraItemList) > 1:
            randomIndex = random.randint(0, len(extraItemList)-1)
        placeItem = extraItemList[randomIndex]
        randomIndex = 0
        if len(availableLocations) > 1:
            randomIndex = random.randint(0, len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    return placeLocation, placeItem
