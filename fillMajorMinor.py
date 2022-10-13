import random

#this will not update any of the parameters it is given
#but it will return an item to place at a location

#itemLists should contain
# [0] earlyItemList
# [1] progressionItemList
# [2] ETankList
# [3] extraItemList

Missile = ["Missile",
           b"\xdb\xee",
           b"\x2f\xef",
           b"\x83\xef",
           b"\x00"]
Super = ["Super Missile",
         b"\xdf\xee",
         b"\x33\xef",
         b"\x87\xef",
         b"\x00"]
PowerBomb = ["Power Bomb",
             b"\xe3\xee",
             b"\x37\xef",
             b"\x8b\xef",
             b"\x00"]
Morph = ["Morph Ball",
         b"\x23\xef",
         b"\x77\xef",
         b"\xcb\xef",
         b"\x00"]
GravityBoots = ["Gravity Boots",
                b"\x40\xfd",
                b"\x40\xfd",
                b"\x40\xfd",
                b"\x00"]   
Speedball = ["Speed Ball",
             b"\x03\xef",
             b"\x57\xef",
             b"\xab\xef",
             b"\x00"]
Bombs = ["Bombs",
         b"\xe7\xee",
         b"\x3b\xef",
         b"\x8f\xef",
         b"\x00"]
HiJump = ["HiJump",
          b"\xf3\xee",
          b"\x47\xef",
          b"\x9b\xef",
          b"\x00"]
GravitySuit = ["Gravity Suit",
               b"\x0b\xef",
               b"\x5f\xef",
               b"\xb3\xef",
               b"\x00"]
DarkVisor = ["Dark Visor",
             b"\xb0\xfd",
             b"\xb0\xfd",
             b"\xb0\xfd",
             b"\x00"]
Wave = ["Wave Beam",
        b"\xfb\xee",
        b"\x4f\xef",
        b"\xa3\xef",
        b"\x00"]
SpeedBooster = ["Speed Booster",
                b"\xf7\xee",
                b"\x4b\xef",
                b"\x9f\xef",
                b"\x00"]
Spazer = ["Spazer",
          b"\xff\xee",
          b"\x53\xef",
          b"\xa7\xef",
          b"\x00"]
Varia = ["Varia Suit",
         b"\x07\xef",
         b"\x5b\xef",
         b"\xaf\xef",
         b"\x00"]
Ice = ["Ice Beam",
       b"\xef\xee",
       b"\x43\xef",
       b"\x97\xef",
       b"\x00"]
Grapple = ["Grapple Beam",
           b"\x17\xef",
           b"\x6b\xef",
           b"\xbf\xef",
           b"\x00"]
MetroidSuit = ["Metroid Suit",
               b"\x20\xfe",
               b"\x20\xfe",
               b"\x20\xfe",
               b"\x00"]
Plasma = ["Plasma Beam",
          b"\x13\xef",
          b"\x67\xef",
          b"\xbb\xef",
          b"\x00"]
Screw = ["Screw Attack",
         b"\x1f\xef",
         b"\x73\xef",
         b"\xc7\xef",
         b"\x00"]
Hypercharge = ["Hypercharge",
               b"\x80\xf7",
               b"\x80\xf7",
               b"\x80\xf7",
               b"\x00"]
Charge = ["Charge Beam",
          b"\xeb\xee",
          b"\x3f\xef",
          b"\x93\xef",
          b"\x00"]
Xray = ["X-Ray Scope",
        b"\x0f\xef",
        b"\x63\xef",
        b"\xb7\xef",
        b"\x00"]
SpaceJump = ["Space Jump",
             b"\x1b\xef",
             b"\x6f\xef",
             b"\xc3\xef",
             b"\x00"]
Energy = ["Energy Tank",
          b"\xd7\xee",
          b"\x2b\xef",
          b"\x7f\xef",
          b"\x00"]
Refuel = ["Refuel Tank",
          b"\x27\xef",
          b"\x7b\xef",
          b"\xcf\xef",
          b"\x00"]
SmallAmmo = ["Small Ammo",
             b"\x00\xf9",
             b"\x04\xf9",
             b"\x08\xf9",
             b"\x05"]
LargeAmmo = ["Large Ammo",
             b"\x00\xf9",
             b"\x04\xf9",
             b"\x08\xf9",
             b"\x0a"]
DamageAmp = ["Damage Amp",
             b"\x7e\xf8",
             b"\x7e\xf8",
             b"\x7e\xf8",
             b"\x00"]
ChargeAmp = ["Charge Amp",
             b"\xa0\xf0",
             b"\xa0\xf0",
             b"\xa0\xf0",
             b"\x00"]
SpaceJumpBoost = ["Space Jump Boost",
                  b"\xc0\xfc",
                  b"\xc0\xfc",
                  b"\xc0\xfc",
                  b"\x00"]
spaceDrop = ["Space Drop","","","",""]
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
