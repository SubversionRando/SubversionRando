from item_data import Item, items_unpackable
from location_data import Location

# Expert logic updater
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

    energyCount = 0
    for item in loadout:
        if item == Energy:
            energyCount += 1
    exitSpacePort = True
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and ((HiJump in loadout) or (GravitySuit in loadout))
    pinkDoor = (Missile in loadout) or (Super in loadout)
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    vulnar = jumpAble and pinkDoor
    pirateLab = vulnar and canUseBombs and (((Speedball in loadout) or (SpeedBooster in loadout) or (GravitySuit in loadout)) or ((DarkVisor in loadout) and (Wave in loadout) and canUsePB))
    canFly = (Bombs in loadout) or (SpaceJump in loadout)
    upperVulnar = jumpAble and (energyCount > 2) and ((canFly and canUsePB) or (vulnar and (SpeedBooster in loadout)))
    depthsL = (energyCount > 4) and (Bombs in loadout) and underwater and (Super in loadout)
    hive = (energyCount > 4) and (Super in loadout) and vulnar and canUseBombs and ((depthsL and (canUsePB or (Ice in loadout))) or ((Wave in loadout) and (SpeedBooster in loadout)) or ((SpeedBooster in loadout) and canUsePB and (energyCount > 6)))
    geothermal = (hive and canUsePB and (Ice in loadout)) or (upperVulnar and canUsePB and (Plasma in loadout) and ((MetroidSuit in loadout) or (Screw in loadout)))
    eastLomyr = (vulnar and (Morph in loadout) and (SpeedBooster in loadout)) or (pirateLab and underwater and (Bombs in loadout) and (Super in loadout)) or (geothermal and underwater and ((Screw in loadout) and ((MetroidSuit in loadout) or (Grapple in loadout))))
    oceanDepths = underwater and ((pinkDoor and (Morph in loadout) and (DarkVisor in loadout)) or (Super in loadout))
    suzi = jumpAble and (Super in loadout) and canUsePB and (Wave in loadout) and (GravitySuit in loadout) and (SpeedBooster in loadout) and (Grapple in loadout)
    # onAndOff = ON varia ice PB grapple OFF Hyper charge
    late_spaceport = (
        (spaceDrop in loadout) and
        geothermal and
        (Grapple in loadout) and
        (Screw in loadout) and
        (MetroidSuit in loadout)
    )

    logic = {
        "Impact Crater: AccelCharge":
            exitSpacePort and (Morph in loadout) and (Spazer in loadout) and ((HiJump in loadout) or (SpeedBooster in loadout) or canFly),
        "Subterranean Burrow":
            exitSpacePort and ((Morph in loadout) or (GravityBoots in loadout)),
        "Sandy Cache":
            jumpAble and (Missile in loadout) and ((Morph in loadout) or (GravitySuit in loadout)),
        "Submarine Nest":
            underwater and pinkDoor,
        "Shrine Of The Penumbra":
            jumpAble and pinkDoor and (GravitySuit in loadout) and (canUsePB or (canUseBombs and (DarkVisor in loadout))),
        "Benthic Cache Access":
            jumpAble and underwater and canUsePB and (Super in loadout),
        "Benthic Cache":
            jumpAble and underwater and canUseBombs and (Super in loadout),
        "Ocean Vent Supply Depot":
            jumpAble and underwater and (Morph in loadout) and ((Super in loadout) or (Screw in loadout)),
        "Sediment Flow":
            jumpAble and underwater and (Super in loadout),
        "Harmonic Growth Enhancer":
            jumpAble and pinkDoor and canUseBombs,
        "Upper Vulnar Power Node":
            vulnar and canUsePB and (Screw in loadout) and (MetroidSuit in loadout),
        "Grand Vault":
            vulnar and (Grapple in loadout),
        "Cistern":
            vulnar and canUseBombs,
        "Warrior Shrine: ETank":
            vulnar and canUsePB,
        "Vulnar Caves Entrance":
            vulnar,
        "Crypt":
            vulnar and canUseBombs and ((Wave in loadout) or (Bombs in loadout)),
        "Archives: SpringBall":  # yes it's actually Speed Ball, uses Spring data
            vulnar and (Speedball in loadout),
        "Archives: SJBoost":
            vulnar and (Speedball in loadout) and (SpeedBooster in loadout),
        "Sensor Maintenance: ETank":  # front
            vulnar and (Morph in loadout),
        "Eribium Apparatus Room":
            vulnar and canUseBombs and (DarkVisor in loadout),
        "Hot Spring":
            vulnar and (Morph in loadout) and (canUseBombs or (Super in loadout) or (Plasma in loadout)) and ((GravitySuit in loadout) or (Speedball in loadout)) and ((HiJump in loadout) or (Ice in loadout)),
        "Epiphreatic Crag":
            vulnar and canUseBombs and (GravitySuit in loadout) and (((DarkVisor in loadout) and (Wave in loadout)) or (pirateLab and canUsePB)),
        "Mezzanine Concourse":
            upperVulnar,
        "Greater Inferno":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout),
        "Burning Depths Cache":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout) and ((Spazer in loadout) or (Wave in loadout)),
        "Mining Cache":
            depthsL and canUseBombs,
        "Infested Passage":
            hive,
        "Fire's Boon Shrine":
            hive and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Fire's Bane Shrine":
            hive and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Ancient Shaft":
            hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Gymnasium":
            hive and (Grapple in loadout) and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Electromechanical Engine":
            geothermal and (Grapple in loadout),
        "Depressurization Valve":
            geothermal and (((Grapple in loadout) and (Screw in loadout)) or (MetroidSuit in loadout)),
        "Loading Dock Storage Area":
            pirateLab,
        "Containment Area":
            pirateLab and underwater and ((MetroidSuit in loadout) or (Screw in loadout)),
        "Briar: SJBoost":  # top
            eastLomyr and canUsePB,
        "Shrine Of Fervor":
            eastLomyr,
        "Chamber Of Wind":
            eastLomyr and pinkDoor and (SpeedBooster in loadout) and (canUseBombs or ((Screw in loadout) and (Speedball in loadout))),
        "Water Garden":
            eastLomyr and (SpeedBooster in loadout),
        "Crocomire's Energy Station":
            eastLomyr and (Super in loadout) and (SpeedBooster in loadout),
        "Wellspring Cache":
            eastLomyr and underwater and (Super in loadout) and (SpeedBooster in loadout),
        "Frozen Lake Wall: DamageAmp":
            upperVulnar and canFly and (Plasma in loadout),
        "Grand Promenade":
            upperVulnar,
        "Summit Landing":
            upperVulnar and canUseBombs,
        "Snow Cache":
            upperVulnar and canUseBombs and (Plasma in loadout),
        "Reliquary Access":
            upperVulnar and canUseBombs and (Super in loadout) and (DarkVisor in loadout),
        "Syzygy Observatorium":
            upperVulnar and (((Super in loadout) and (Varia in loadout) and ((MetroidSuit in loadout) or (Hypercharge in loadout))) or (Screw in loadout)),
        "Armory Cache 2":
            upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout)),
        "Armory Cache 3":
            upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout)),
        "Drawing Room":
            upperVulnar and (Super in loadout),
        "Impact Crater Overlook":
            canFly and canUseBombs and (canUsePB or (Super in loadout)),
        "Magma Lake Cache":
            depthsL and (Ice in loadout),
        "Shrine Of The Animate Spark":
            hive and suzi and (Hypercharge in loadout),
        "Docking Port 4":  # (4 = letter Omega)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or late_spaceport,
        "Ready Room":
            ((spaceDrop not in loadout) and (Super in loadout)) or late_spaceport,
        "Torpedo Bay":
            (spaceDrop not in loadout) or (late_spaceport),
        "Extract Storage":
            ((spaceDrop not in loadout) and canUsePB) or late_spaceport,
        "Impact Crater Alcove":
            jumpAble and canFly and canUseBombs,
        "Ocean Shore: bottom":
            exitSpacePort,
        "Ocean Shore: top":
            jumpAble,
        "Sandy Burrow: ETank":  # top
            underwater and (((GravitySuit in loadout) and ((Screw in loadout) or canUseBombs)) or ((Speedball in loadout) and canUseBombs)),
        "Submarine Alcove":
            underwater and (Morph in loadout) and (((DarkVisor in loadout) and pinkDoor) or (Super in loadout) or (vulnar and underwater and (energyCount > 4) and canUseBombs and (Speedball in loadout))),
        "Sediment Floor":
            underwater and (Morph in loadout) and ((Super in loadout) or (vulnar and underwater and (energyCount > 4) and canUseBombs and (Speedball in loadout))),
        "Sandy Gully":
            underwater and (Super in loadout),
        "Hall Of The Elders":
            vulnar and (Morph in loadout) and ((Missile in loadout) or (GravitySuit in loadout) or (underwater and (Speedball in loadout))),
        "Warrior Shrine: AmmoTank bottom":
            vulnar and (Morph in loadout) and (Missile in loadout),
        "Warrior Shrine: AmmoTank top":
            vulnar and (Morph in loadout) and (Missile in loadout) and canUseBombs,
        "Path Of Swords":
            vulnar and (canUseBombs or ((Morph in loadout) and (Screw in loadout))),
        "Auxiliary Pump Room":
            vulnar and canUseBombs,
        "Monitoring Station":
            vulnar and (Morph in loadout),
        "Sensor Maintenance: AmmoTank":  # back
            vulnar and canUseBombs,
        "Causeway Overlook":
            vulnar and canUseBombs,
        "Placid Pool":
            vulnar and canUsePB and ((geothermal and (Screw in loadout) and energyCount > 4) or ((Super in loadout) and (((energyCount > 4) or (Wave in loadout)) or ((DarkVisor in loadout) and ((Speedball in loadout) or (SpeedBooster in loadout)))))),
        "Blazing Chasm":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout),
        "Generator Manifold":
            (depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout)) or (geothermal and (Screw in loadout)),
        "Fiery Crossing Cache":
            depthsL and canUsePB,
        "Dark Crevice Cache":
            depthsL and canUseBombs and canFly,
        "Ancient Basin":
            hive,
        "Central Corridor: right":
            vulnar and canUseBombs and (((DarkVisor in loadout) and (Wave in loadout)) or (pirateLab and (canUsePB or (underwater and (Screw in loadout)))) or (eastLomyr and canUsePB and underwater)),
        "Briar: AmmoTank":  # bottom
            eastLomyr and (Morph in loadout),
        "Icy Flow":
            upperVulnar and (SpeedBooster in loadout) and (Plasma in loadout),
        "Ice Cave":
            upperVulnar and (Plasma in loadout),
        "Antechamber":
            upperVulnar and canUsePB,
        "Eddy Channels":
            underwater and (Speedball in loadout) and ((pinkDoor and (DarkVisor in loadout)) or (Super in loadout) or (vulnar and (energyCount > 4) and canUseBombs)),
        "Tram To Suzi Island":
            underwater and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Spazer in loadout),
        "Portico":
            suzi,
        "Tower Rock Lookout":
            suzi and canFly,
        "Reef Nook":
            suzi and canFly,
        "Saline Cache":
            suzi and canFly,
        "Enervation Chamber":
            suzi and (Hypercharge in loadout),
        "Weapon Locker":
            ((spaceDrop not in loadout) and (Missile in loadout)) or late_spaceport,
        "Aft Battery":
            ((spaceDrop not in loadout) and (Morph in loadout)) or late_spaceport,
        "Forward Battery":
            geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout),
        "Gantry":
            ((spaceDrop not in loadout) and (Missile in loadout)) or late_spaceport,
        "Garden Canal":
            eastLomyr and canUsePB and (Spazer in loadout),
        "Sandy Burrow: AmmoTank":  # bottom
            underwater and (Morph in loadout) and ((Speedball in loadout) or (GravitySuit in loadout)),
        "Trophobiotic Chamber":
            vulnar and (Morph in loadout) and (Speedball in loadout),
        "Waste Processing":
            (SpeedBooster in loadout) and ((vulnar and (Wave in loadout)) or (pirateLab and canUsePB)),
        "Grand Chasm":
            upperVulnar and canUseBombs and (Screw in loadout),
        "Mining Site 1":  # (1 = letter Alpha)
            canUseBombs and (vulnar or depthsL),
        "Colosseum":  # GT
            depthsL and (Varia in loadout) and (Charge in loadout),
        "Lava Pool":
            depthsL and (MetroidSuit in loadout),
        "Hive Main Chamber":
            hive,
        "Crossway Cache":
            hive and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Slag Heap":
            hive and canUseBombs and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Hydrodynamic Chamber":
            pirateLab and underwater and (Spazer in loadout),
        "Central Corridor: left":
            vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout) and (GravitySuit in loadout) and ((DarkVisor in loadout) or (pirateLab and canUsePB)),
        "Restricted Area":
            vulnar and canUseBombs and underwater and (MetroidSuit in loadout) and (((DarkVisor in loadout) and (Wave in loadout)) or ((pirateLab or eastLomyr) and canUsePB)),
        "Foundry":
            vulnar and canUseBombs and underwater and (((DarkVisor in loadout) and (Wave in loadout)) or ((pirateLab or eastLomyr) and canUsePB)),
        "Norak Escarpment":
            eastLomyr and (canFly or (SpeedBooster in loadout)),
        "Glacier's Reach":
            upperVulnar and (energyCount > 3),
        "Sitting Room":
            upperVulnar and canUsePB,
        "Suzi Ruins Map Station Access":
            suzi,
        "Obscured Vestibule":
            suzi,
        "Docking Port 3":  # (3 = letter Gamma)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or late_spaceport,
        "Arena":
            vulnar and (Morph in loadout),
        "West Spore Field":
            vulnar and canUseBombs and (Super in loadout) and (Wave in loadout) and (Speedball in loadout),
        "Magma Chamber":
            depthsL and (((Varia in loadout) and (Charge in loadout)) or ((MetroidSuit in loadout) and energyCount > 6)),
        "Equipment Locker":
            pirateLab,
        "Antelier":  # spelled "Antilier" in subversion 1.1
            pirateLab and underwater,
        "Weapon Research":
            vulnar and canUseBombs and (Wave in loadout) and underwater and ((DarkVisor in loadout) or (pirateLab and (canUsePB or (Screw in loadout)))),
        "Crocomire's Lair":
            eastLomyr and (Super in loadout) and (SpeedBooster in loadout),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

    return unusedLocations
