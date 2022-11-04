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
    pirateLab = vulnar and canUseBombs and (
        ((Speedball in loadout) or (SpeedBooster in loadout)) or ((DarkVisor in loadout) and canUsePB)
    )
    canFly = (Bombs in loadout) or (SpaceJump in loadout)
    upperVulnar = jumpAble and ((canUsePB and canFly) or (vulnar and (SpeedBooster in loadout)))
    depthsL = (Varia in loadout) and (Bombs in loadout) and (
        (underwater and (Super in loadout)) or (vulnar and (Wave in loadout))
    )
    hive = (Varia in loadout) and (
        (Super in loadout) or (upperVulnar and underwater and breakIce)
    ) and vulnar and canUseBombs and (
        (depthsL and (canUsePB or (Ice in loadout))) or
        ((Wave in loadout) and (SpeedBooster in loadout)) or
        ((SpeedBooster in loadout) and canUsePB)
    )
    geothermal = (hive and canUsePB and (Ice in loadout)) or (
        upperVulnar and underwater and breakIce and canUsePB and (Screw in loadout)
    )
    eastLomyr = vulnar and canUsePB and (Bombs in loadout) and (
        (SpeedBooster in loadout) or (pirateLab and (GravitySuit in loadout) and (Super in loadout))
    )
    oceanDepths = underwater and ((pinkDoor and (Morph in loadout) and (DarkVisor in loadout)) or (Super in loadout))
    breakIce = (Plasma in loadout) or ((Hypercharge in loadout) and (Charge in loadout))
    suzi = underwater and (SpeedBooster in loadout) and (Grapple in loadout) and \
        (Super in loadout) and canUsePB and (Wave in loadout)
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
            exitSpacePort and (Morph in loadout) and (Spazer in loadout) and (
                (HiJump in loadout) or (SpeedBooster in loadout) or (SpaceJump in loadout)
            ),
        "Subterranean Burrow":
            exitSpacePort and ((Morph in loadout) or (GravityBoots in loadout)),
        "Sandy Cache":
            jumpAble and (Missile in loadout),
        "Submarine Nest":
            underwater and pinkDoor,
        "Shrine Of The Penumbra":
            jumpAble and pinkDoor and (GravitySuit in loadout) and (
                canUsePB or (canUseBombs and (DarkVisor in loadout))
            ),
        "Benthic Cache Access":
            jumpAble and underwater and canUseBombs and (DarkVisor in loadout) and
            (Super in loadout) and (PowerBomb in loadout),
        "Benthic Cache":
            jumpAble and underwater and canUseBombs and (DarkVisor in loadout) and (Super in loadout),
        "Ocean Vent Supply Depot":
            jumpAble and underwater and (Morph in loadout) and (DarkVisor in loadout) and pinkDoor and (
                (Super in loadout) or (Screw in loadout) or (canUsePB and (MetroidSuit in loadout))
            ),
        "Sediment Flow":
            jumpAble and underwater and (Super in loadout),
        "Harmonic Growth Enhancer":
            jumpAble and pinkDoor and canUseBombs and ((Wave in loadout) or (DarkVisor in loadout)),
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
            vulnar and canUseBombs,
        "Archives: SpringBall":  # yes it's actually Speed Ball, uses Spring data
            vulnar and canUseBombs and (Speedball in loadout),
        "Archives: SJBoost":
            vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout),
        "Sensor Maintenance: ETank":  # front
            vulnar and canUseBombs and (Speedball in loadout),
        "Eribium Apparatus Room":
            vulnar and canUseBombs and (DarkVisor in loadout),
        "Hot Spring":
            vulnar and underwater and canUseBombs and (DarkVisor in loadout) and (
                (Wave in loadout) or (Varia in loadout)
            ),
        "Epiphreatic Crag":
            vulnar and canUseBombs and (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and canUsePB)
            ),
        "Mezzanine Concourse":
            upperVulnar,
        "Greater Inferno":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout) and (
                (SpeedBooster in loadout) or (Screw in loadout)
            ),
        "Burning Depths Cache":
            depthsL and canUsePB and ((Super in loadout) or breakIce) and (MetroidSuit in loadout) and (
                (SpeedBooster in loadout) or (Screw in loadout)
            ) and ((Spazer in loadout) or (Wave in loadout)),
        "Mining Cache":
            vulnar and underwater and canUseBombs and (DarkVisor in loadout) and (Super in loadout),
        "Infested Passage":
            hive,
        "Fire's Boon Shrine":
            (Wave in loadout) and (
                (hive and ((Ice in loadout) or (SpeedBooster in loadout))) or (eastLomyr and canUseBombs and underwater)
            ),
        "Fire's Bane Shrine":
            (hive and ((Ice in loadout) or (SpeedBooster in loadout))) or
            (eastLomyr and canUseBombs and underwater),
        "Ancient Shaft":
            hive and (MetroidSuit in loadout) and ((Ice in loadout) or (SpeedBooster in loadout)),
        "Gymnasium":
            (Grapple in loadout) and (
                (hive and canUsePB and ((Ice in loadout) or (SpeedBooster in loadout))) or
                (eastLomyr and canUseBombs and underwater)
            ),
        "Electromechanical Engine":
            geothermal,
        "Depressurization Valve":
            geothermal and ((MetroidSuit in loadout) or ((Grapple in loadout) and (Screw in loadout))),
        "Loading Dock Storage Area":
            pirateLab,
        "Containment Area":
            pirateLab and (GravitySuit in loadout) and ((MetroidSuit in loadout) or (Screw in loadout)),
        "Briar: SJBoost":  # top
            eastLomyr and canUsePB,
        "Shrine Of Fervor":
            eastLomyr,
        "Chamber Of Wind":
            eastLomyr and pinkDoor and (SpeedBooster in loadout) and (
                canUseBombs or ((Screw in loadout) and (Speedball in loadout))
            ),
        "Water Garden":
            eastLomyr and pinkDoor and (SpeedBooster in loadout),
        "Crocomire's Energy Station":
            eastLomyr and (Super in loadout) and (SpeedBooster in loadout),
        "Wellspring Cache":
            eastLomyr and (Super in loadout) and (SpeedBooster in loadout),
        "Frozen Lake Wall: DamageAmp":
            upperVulnar and breakIce,
        "Grand Promenade":
            upperVulnar,
        "Summit Landing":
            upperVulnar and canUseBombs and (Speedball in loadout),
        "Snow Cache":
            upperVulnar and canUseBombs and breakIce,
        "Reliquary Access":
            upperVulnar and canUseBombs and (Super in loadout) and (DarkVisor in loadout),
        "Syzygy Observatorium":
            upperVulnar and (((Super in loadout) and (Varia in loadout) and (
                (MetroidSuit in loadout) or (Hypercharge in loadout)
            )) or (Screw in loadout)),
        "Armory Cache 2":
            upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout)),
        "Armory Cache 3":
            upperVulnar and ((canUseBombs and (Super in loadout) and (DarkVisor in loadout)) or (Screw in loadout)),
        "Drawing Room":
            upperVulnar and (Super in loadout),
        "Impact Crater Overlook":
            canFly and canUseBombs and (canUsePB or (Super in loadout)),
        "Magma Lake Cache":
            depthsL,
        "Shrine Of The Animate Spark":
            suzi and canFly and (Hypercharge in loadout) and (Charge in loadout),
        "Docking Port 4":  # (4 = letter Omega)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or late_spaceport,
        "Ready Room":
            ((spaceDrop not in loadout) and (Super in loadout)) or late_spaceport,
        "Torpedo Bay":
            True,
        "Extract Storage":
            geothermal and canUsePB and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout),
        "Impact Crater Alcove":
            jumpAble and canFly and canUseBombs,
        "Ocean Shore: bottom":
            exitSpacePort,
        "Ocean Shore: top":
            jumpAble and (canFly or (HiJump in loadout) or ((SpeedBooster in loadout) and (GravitySuit in loadout))),
        "Sandy Burrow: ETank":  # top
            underwater and canUseBombs,
        "Submarine Alcove":
            underwater and (Morph in loadout) and (DarkVisor in loadout) and pinkDoor,
        "Sediment Floor":
            underwater and (Morph in loadout) and (
                (Super in loadout) or (vulnar and (Varia in loadout) and canUseBombs)
            ),
        "Sandy Gully":  # TODO: really no (high jump boots or space jump) required for this?
            underwater and (Super in loadout),
        "Hall Of The Elders":
            vulnar and (Morph in loadout) and ((Missile in loadout) or (GravitySuit in loadout)),
        "Warrior Shrine: AmmoTank bottom":
            vulnar and (Morph in loadout) and (Missile in loadout) and ((Bombs in loadout) or (Wave in loadout)),
        "Warrior Shrine: AmmoTank top":
            vulnar and
            canUseBombs and
            ((Missile in loadout) or (GravitySuit in loadout)) and
            ((Bombs in loadout) or (Wave in loadout)),
        "Path Of Swords":
            vulnar and canUseBombs,
        "Auxiliary Pump Room":
            vulnar and canUseBombs,
        "Monitoring Station":
            vulnar and (Morph in loadout) and (Speedball in loadout),
        "Sensor Maintenance: AmmoTank":  # back
            vulnar and canUseBombs and (Speedball in loadout) and (Missile in loadout),
        "Causeway Overlook":
            vulnar and canUseBombs,
        "Placid Pool":
            vulnar and canUsePB and (Ice in loadout) and (
                (Varia in loadout) or
                ((DarkVisor in loadout) and (Wave in loadout)) or
                ((DarkVisor in loadout) and (Speedball in loadout) or (SpeedBooster in loadout))
            ),
        "Blazing Chasm":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout),
        "Generator Manifold":
            depthsL and canUsePB and (Super in loadout) and (MetroidSuit in loadout),
        "Fiery Crossing Cache":
            depthsL and canUsePB and (Super in loadout),
        "Dark Crevice Cache":
            depthsL and canUseBombs,
        "Ancient Basin":
            hive,
        "Central Corridor: right":
            vulnar and canUseBombs and (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and canUsePB)
            ),
        "Briar: AmmoTank":  # bottom
            eastLomyr and (Morph in loadout),
        "Icy Flow":
            upperVulnar and (SpeedBooster in loadout) and breakIce,
        "Ice Cave":
            upperVulnar and breakIce,
        "Antechamber":
            upperVulnar and canUsePB,
        "Eddy Channels":
            underwater and (Speedball in loadout) and ((pinkDoor and (DarkVisor in loadout)) or (Super in loadout)),
        "Tram To Suzi Island":
            oceanDepths and canUsePB and (Super in loadout) and (Grapple in loadout) and
            (SpeedBooster in loadout) and (Spazer in loadout),
        "Portico":
            suzi,
        "Tower Rock Lookout":
            suzi and canFly,
        "Reef Nook":
            suzi and canFly,
        "Saline Cache":
            suzi,
        "Enervation Chamber":
            suzi and canFly and (Hypercharge in loadout) and (Charge in loadout),
        "Weapon Locker":
            ((spaceDrop not in loadout) and (Missile in loadout)) or late_spaceport,
        "Aft Battery":  # CAUTIOUS LOGIC
            ((spaceDrop not in loadout) and (Morph in loadout)) or late_spaceport,
        "Forward Battery":  # CAUTIOUS LOGIC
            geothermal and (Grapple in loadout) and (Screw in loadout) and (MetroidSuit in loadout),
        "Gantry":  # CAUTIOUS LOGIC
            ((spaceDrop not in loadout) and (Missile in loadout)) or late_spaceport,
        "Garden Canal":  # CAUTIOUS LOGIC
            eastLomyr and canUsePB and (Spazer in loadout),
        "Sandy Burrow: AmmoTank":  # bottom
            underwater and (Morph in loadout) and pinkDoor,
        "Trophobiotic Chamber":
            vulnar and (Morph in loadout) and (Speedball in loadout),
        "Waste Processing":
            pirateLab and (SpeedBooster in loadout) and ((Wave in loadout) or canUsePB),
        "Grand Chasm":
            upperVulnar and canUseBombs and (Screw in loadout),
        "Mining Site 1":  # (1 = letter Alpha)
            canUseBombs and ((vulnar and underwater and (Wave in loadout)) or depthsL),
        "Colosseum":  # GT
            depthsL and (Charge in loadout),
        "Lava Pool":
            depthsL and (MetroidSuit in loadout) and canUsePB,
        "Hive Main Chamber":
            hive,
        "Crossway Cache":
            hive and (
                (Ice in loadout) or
                (SpeedBooster in loadout) or
                (eastLomyr and canUseBombs and (Wave in loadout))
            ),
        "Slag Heap":
            hive and (MetroidSuit in loadout) and (
                (Ice in loadout) or (SpeedBooster in loadout) or (
                    eastLomyr and canUseBombs and (Wave in loadout)
                )
            ),
        "Hydrodynamic Chamber":
            pirateLab and (Spazer in loadout) and ((HiJump in loadout) or (GravitySuit in loadout)),
        "Central Corridor: left":
            vulnar and canUseBombs and (Speedball in loadout) and (SpeedBooster in loadout) and
            (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and ((canUsePB and (Wave in loadout)) or (Screw in loadout)))
            ),
        "Restricted Area":
            vulnar and canUseBombs and (MetroidSuit in loadout) and (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and ((canUsePB and (Wave in loadout)) or (Screw in loadout)))
            ),
        "Foundry":
            vulnar and canUseBombs and (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and canUsePB)
            ),
        "Norak Escarpment":
            eastLomyr and (canFly or (SpeedBooster in loadout)),
        "Glacier's Reach":
            upperVulnar and canUseBombs and breakIce,
        "Sitting Room":
            upperVulnar and canUsePB and (Speedball in loadout),
        "Suzi Ruins Map Station Access":
            suzi,
        "Obscured Vestibule":  # Suzi
            suzi,
        "Docking Port 3":  # (3 = letter Gamma)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or late_spaceport,
        "Arena":
            vulnar and (Morph in loadout) and (Missile in loadout) and (
                (Bombs in loadout) or (Screw in loadout) or (Wave in loadout)
            ),
        "West Spore Field":
            vulnar and canUseBombs and (Super in loadout) and (Wave in loadout) and (Speedball in loadout),
        "Magma Chamber":
            depthsL and ((Charge in loadout) or (MetroidSuit in loadout)),
        "Equipment Locker":
            pirateLab and canUseBombs,
        "Antelier":  # spelled "Antilier" in subversion 1.1
            pirateLab and ((HiJump in loadout) or (GravitySuit in loadout)),
        "Weapon Research":
            vulnar and canUseBombs and (Wave in loadout) and (GravitySuit in loadout) and (
                (DarkVisor in loadout) or (pirateLab and canUsePB)
            ),
        "Crocomire's Lair":
            eastLomyr and (Super in loadout) and (SpeedBooster in loadout),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

    return unusedLocations
