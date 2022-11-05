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


majorLocs = ["Ocean Vent Supply Depot", #start of unique majors
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
             "Torpedo Bay", #end of unique majors
             "Sandy Burrow: ETank", #E Tanks
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


#itemLists should contain
# [0] earlyItemList
# [1] progressionItemList
# [2] ETankList
# [3] extraItemList


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
                         Hypercharge,
                         Xray,
                         Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy]
    eTankList=[Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy]
    extraItemList=[Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,
                   DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,
                   ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,
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
    return [earlyItemList,progressionItemList,eTankList,extraItemList]

def placementAlg(availableLocations, locArray, loadout, itemLists) :
    earlyItemList=itemLists[0]
    progressionItemList=itemLists[1]
    eTankList=itemLists[2]
    extraItemList=itemLists[3]
    for torpedoSearch in availableLocations :
        #print("Searching for Torpedo Bay: ",torpedoSearch['fullitemname'])
        if torpedoSearch['fullitemname'] == "Torpedo Bay" :
            #print("          found Torpedo Bay")
            randomIndex = random.randint(0,1)
            firstItems = [Missile, Morph]
            placeItem = firstItems[randomIndex]
            #print(availableLocations[0][0]," - - - ",placeItem[0])
            placeLocation = torpedoSearch
            return [placeLocation, placeItem]
        
    if earlyItemList != [] and availableLocations != []:
        loadMajors = []
        for loc in availableLocations :
            if (loc['fullitemname'] in majorLocs) :
                loadMajors.append(loc)
        if loadMajors == [] :
            for sandySearch in locArray :
                #print("Searching for Sandy Cache: ",sandySearch['fullitemname'])
                if (Morph in loadout) and sandySearch['fullitemname'] == "Sandy Cache" :
                    loadMajors.append(sandySearch)
                    availableLocations.append(sandySearch)
        if loadMajors == [] :
            return ["Fail","Fail"]
        randomIndex=0
        if len(earlyItemList) > 1 :
            randomIndex = random.randint(0,len(earlyItemList)-1)
        placeItem = earlyItemList[randomIndex]
        randomIndex=0
        if len(loadMajors) > 1 :
            randomIndex = random.randint(0,len(loadMajors)-1)
        placeLocation = loadMajors[randomIndex]

    if earlyItemList == [] and progressionItemList != [] and availableLocations != [] :
        loadMajors = []
        for loc in availableLocations :
            if (loc['fullitemname'] in majorLocs) :
                loadMajors.append(loc)
        if loadMajors == [] :
            return ["Fail","Fail"]
        randomIndex=0
        if len(progressionItemList) > 1 :
            randomIndex = random.randint(0,len(progressionItemList)-1)
        placeItem = progressionItemList[randomIndex]
        randomIndex=0
        if len(loadMajors) > 1 :
            randomIndex = random.randint(0,len(loadMajors)-1)
        placeLocation = loadMajors[randomIndex]

    if earlyItemList == [] and progressionItemList == [] and eTankList != [] and availableLocations != [] :
        loadMajors = []
        for loc in availableLocations :
            if (loc['fullitemname'] in majorLocs) :
                loadMajors.append(loc)
        if loadMajors == [] :
            return ["Fail","Fail"]
        randomIndex=0
        placeItem = eTankList[randomIndex]
        randomIndex=0
        if len(loadMajors) > 1 :
            randomIndex = random.randint(0,len(loadMajors)-1)
        placeLocation = loadMajors[randomIndex]

    if earlyItemList == [] and progressionItemList == [] and eTankList == [] and availableLocations != []:
        randomIndex=0
        if len(extraItemList) > 1 :
            randomIndex = random.randint(0,len(extraItemList)-1)
        placeItem = extraItemList[randomIndex]
        randomIndex=0
        if len(availableLocations) > 1 :
            randomIndex = random.randint(0,len(availableLocations)-1)
        placeLocation = availableLocations[randomIndex]

    return [placeLocation, placeItem]
