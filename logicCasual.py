from item_data import Item, items_unpackable
from location_data import Location

# Casual logic updater
# updates unusedLocations

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


def updateLogic(unusedLocations: list[Location],
                locArray: list[Location],
                loadout: list[Item]) -> list[Location]:

    exitSpacePort = (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and (GravitySuit in loadout)
    pinkDoor = (Missile in loadout) or (Super in loadout)
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    breakIce = (Plasma in loadout) or ((Hypercharge in loadout) and (Charge in loadout))
    vulnar = jumpAble and pinkDoor
    pirateLab = vulnar and canUseBombs and (((Speedball in loadout) or (SpeedBooster in loadout)) or ((DarkVisor in loadout) and canUsePB))
    canFly = (Bombs in loadout) or (SpaceJump in loadout)
    upperVulnar = jumpAble and ((canUsePB and canFly) or (vulnar and (SpeedBooster in loadout)))
    depthsL = (Varia in loadout) and (Bombs in loadout) and ((underwater and (Super in loadout)) or (vulnar and (Wave in loadout)))
    hive = (Varia in loadout) and ((Super in loadout) or (upperVulnar and underwater and breakIce)) and vulnar and canUseBombs and ((depthsL and (canUsePB or (Ice in loadout))) or ((Wave in loadout) and (SpeedBooster in loadout)) or ((SpeedBooster in loadout) and canUsePB))
    geothermal = (hive and canUsePB and (Ice in loadout)) or (upperVulnar and underwater and breakIce and canUsePB and (Screw in loadout))
    eastLomyr = vulnar and canUsePB and (Bombs in loadout) and ((SpeedBooster in loadout) or (pirateLab and (GravitySuit in loadout) and (Super in loadout)))
    oceanDepths = underwater and ((pinkDoor and (Morph in loadout) and (DarkVisor in loadout)) or (Super in loadout))
    breakIce = (Plasma in loadout) or ((Hypercharge in loadout) and (Charge in loadout))
    suzi = underwater and (SpeedBooster in loadout) and (Grapple in loadout) and (Super in loadout) and canUsePB and (Wave in loadout)
    # onAndOff = ON varia ice PB graple OFF Hyper charge

    logic = {
        "Impact Crater: AccelCharge": (
            exitSpacePort and (Morph in loadout) and (Spazer in loadout) and (
                (HiJump in loadout) or (SpeedBooster in loadout) or (SpaceJump in loadout)
            )
        ),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

        # thisLoc is a row. thisLoc['inlogic'] is the logic
        # for each location, check that location names match
        if thisLoc['fullitemname'] == "Impact Crater: AccelCharge":
            thisLoc['inlogic'] = exitSpacePort and (Morph in loadout) and (Spazer in loadout) and ((HiJump in loadout) or (SpeedBooster in loadout) or (SpaceJump in loadout))
        if thisLoc['fullitemname'] == "Subterranean Burrow":
            thisLoc['inlogic'] = exitSpacePort and ((Morph in loadout) or (GravityBoots in loadout))
        if thisLoc['fullitemname'] == "Sandy Cache":
            thisLoc['inlogic'] = jumpAble and (Missile in loadout)
        if thisLoc['fullitemname'] == "Submarine Nest":
            thisLoc['inlogic'] = underwater and pinkDoor
        if thisLoc['fullitemname'] == "Shrine Of The Penumbra":
            thisLoc['inlogic'] = jumpAble and pinkDoor and (GravitySuit in loadout) and (canUsePB or (canUseBombs and (DarkVisor in loadout)))
        if thisLoc['fullitemname'] == "Benthic Cache Access":
            thisLoc['inlogic'] = jumpAble and underwater and canUseBombs and (DarkVisor in loadout) and (Super in loadout) and (PowerBomb in loadout)
        if thisLoc['fullitemname'] == "Benthic Cache":
            thisLoc['inlogic'] = jumpAble and underwater and canUseBombs and (DarkVisor in loadout) and (Super in loadout)
        if thisLoc['fullitemname'] == "Ocean Vent Supply Depot":
            thisLoc['inlogic'] = jumpAble and underwater and (Morph in loadout) and (DarkVisor in loadout) and pinkDoor and ((Super in loadout) or (Screw in loadout) or (canUsePB and (MetroidSuit in loadout)))
        if thisLoc['fullitemname'] == "Sediment Flow":
            thisLoc['inlogic'] = jumpAble and underwater and (Super in loadout)
        if thisLoc['fullitemname'] == "Harmonic Growth Enhancer":
            thisLoc['inlogic'] = jumpAble and pinkDoor and canUseBombs and ((Wave in loadout) or (DarkVisor in loadout))
        if thisLoc['fullitemname'] == "Upper Vulnar Power Node":
            thisLoc['inlogic'] = vulnar and canUsePB and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc['fullitemname'] == "Grand Vault":
            thisLoc['inlogic'] = vulnar and (Grapple in loadout)
        if thisLoc['fullitemname'] == "Cistern":
            thisLoc['inlogic'] = vulnar and canUseBombs
        if thisLoc['fullitemname'] == "Warrior Shrine: ETank":
            thisLoc['inlogic'] = vulnar and canUsePB
        if thisLoc['fullitemname'] == "Vulnar Caves Entrance":
            thisLoc['inlogic'] = vulnar
        if thisLoc['fullitemname'] == "Crypt":
            thisLoc['inlogic'] = vulnar and canUseBombs
        if thisLoc['fullitemname'] == "Archives: SpringBall":  # yes it's actually Speed Ball, uses Spring data
            thisLoc['inlogic'] = vulnar and canUseBombs and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Archives: SJBoost":
            thisLoc['inlogic'] = vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout)
        if thisLoc['fullitemname'] == "Sensor Maintenance: ETank":  # front
            thisLoc['inlogic'] = vulnar and canUseBombs and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Eribium Apparatus Room":
            thisLoc['inlogic'] = vulnar and canUseBombs and (DarkVisor in loadout)
        if thisLoc['fullitemname'] == "Hot Spring":
            thisLoc['inlogic'] = vulnar and underwater and canUseBombs and (DarkVisor in loadout) and ((Wave in loadout) or (Varia in loadout))
        if thisLoc['fullitemname'] == "Epiphreatic Crag":
            thisLoc['inlogic'] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc['fullitemname'] == "Mezzanine Concourse":
            thisLoc['inlogic'] = upperVulnar
        if thisLoc['fullitemname'] == "Greater Inferno":
            thisLoc['inlogic'] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout) and ((SpeedBooster in loadout) or (Screw in loadout))
        if thisLoc['fullitemname'] == "Burning Depths Cache":
            thisLoc['inlogic'] = depthsL and canUsePB and ((Super in loadout) or breakIce) and (MetroidSuit in loadout) and ((SpeedBooster in loadout) or (Screw in loadout)) and ((Spazer in loadout) or (Wave in loadout))
        if thisLoc['fullitemname'] == "Mining Cache": 
            thisLoc['inlogic'] = vulnar and underwater and canUseBombs and (DarkVisor in loadout) and (Super in loadout)
        if thisLoc['fullitemname'] == "Infested Passage":
            thisLoc['inlogic'] = hive
        if thisLoc['fullitemname'] == "Fire's Boon Shrine":
            thisLoc['inlogic'] = (Wave in loadout) and ((hive and ((Ice in loadout) or (SpeedBooster in loadout))) or (eastLomyr and canUseBombs and underwater))
        if thisLoc['fullitemname'] == "Fire's Bane Shrine":
            thisLoc['inlogic'] = (hive and ((Ice in loadout) or (SpeedBooster in loadout))) or (eastLomyr and canUseBombs and underwater)
        if thisLoc['fullitemname'] == "Ancient Shaft":
            thisLoc['inlogic'] = hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout))
        if thisLoc['fullitemname'] == "Gymnasium":
            thisLoc['inlogic'] = (Grapple in loadout) and ((hive and canUsePB and ((Ice in loadout) or (SpeedBooster in loadout))) or (eastLomyr and canUseBombs and underwater))
        if thisLoc['fullitemname'] == "Electromechanical Engine":
            thisLoc['inlogic'] = geothermal
        if thisLoc['fullitemname'] == "Depressurization Valve":
            thisLoc['inlogic'] = geothermal and ((MetroidSuit in loadout) or ((Grapple in loadout) and (Screw in loadout)))
        if thisLoc['fullitemname'] == "Loading Dock Storage Area":
            thisLoc['inlogic'] = pirateLab
        if thisLoc['fullitemname'] == "Containment Area":
            thisLoc['inlogic'] = pirateLab and (GravitySuit in loadout) and ((MetroidSuit in loadout) or (Screw in loadout))
        if thisLoc['fullitemname'] == "Briar: SJBoost":  # top
            thisLoc['inlogic'] = eastLomyr and canUsePB
        if thisLoc['fullitemname'] == "Shrine Of Fervor":
            thisLoc['inlogic'] = eastLomyr
        if thisLoc['fullitemname'] == "Chamber Of Wind":
            thisLoc['inlogic'] = eastLomyr and pinkDoor and (SpeedBooster in loadout) and (canUseBombs or ((Screw in loadout) and (Speedball in loadout)))
        if thisLoc['fullitemname'] == "Water Garden":
            thisLoc['inlogic'] = eastLomyr and pinkDoor and (SpeedBooster in loadout)
        if thisLoc['fullitemname'] == "Crocomire's Energy Station":
            thisLoc['inlogic'] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
        if thisLoc['fullitemname'] == "Wellspring Cache":
            thisLoc['inlogic'] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
        if thisLoc['fullitemname'] == "Frozen Lake Wall: DamageAmp":
            thisLoc['inlogic'] = upperVulnar and breakIce
        if thisLoc['fullitemname'] == "Grand Promenade":
            thisLoc['inlogic'] = upperVulnar
        if thisLoc['fullitemname'] == "Summit Landing":
            thisLoc['inlogic'] = upperVulnar and canUseBombs and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Snow Cache":
            thisLoc['inlogic'] = upperVulnar and canUseBombs and breakIce
        if thisLoc['fullitemname'] == "Reliquary Access":
            thisLoc['inlogic'] = upperVulnar and canUseBombs and (Super in loadout) and (DarkVisor in loadout)
        if thisLoc['fullitemname'] == "Syzygy Observatorium":
            thisLoc['inlogic'] = upperVulnar and (((Super in loadout) and (Varia in loadout) and ((MetroidSuit in loadout) or (Hypercharge in loadout))) or (Screw in loadout))
        if thisLoc['fullitemname'] == "Armory Cache 2":
            thisLoc['inlogic'] = upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout))
        if thisLoc['fullitemname'] == "Armory Cache 3":
            thisLoc['inlogic'] = upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout))
        if thisLoc['fullitemname'] == "Drawing Room":
            thisLoc['inlogic'] = upperVulnar and (Super in loadout)
        if thisLoc['fullitemname'] == "Impact Crater Overlook":
            thisLoc['inlogic'] = canFly and canUseBombs and (canUsePB or (Super in loadout))
        if thisLoc['fullitemname'] == "Magma Lake Cache":
            thisLoc['inlogic'] = depthsL
        if thisLoc['fullitemname'] == "Shrine Of The Animate Spark":
            thisLoc['inlogic'] = suzi and canFly and (Hypercharge in loadout) and (Charge in loadout)
        if thisLoc['fullitemname'] == "Docking Port 4":  # (4 = letter Omega)
            thisLoc['inlogic'] = (((spaceDrop in loadout) is False) and (Grapple in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Ready Room":
            thisLoc['inlogic'] = (((spaceDrop in loadout) is False) and (Super in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Torpedo Bay":
            thisLoc['inlogic'] = True
        if thisLoc['fullitemname'] == "Extract Storage":
            thisLoc['inlogic'] = geothermal and canUsePB and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc['fullitemname'] == "Impact Crater Alcove":
            thisLoc['inlogic'] = jumpAble and canFly and canUseBombs
        if thisLoc['fullitemname'] == "Ocean Shore: bottom":
            thisLoc['inlogic'] = exitSpacePort
        if thisLoc['fullitemname'] == "Ocean Shore: top":
            thisLoc['inlogic'] = jumpAble and (canFly or (HiJump in loadout) or ((SpeedBooster in loadout) and (GravitySuit in loadout))) 
        if thisLoc['fullitemname'] == "Sandy Burrow: ETank": # top
            thisLoc['inlogic'] = underwater and canUseBombs
        if thisLoc['fullitemname'] == "Submarine Alcove":
            thisLoc['inlogic'] = underwater and (Morph in loadout) and (DarkVisor in loadout) and pinkDoor
        if thisLoc['fullitemname'] == "Sediment Floor":
            thisLoc['inlogic'] = underwater and (Morph in loadout) and ((Super in loadout) or (vulnar and (Varia in loadout) and canUseBombs))
        if thisLoc['fullitemname'] == "Sandy Gully":
            thisLoc['inlogic'] = underwater and (Super in loadout)
        if thisLoc['fullitemname'] == "Hall Of The Elders":
            thisLoc['inlogic'] = vulnar and (Morph in loadout) and ((Missile in loadout) or (GravitySuit in loadout))
        if thisLoc['fullitemname'] == "Warrior Shrine: AmmoTank bottom":
            thisLoc['inlogic'] = vulnar and (Morph in loadout) and (Missile in loadout) and ((Bombs in loadout) or (Wave in loadout))
        if thisLoc['fullitemname'] == "Warrior Shrine: AmmoTank top":
            thisLoc['inlogic'] = vulnar and canUseBombs and ((Missile in loadout) or (GravitySuit in loadout)) and ((Bombs in loadout) or (Wave in loadout))
        if thisLoc['fullitemname'] == "Path Of Swords":
            thisLoc['inlogic'] = vulnar and canUseBombs
        if thisLoc['fullitemname'] == "Auxiliary Pump Room":
            thisLoc['inlogic'] = vulnar and canUseBombs
        if thisLoc['fullitemname'] == "Monitoring Station":
            thisLoc['inlogic'] = vulnar and (Morph in loadout) and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Sensor Maintenance: AmmoTank":  # back
            thisLoc['inlogic'] = vulnar and canUseBombs and (Speedball in loadout) and (Missile in loadout)
        if thisLoc['fullitemname'] == "Causeway Overlook":
            thisLoc['inlogic'] = vulnar and canUseBombs
        if thisLoc['fullitemname'] == "Placid Pool":
            thisLoc['inlogic'] = vulnar and canUsePB and (Ice in loadout) and ((Varia in loadout) or ((DarkVisor in loadout) and (Wave in loadout)) or ((DarkVisor in loadout) and (Speedball in loadout) or
                                                                                                                                                        (SpeedBooster in loadout)))
        if thisLoc['fullitemname'] == "Blazing Chasm":
            thisLoc['inlogic'] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)
        if thisLoc['fullitemname'] == "Generator Manifold":
            thisLoc['inlogic'] = depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)
        if thisLoc['fullitemname'] == "Fiery Crossing Cache":
            thisLoc['inlogic'] = depthsL and canUsePB and (Super in loadout)
        if thisLoc['fullitemname'] == "Dark Crevice Cache":
            thisLoc['inlogic'] = depthsL and canUseBombs
        if thisLoc['fullitemname'] == "Ancient Basin":
            thisLoc['inlogic'] = hive
        if thisLoc['fullitemname'] == "Central Corridor: right":
            thisLoc['inlogic'] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc['fullitemname'] == "Briar: AmmoTank": # bottom
            thisLoc['inlogic'] = eastLomyr and (Morph in loadout)
        if thisLoc['fullitemname'] == "Icy Flow":
            thisLoc['inlogic'] = upperVulnar and (SpeedBooster in loadout) and breakIce
        if thisLoc['fullitemname'] == "Ice Cave":
            thisLoc['inlogic'] = upperVulnar and breakIce
        if thisLoc['fullitemname'] == "Antechamber":
            thisLoc['inlogic'] = upperVulnar and canUsePB
        if thisLoc['fullitemname'] == "Eddy Channels":
            thisLoc['inlogic'] = underwater and (Speedball in loadout) and ((pinkDoor and (DarkVisor in loadout)) or (Super in loadout))
        if thisLoc['fullitemname'] == "Tram To Suzi Island":
            thisLoc['inlogic'] = oceanDepths and canUsePB and (Super in loadout) and (Grapple in loadout) and (SpeedBooster in loadout) and (Spazer in loadout)
        if thisLoc['fullitemname'] == "Portico":
            thisLoc['inlogic'] = suzi
        if thisLoc['fullitemname'] == "Tower Rock Lookout":
            thisLoc['inlogic'] = suzi and canFly
        if thisLoc['fullitemname'] == "Reef Nook":
            thisLoc['inlogic'] = suzi and canFly
        if thisLoc['fullitemname'] == "Saline Cache":
            thisLoc['inlogic'] = suzi
        if thisLoc['fullitemname'] == "Enervation Chamber":
            thisLoc['inlogic'] = suzi and canFly and (Hypercharge in loadout) and (Charge in loadout)
        if thisLoc['fullitemname'] == "Weapon Locker":
            thisLoc['inlogic'] = (((spaceDrop in loadout) is False) and (Missile in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Aft Battery":  # CAUTIOUS LOGIC
            thisLoc['inlogic'] = (((spaceDrop in loadout) is False) and (Morph in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Forward Battery":  # CAUTIOUS LOGIC
            thisLoc['inlogic'] = geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
        if thisLoc['fullitemname'] == "Gantry":  # CAUTIOUS LOGIC
            thisLoc['inlogic'] = (((spaceDrop in loadout) is False) and (Missile in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Garden Canal":  # CAUTIOUS LOGIC
            thisLoc['inlogic'] = eastLomyr and canUsePB and (Spazer in loadout)
        if thisLoc['fullitemname'] == "Sandy Burrow: AmmoTank":  # bottom
            thisLoc['inlogic'] = underwater and (Morph in loadout) and pinkDoor
        if thisLoc['fullitemname'] == "Trophobiotic Chamber":
            thisLoc['inlogic'] = vulnar and (Morph in loadout) and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Waste Processing":
            thisLoc['inlogic'] = pirateLab and (SpeedBooster in loadout) and ((Wave in loadout) or canUsePB)
        if thisLoc['fullitemname'] == "Grand Chasm":
            thisLoc['inlogic'] = upperVulnar and canUseBombs and (Screw in loadout)
        if thisLoc['fullitemname'] == "Mining Site 1":  # (1 = letter Alpha)
            thisLoc['inlogic'] = canUseBombs and ((vulnar and underwater and (Wave in loadout)) or depthsL)
        if thisLoc['fullitemname'] == "Colosseum":  # GT
            thisLoc['inlogic'] = depthsL and (Charge in loadout)
        if thisLoc['fullitemname'] == "Lava Pool":
            thisLoc['inlogic'] = depthsL and (MetroidSuit in loadout) and canUsePB
        if thisLoc['fullitemname'] == "Hive Main Chamber":
            thisLoc['inlogic'] = hive
        if thisLoc['fullitemname'] == "Crossway Cache":
            thisLoc['inlogic'] = hive and ((Ice in loadout) or (SpeedBooster in loadout) or (eastLomyr and canUseBombs and (Wave in loadout)))
        if thisLoc['fullitemname'] == "Slag Heap":
            thisLoc['inlogic'] = hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout) or (eastLomyr and canUseBombs and (Wave in loadout)))
        if thisLoc['fullitemname'] == "Hydrodynamic Chamber":
            thisLoc['inlogic'] = pirateLab and (Spazer in loadout) and ((HiJump in loadout) or (GravitySuit in loadout))
        if thisLoc['fullitemname'] == "Central Corridor: left":
            thisLoc['inlogic'] = vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and ((canUsePB and (Wave in loadout)) or (Screw in loadout))))
        if thisLoc['fullitemname'] == "Restricted Area":
            thisLoc['inlogic'] = vulnar and canUseBombs and (MetroidSuit in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and ((canUsePB and (Wave in loadout)) or (Screw in loadout))))
        if thisLoc['fullitemname'] == "Foundry":
            thisLoc['inlogic'] = vulnar and canUseBombs and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc['fullitemname'] == "Norak Escarpment":
            thisLoc['inlogic'] = eastLomyr and (canFly or (SpeedBooster in loadout))
        if thisLoc['fullitemname'] == "Glacier's Reach":
            thisLoc['inlogic'] = upperVulnar and canUseBombs and breakIce
        if thisLoc['fullitemname'] == "Sitting Room":
            thisLoc['inlogic'] = upperVulnar and canUsePB and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Suzi Ruins Map Station Access":
            thisLoc['inlogic'] = suzi
        if thisLoc['fullitemname'] == "Obscured Vestibule": # Suzi
            thisLoc['inlogic'] = suzi
        if thisLoc['fullitemname'] == "Docking Port 3": # (3 = letter Gamma)
            thisLoc['inlogic'] = (((spaceDrop in loadout) == False) and (Grapple in loadout)) or ((spaceDrop in loadout) and geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Arena":
            thisLoc['inlogic'] = vulnar and (Morph in loadout) and (Missile in loadout) and ((Bombs in loadout) or (Screw in loadout) or (Wave in loadout))
        if thisLoc['fullitemname'] == "West Spore Field":
            thisLoc['inlogic'] = vulnar and canUseBombs and (Super in loadout) and (Wave in loadout) and (Speedball in loadout)
        if thisLoc['fullitemname'] == "Magma Chamber":
            thisLoc['inlogic'] = depthsL and ((Charge in loadout) or (MetroidSuit in loadout))
        if thisLoc['fullitemname'] == "Equipment Locker":
            thisLoc['inlogic'] = pirateLab and canUseBombs
        if thisLoc['fullitemname'] == "Antelier":  # spelled "Antilier" in subversion 1.1
            thisLoc['inlogic'] = pirateLab and ((HiJump in loadout) or (GravitySuit in loadout))
        if thisLoc['fullitemname'] == "Weapon Research":
            thisLoc['inlogic'] = vulnar and canUseBombs and (Wave in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB))
        if thisLoc['fullitemname'] == "Crocomire's Lair":
            thisLoc['inlogic'] = eastLomyr and (Super in loadout) and (SpeedBooster in loadout)
    return unusedLocations
