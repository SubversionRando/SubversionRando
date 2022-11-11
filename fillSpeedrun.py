import random

from item_data import items_unpackable

#this will not update any of the parameters it is given
#but it will return an item to place at a location


(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable

#itemLists should contain
# [0] earlyItemList
# [1] progressionItemList
# [2] extraItemList


def initItemLists () :
    earlyItemList=[Missile,
                   Morph,
                   GravityBoots]
    progressionItemList=[Super,
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
                         Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy]
    extraItemList=[Hypercharge,
                   Xray,
                   DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,
                   ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,
                   Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,
                   Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,
                   SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,
                   SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo]
    return [earlyItemList,progressionItemList,extraItemList]

def placementAlg(availableLocations, locArray, loadout, itemLists) :
    earlyItemList=itemLists[0]
    progressionItemList=itemLists[1]
    extraItemList=itemLists[2]
    if availableLocations[0]['fullitemname'] == "TORPEDO BAY" :
        randomIndex = random.randint(0,1)
        firstItems = [Missile, Morph]
        placeItem = firstItems[randomIndex]
        #print(availableLocations[0][0]," - - - ",placeItem[0])

        
    if earlyItemList != [] and availableLocations != []:
        randomIndex=0
        if len(earlyItemList) > 1 :
            randomIndex = random.randint(0,len(earlyItemList)-1)
        placeItem = earlyItemList[randomIndex]
        randomIndex=0
        if len(availableLocations) > 1 :
            randomIndex = random.randint(0,len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    if earlyItemList == [] and progressionItemList != [] and availableLocations != [] :
        randomIndex=0
        if len(progressionItemList) > 1 :
            randomIndex = random.randint(0,len(progressionItemList)-1)
        placeItem = progressionItemList[randomIndex]
        randomIndex=0
        if len(availableLocations) > 1 :
            randomIndex = random.randint(0,len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    if earlyItemList == [] and progressionItemList == [] and availableLocations != []:
        randomIndex=0
        if len(extraItemList) > 1 :
            randomIndex = random.randint(0,len(extraItemList)-1)
        placeItem = extraItemList[randomIndex]
        randomIndex=0
        if len(availableLocations) > 1 :
            randomIndex = random.randint(0,len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    return [placeLocation, placeItem]
