#Casual logic updater
#updates unusedLocations

def updateLogic (unusedLocations, locArray, loadout) :
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
             b"\x23\xef",
             b"\x23\xef",
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
    exitSpacePort = (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and (GravitySuit in loadout)
    pinkDoor = (Missile in loadout) or (Super in loadout)
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    vulnar = jumpAble and pinkDoor
    pirateLab = vulnar and canUseBombs and (((Speedball in loadout) or (SpeedBooster in loadout)) or ((DarkVisor in loadout) and canUsePB))
    canFly = (Bombs in loadout) or (SpaceJump in loadout)
    upperVulnar = jumpAble and canUsePB and (canFly or (vulnar and (SpeedBooster in loadout)))
    depthsL = (Varia in loadout) and (Bombs in loadout) and ((underwater and (Super in loadout)) or (vulnar and (Wave in loadout)))
    hive = (Varia in loadout) and (Super in loadout) and vulnar and canUseBombs and ((depthsL and (canUsePB or (Ice in loadout))) or ((Wave in loadout) and (SpeedBooster in loadout)) or ((SpeedBooster in loadout) and canUsePB))
    geothermal = hive and canUsePB and (Ice in loadout)
    eastLomyr = vulnar and canUsePB and (Bombs in loadout) and ((SpeedBooster in loadout) or (pirateLab and (GravitySuit in loadout) and (Super in loadout)))
    oceanDepths = underwater and ((pinkDoor and (Morph in loadout) and (DarkVisor in loadout)) or (Super in loadout))
    #print("Updating logic...")
    for thisLoc in unusedLocations :
        #thisLoc is a row. thisLoc[4] is the logic
        #for each location, check that location names match
        if thisLoc[0] == locArray[0][0] : #IMPACT CRATER
            thisLoc[4] = exitSpacePort and (Morph in loadout) and (Spazer in loadout) and ((HiJump in loadout) or (SpeedBooster in loadout) or (SpaceJump in loadout))
        if thisLoc[0] == locArray[1][0] : #SUBTERRANEAN BURROW
            thisLoc[4] = exitSpacePort and ((Morph in loadout) or (GravityBoots in loadout))
        if thisLoc[0] == locArray[2][0] : #SANDY CACHE
            thisLoc[4] = jumpAble and (Missile in loadout)
        if thisLoc[0] == locArray[3][0] : #SUBMARINE NEST
            thisLoc[4] = underwater and pinkDoor
        if thisLoc[0] == (locArray[4][0]) : #SHRINE OF THE PENUMBRA
            thisLoc[4] = jumpAble and pinkDoor and (GravitySuit in loadout) and (canUsePB or (canUseBombs and (DarkVisor in loadout)))
        if thisLoc[0] == locArray[5][0] : #BENTHIC CACHE ACCESS
            thisLoc[4] = jumpAble and underwater and canUseBombs and (Super in loadout) and (PowerBomb in loadout)
        if thisLoc[0] == locArray[6][0] : #BENTHIC CACHE
            thisLoc[4] = jumpAble and underwater and canUseBombs and (Super in loadout) and (PowerBomb in loadout)
        if thisLoc[0] == locArray[7][0] : #OCEAN VENT SUPPLY DEPOT
            thisLoc[4] = jumpAble and underwater and (Morph in loadout) and ((Super in loadout) or (Screw in loadout))
        if thisLoc[0] == locArray[8][0] : #SEDIMENT FLOW
            thisLoc[4] = jumpAble and underwater and (Super in loadout)
        if thisLoc[0] == locArray[9][0] : #HARMONIC GROWTH ENHANCER
            thisLoc[4] = jumpAble and pinkDoor and canUseBombs and ((Wave in loadout) or (DarkVisor in loadout))
        if thisLoc[0] == locArray[10][0] : #UPPER VULNAR POWER NODE
            thisLoc[4] = jumpAble and canUsePB and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[11][0] : #GRAND VAULT
            thisLoc[4] = jumpAble and (Grapple in loadout)
        if thisLoc[0] == locArray[12][0] : #CISTERN
            thisLoc[4] = vulnar and canUseBombs
        if thisLoc[0] == locArray[13][0] : #WARRIOR SHRINE MID
            thisLoc[4] = vulnar and canUsePB
        if thisLoc[0] == locArray[14][0] : #VULNAR CAVES ENTRANCE
            thisLoc[4] = vulnar
        if thisLoc[0] == locArray[15][0] : #CRYPT
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout)
        if thisLoc[0] == locArray[16][0] : #ARCHIVES FRONT
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout)
        if thisLoc[0] == locArray[17][0] : #ARCHIVES BACK
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout)
        if thisLoc[0] == locArray[18][0] : #SENSOR MAINTENANCE FRONT
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout)
        if thisLoc[0] == locArray[19][0] : #ERIBIUM APPARATUS ROOM
            thisLoc[4] = vulnar and canUseBombs and (DarkVisor in loadout)
        if thisLoc[0] == locArray[20][0] : #HOT SPRING
            thisLoc[4] = vulnar and canUseBombs and (Wave in loadout)
        if thisLoc[0] == locArray[21][0] : #EPIPHREATIC CRAG
            thisLoc[4] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[22][0] : #MEZZANINE CONCOURSE
            thisLoc[4] = upperVulnar
        if thisLoc[0] == locArray[23][0] : #GREATER INFERNO
            thisLoc[4] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[24][0] : #BURNING DEPTHS CACHE
            thisLoc[4] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout) and ((Spazer in loadout) or (Wave in loadout))
        if thisLoc[0] == locArray[25][0] : #MINING CACHE
            thisLoc[4] = depthsL and canUseBombs
        if thisLoc[0] == locArray[26][0] : #INFESTED PASSAGE
            thisLoc[4] = hive
        if thisLoc[0] == locArray[27][0] : #FIRE'S BOON SHRINE
            thisLoc[4] = hive and (Wave in loadout) and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[28][0] : #FIRE'S BANE SHRINE
            thisLoc[4] = hive and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[29][0] : #ANCIENT SHAFT
            thisLoc[4] = hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[30][0] : #GYMNASIUM
            thisLoc[4] = hive and (Grapple in loadout) and canUsePB and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[31][0] : #ELECTROMECHANICAL ENGINE
            thisLoc[4] = geothermal
        if thisLoc[0] == locArray[32][0] : #DEPRESSURIZATION VALVE
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout)
        if thisLoc[0] == locArray[33][0] : #LOADING DOCK STORAGE AREA
            thisLoc[4] = pirateLab
        if thisLoc[0] == locArray[34][0] : #CONTAINMENT AREA
            thisLoc[4] = pirateLab and (GravitySuit in loadout) and ((MetroidSuit in loadout) or (Screw in loadout))
        if thisLoc[0] == locArray[35][0] : #BRIAR TOP
            thisLoc[4] = eastLomyr and canUsePB
        if thisLoc[0] == locArray[36][0] : #SHRINE OF FERVOR
            thisLoc[4] = eastLomyr
        if thisLoc[0] == locArray[37][0] : #CHAMBER OF WIND
            thisLoc[4] = eastLomyr and pinkDoor and (SpeedBooster in loadout)
        if thisLoc[0] == locArray[38][0] : #WATER GARDEN
            thisLoc[4] = eastLomyr and pinkDoor and (SpeedBooster in loadout)
        if thisLoc[0] == locArray[39][0] : #CROCOMIRE'S ENERGY STATION
            thisLoc[4] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
        if thisLoc[0] == locArray[40][0] : #WELLSPRING CACHE
            thisLoc[4] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
        if thisLoc[0] == locArray[41][0] : #FROZEN LAKE WALL
            thisLoc[4] = upperVulnar and canFly and (Plasma in loadout)
        if thisLoc[0] == locArray[42][0] : #GRAND PROMENADE
            thisLoc[4] = upperVulnar
        if thisLoc[0] == locArray[43][0] : #SUMMIT LANDING
            thisLoc[4] = upperVulnar and canUseBombs and (Speedball in loadout)
        if thisLoc[0] == locArray[44][0] : #SNOW CACHE
            thisLoc[4] = upperVulnar and canUseBombs and (Plasma in loadout)
        if thisLoc[0] == locArray[45][0] : #RELIQUARY ACCESS
            thisLoc[4] = upperVulnar and canUseBombs and (Super in loadout) and (DarkVisor in loadout)
        if thisLoc[0] == locArray[46][0] : #SYZYGY OBSERVATORIUM
            thisLoc[4] = upperVulnar and (((Super in loadout) and (Varia in loadout) and ((MetroidSuit in loadout) or (Hypercharge in loadout))) or (Screw in loadout))
        if thisLoc[0] == locArray[47][0] : #ARMORY CACHE 2
            thisLoc[4] = upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout))
        if thisLoc[0] == locArray[48][0] : #ARMORY CACHE 3
            thisLoc[4] = upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout))
        if thisLoc[0] == locArray[49][0] : #DRAWING ROOM
            thisLoc[4] = upperVulnar and (Super in loadout) and (SpaceJump in loadout)
        if thisLoc[0] == locArray[50][0] : #IMPACT CRATER OVERLOOK
            thisLoc[4] = canFly and canUseBombs and (canUsePB or (Super in loadout))
        if thisLoc[0] == locArray[51][0] : #MAGMA LAKE CACHE
            thisLoc[4] = depthsL
        if thisLoc[0] == locArray[52][0] : #SHRINE OF THE ANIMATE SPARK
            thisLoc[4] = hive and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[53][0] : #DOCKING PORT OMEGA
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[54][0] : #READY ROOM
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[55][0] : #TORPEDO BAY
            thisLoc[4] = True
        if thisLoc[0] == locArray[56][0] : #EXTRACT STORAGE
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[57][0] : #IMPACT CRATER ALCOVE
            thisLoc[4] = jumpAble and canFly and canUseBombs
        if thisLoc[0] == locArray[58][0] : #OCEAN SHORE BOTTOM
            thisLoc[4] = exitSpacePort
        if thisLoc[0] == locArray[59][0] : #OCEAN SHORE TOP
            thisLoc[4] = jumpAble and (canFly or (HiJump in loadout) or ((SpeedBooster in loadout) and (GravitySuit in loadout))) 
        if thisLoc[0] == locArray[60][0] : #SANDY BURROW TOP
            thisLoc[4] = underwater and canUseBombs
        if thisLoc[0] == locArray[61][0] : #SUBMARINE ALCOVE 
            thisLoc[4] = underwater and (Morph in loadout) and (DarkVisor in loadout) and pinkDoor
        if thisLoc[0] == locArray[62][0] : #SEDIMENT FLOOR
            thisLoc[4] = underwater and (Super in loadout) and (Morph in loadout)
        if thisLoc[0] == locArray[63][0] : #SANDY GULLY
            thisLoc[4] = underwater and (Super in loadout)
        if thisLoc[0] == locArray[64][0] : #HALL OF THE ELDERS
            thisLoc[4] = vulnar and (Morph in loadout) and ((Missile in loadout) or (GravitySuit in loadout))
        if thisLoc[0] == locArray[65][0] : #WARRIOR SHRINE LOW RIGHT
            thisLoc[4] = vulnar and (Morph in loadout) and (Missile in loadout) and ((Bombs in loadout) or (Wave in loadout))
        if thisLoc[0] == locArray[66][0] : #WARRIOR SHRINE TOP LEFT
            thisLoc[4] = vulnar and canUseBombs and ((Missile in loadout) or (GravitySuit in loadout)) and ((Bombs in loadout) or (Wave in loadout))
        if thisLoc[0] == locArray[67][0] : #PATH OF SWORDS
            thisLoc[4] = vulnar and canUseBombs
        if thisLoc[0] == locArray[68][0] : #AUXILIARY PUMP ROOM
            thisLoc[4] = vulnar and canUseBombs
        if thisLoc[0] == locArray[69][0] : #MONITORING STATION
            thisLoc[4] = vulnar and (Morph in loadout) and (Speedball in loadout)
        if thisLoc[0] == locArray[70][0] : #SENSOR MAINTENANCE BACK
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout) and (Missile in loadout)
        if thisLoc[0] == locArray[71][0] : #CAUSEWAY OVERLOOK
            thisLoc[4] = vulnar and canUseBombs
        if thisLoc[0] == locArray[72][0] : #PLACID POOL
            thisLoc[4] = vulnar and canUsePB and (Ice in loadout) and ((Varia in loadout) or ((DarkVisor in loadout) and (Wave in loadout)) or ((DarkVisor in loadout) and (Speedball in loadout) or (SpeedBooster in loadout)))
        if thisLoc[0] == locArray[73][0] : #BLAZING CHASM
            thisLoc[4] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)                  
        if thisLoc[0] == locArray[74][0] : #GENERATOR MANIFOLD
            thisLoc[4] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)                  
        if thisLoc[0] == locArray[75][0] : #FIERY CROSSING CACHE
            thisLoc[4] = depthsL and canUsePB and (Super in loadout)
        if thisLoc[0] == locArray[76][0] : #DARK CREVICE CACHE
            thisLoc[4] = depthsL and canUseBombs
        if thisLoc[0] == locArray[77][0] : #ANCIENT BASIN
            thisLoc[4] = hive
        if thisLoc[0] == locArray[78][0] : #CENTRAL CORRIDOR RIGHT
            thisLoc[4] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[79][0] : #BRIAR BOTTOM
            thisLoc[4] = eastLomyr and (Morph in loadout)
        if thisLoc[0] == locArray[80][0] : #ICY FLOW
            thisLoc[4] = upperVulnar and (SpeedBooster in loadout) and (Plasma in loadout)
        if thisLoc[0] == locArray[81][0] : #ICE CAVE
            thisLoc[4] = upperVulnar and (Plasma in loadout)
        if thisLoc[0] == locArray[82][0] : #ANTECHAMBER
            thisLoc[4] = upperVulnar and canUsePB
        if thisLoc[0] == locArray[83][0] : #EDDY CHANNELS
            thisLoc[4] = underwater and (Speedball in loadout) and ((pinkDoor and (DarkVisor in loadout)) or (Super in loadout))
        if thisLoc[0] == locArray[84][0] : #TRAM TO SUZI ISLAND
            thisLoc[4] = underwater and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Spazer in loadout)
        if thisLoc[0] == locArray[85][0] : #PORTICO (idk Suzi)
            thisLoc[4] = hive and canUsePB and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[86][0] : #TOWER ROCK LOOKOUT (suzi)
            thisLoc[4] = hive and canUsePB and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[87][0] : #REEF NOOK (suzi)
            thisLoc[4] = hive and canUsePB and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[88][0] : #SALINE CACHE (suzi)
            thisLoc[4] = hive and canUsePB and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[89][0] : #ENERVATION CHAMBER (SUZI)
            thisLoc[4] = hive and canUsePB and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[90][0] : #WEAPON LOCKER (cautious logic)
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[91][0] : #AFT BATTERY (cautious logic)
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[92][0] : #FORWARD BATTERY (cautious logic)
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[93][0] : #GANTRY (cautious logic)
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[94][0] : #GARDEN CANAL (cautious logic)
            thisLoc[4] = eastLomyr and canUsePB and (Spazer in loadout)
        if thisLoc[0] == locArray[95][0] : #SANDY BURROW BOTTOM
            thisLoc[4] = underwater and (Morph in loadout)
        if thisLoc[0] == locArray[96][0] : #TROPHOBIOTIC CHAMBER
            thisLoc[4] = vulnar and (Morph in loadout) and (Speedball in loadout)
        if thisLoc[0] == locArray[97][0] : #WASTE PROCESSING
            thisLoc[4] = pirateLab and (SpeedBooster in loadout) and ((Wave in loadout) or canUsePB)
        if thisLoc[0] == locArray[98][0] : #GRAND CHASM
            thisLoc[4] = upperVulnar and canUseBombs and (Screw in loadout) and (SpaceJump in loadout)
        if thisLoc[0] == locArray[99][0] : #MINING SITE 1 (ALPHA)
            thisLoc[4] = canUseBombs and ((vulnar and (Wave in loadout)) or depthsL)
        if thisLoc[0] == locArray[100][0] : #COLOSSEUM (GT)
            thisLoc[4] = depthsL and (Charge in loadout)
        if thisLoc[0] == locArray[101][0] : #LAVA POOL
            thisLoc[4] = depthsL and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[102][0] : #HIVE MAIN CHAMBER
            thisLoc[4] = hive
        if thisLoc[0] == locArray[103][0] : #CROSSWAY CACHE
            thisLoc[4] = hive and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[104][0] : #SLAG HEAP
            thisLoc[4] = hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[105][0] : #HYDRODYNAMIC CHAMBER
            thisLoc[4] = pirateLab and (Spazer in loadout) and ((HiJump in loadout) or (GravitySuit in loadout))
        if thisLoc[0] == locArray[106][0] : #CENTRAL CORRIDOR LEFT
            thisLoc[4] = vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[107][0] : #RESTRICTED AREA
            thisLoc[4] = vulnar and canUseBombs and (MetroidSuit in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[108][0] : #FOUNDRY
            thisLoc[4] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[109][0] : #NORAK ESCARPMENT
            thisLoc[4] = eastLomyr and (canFly or (SpeedBooster in loadout))
        if thisLoc[0] == locArray[110][0] : #GLACIER'S REACH
            thisLoc[4] = upperVulnar and canUseBombs and (Plasma in loadout)
        if thisLoc[0] == locArray[111][0] : #SITTING ROOM
            thisLoc[4] = upperVulnar and canUsePB and (Speedball in loadout)
        if thisLoc[0] == locArray[112][0] : #SUZI RUINS MAP STATION ACCESS
            thisLoc[4] = hive and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[113][0] : #OBSCURED VESTIBULE (SUZI)
            thisLoc[4] = hive and (GravitySuit in loadout) and (Grapple in loadout) and (Screw in loadout) and (SpaceJump in loadout) and (SpeedBooster in loadout) and (Charge in loadout)
        if thisLoc[0] == locArray[114][0] : #DOCKING PORT 3 (UPSILON)
            thisLoc[4] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc[0] == locArray[115][0] : #ARENA
            thisLoc[4] = vulnar and (Morph in loadout) and (Missile in loadout) and ((Bombs in loadout) or (Wave in loadout))
        if thisLoc[0] == locArray[116][0] : #WEST SPORE FIELD
            thisLoc[4] = vulnar and canUseBombs and (Super in loadout) and (Wave in loadout) and (Speedball in loadout)
        if thisLoc[0] == locArray[117][0] : #MAGMA CHAMBER
            thisLoc[4] = depthsL and ((Charge in loadout) or (MetroidSuit in loadout))
        if thisLoc[0] == locArray[118][0] : #EQUIPMENT LOCKER
            thisLoc[4] = pirateLab and canUseBombs
        if thisLoc[0] == locArray[119][0] : #ANTILIER
            thisLoc[4] = pirateLab and ((HiJump in loadout) or (GravitySuit in loadout))
        if thisLoc[0] == locArray[120][0] : #WEAPON RESEARCH
            thisLoc[4] = vulnar and canUseBombs and (Wave in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc[0] == locArray[121][0] : #CROCOMIRE'S LAIR
            thisLoc[4] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
    return unusedLocations
