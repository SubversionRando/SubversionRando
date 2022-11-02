import random

from item_data import Items, Item

# this will not update any of the parameters it is given
# but it will return an item to place at a location


# itemLists should contain
# [0] earlyItemList
# [1] lowPowerList
# [2] highPowerList
# [3] extraItemList
ItemLists = tuple[list[Item], list[Item], list[Item], list[Item]]


def initItemLists() -> ItemLists:
    earlyItemList = [Items.Missile,
                     Items.Morph,
                     Items.GravityBoots]
    lowPowerList = [Items.Super,
                    Items.Speedball,
                    Items.Bombs,
                    Items.HiJump,
                    Items.GravitySuit,
                    Items.DarkVisor,
                    Items.Wave,
                    Items.SpeedBooster,
                    Items.SpaceJump,
                    Items.Charge,
                    Items.Energy, Items.Energy, Items.Energy, Items.Energy, Items.Energy]
    highPowerList = [Items.Grapple,
                     Items.PowerBomb,
                     Items.Varia,
                     Items.Ice,
                     Items.MetroidSuit,
                     Items.Screw,
                     Items.Spazer,
                     Items.Plasma,
                     Items.Hypercharge]
    extraItemList = [Items.Xray,
                     Items.DamageAmp, Items.DamageAmp, Items.DamageAmp,
                     Items.DamageAmp, Items.DamageAmp, Items.DamageAmp,
                     Items.ChargeAmp, Items.ChargeAmp, Items.ChargeAmp,
                     Items.ChargeAmp, Items.ChargeAmp, Items.ChargeAmp,
                     Items.Refuel, Items.Refuel, Items.Refuel, Items.Refuel, Items.Refuel, Items.Refuel, Items.Refuel,
                     Items.Energy, Items.Energy, Items.Energy, Items.Energy,
                     Items.Energy, Items.Energy, Items.Energy, Items.Energy, Items.Energy,
                     Items.Energy, Items.Energy, Items.Energy, Items.Energy,
                     Items.SpaceJumpBoost, Items.SpaceJumpBoost, Items.SpaceJumpBoost, Items.SpaceJumpBoost,
                     Items.SpaceJumpBoost, Items.SpaceJumpBoost, Items.SpaceJumpBoost, Items.SpaceJumpBoost,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.SmallAmmo, Items.SmallAmmo, Items.SmallAmmo,
                     Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo,
                     Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo,
                     Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo,
                     Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo,
                     Items.LargeAmmo, Items.LargeAmmo, Items.LargeAmmo]
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
