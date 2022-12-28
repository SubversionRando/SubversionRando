from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from logicCommon import ammo_req, can_bomb, can_use_pbs, energy_req, \
    hell_run_energy, lava_run, varia_or_hell_run
from logic_area_shortcuts import SandLand, ServiceSector, LifeTemple, \
    SkyWorld, FireHive, PirateLab, Verdite, Geothermal, DrayLand, Early
from logicInterface import AreaLogicType
from logic_shortcut_data import (
    canFly, shootThroughWalls, breakIce, missileDamage, pinkDoor, pinkSwitch,
    missileBarrier, icePod, electricHyper, killRippers, killGreenPirates
)
from trick_data import Tricks

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            canFly in loadout
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(CraterR) in loadout) and
            ((
                (SpaceJump in loadout) and (HiJump in loadout)  # TODO: count sjb with and without hjb
            ) or (SpeedBooster in loadout) or (
                (Morph in loadout) and (Bombs in loadout)
            ))
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(
                GravityBoots, pinkDoor, missileBarrier, Early.cisternAccessTunnel, Early.concourseShinespark
            )
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout)
            # TODO: confirm these doors are pink if they're encountered 1st in this direction
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout)
        ),
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            loadout.has_all(
                GravityBoots, pinkDoor, missileBarrier, Early.cisternAccessTunnel, Early.concourseShinespark
            )
            # TODO: confirm these doors are pink if they're encountered 1st in this direction
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
            # TODO: confirm these doors are pink if they're encountered 1st in this direction
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout)
        ),
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.sporeFieldEntrance in loadout)
            # TODO: confirm these doors are pink if they're encountered 1st in this direction
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (Early.sporeFieldEntrance in loadout)
            # TODO: confirm these doors are pink if they're encountered 1st in this direction
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
            # same as "EleToTurbidPassageR", "OceanShoreR" except door colors changed for direction
            (SandLand.turbidToSedFloor in loadout) and
            (Super in loadout) and  # door from sediment floor to turbid passage
            ((
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and
                (Super in loadout)  # door from shallows to canyon
                # TODO: instead of super door, moonfall and pb to open door from other side
            ) or (
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToShaft in loadout) and
                (SandLand.shaftToGreenMoon in loadout)
            ) or (
                (SandLand.lowerLowerToSedFloor in loadout) and
                (Super in loadout) and  # door from meandering to sediment floor
                (SandLand.shaftToLowerLower in loadout) and
                ((
                    (SandLand.canyonToShaft in loadout) and
                    (SandLand.canyonToGreenMoon in loadout) and
                    (Super in loadout)  # door from shallows to canyon
                ) or (
                    (SandLand.shaftToGreenMoon in loadout)
                ))
            ))
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
            # same as "OceanShoreR", "EleToTurbidPassageR" except door colors changed for direction
            (SandLand.turbidToSedFloor in loadout) and
            (pinkDoor in loadout) and  # turbid passage to sediment floor
            ((
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and
                (can_use_pbs(1) in loadout)  # door to shallows
            ) or (
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToShaft in loadout) and
                (SandLand.shaftToGreenMoon in loadout)
            ) or (
                (SandLand.lowerLowerToSedFloor in loadout) and
                (pinkDoor in loadout) and  # sediment floor to meandering
                (SandLand.shaftToLowerLower in loadout) and
                ((
                    (SandLand.canyonToShaft in loadout) and
                    (SandLand.canyonToGreenMoon in loadout) and
                    (can_use_pbs(1) in loadout)  # door to shallows
                ) or (
                    (SandLand.shaftToGreenMoon in loadout)
                ))
            ))
        ),
        ("OceanShoreR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, GravitySuit, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, GravitySuit, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, GravitySuit, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, GravitySuit, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
    },
    "PirateLab": {
        ("ExcavationSiteL", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and (killGreenPirates in loadout)
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            ((  # high
                (killGreenPirates in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (Screw in loadout) and
                (PirateLab.eastCorridor in loadout)
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.eastCorridor in loadout)
            ))
        ),
        ("ExcavationSiteL", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ExcavationSiteL", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # high
                (killGreenPirates in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (Screw in loadout) and
                (PirateLab.cenote in loadout)
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                ((Screw in loadout) or (MetroidSuit in loadout)) and
                (PirateLab.cenote in loadout)
            ))
        ),
        ("WestCorridorR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and (killGreenPirates in loadout)
        ),
        ("WestCorridorR", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (Screw in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("WestCorridorR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (killGreenPirates in loadout) and  # TODO: is this needed for either direction if you start from corridor?
            (can_use_pbs(1) in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("WestCorridorR", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (Screw in loadout) and
            (PirateLab.cenote in loadout)
        ),
        ("FoyerR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # high
                (PirateLab.eastCorridor in loadout) and
                (Screw in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenPirates in loadout)  # TODO: is this needed for either direction if you start from corridor?
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.eastCorridor in loadout)
            ))
        ),
        ("FoyerR", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (Screw in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("FoyerR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            (PirateLab.epiphreaticCrag in loadout) and
            (PirateLab.centralCorridorWater in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("FoyerR", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.eastCorridor in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("ConstructionSiteL", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            ((  # outside
                (can_use_pbs(1) in loadout)
            ) or (  # inside
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (Screw in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenPirates in loadout)
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (killGreenPirates in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ConstructionSiteL", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.eastCorridor in loadout) and
            (PirateLab.centralCorridorWater in loadout) and
            (PirateLab.epiphreaticCrag in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ConstructionSiteL", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            ((  # top
                (can_use_pbs(1) in loadout) and
                (killGreenPirates in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (Screw in loadout)
            ) or (  # bottom
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout)
            )) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("AlluringCenoteR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # top
                (killGreenPirates in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (Screw in loadout)
            ) or (  # bottom
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticCrag in loadout) and
                (PirateLab.centralCorridorWater in loadout)
            )) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("AlluringCenoteR", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (Screw in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout)
            ) or (
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.epiphreaticCrag in loadout) and
                (can_use_pbs(1) in loadout) and
                (killGreenPirates in loadout)
            ))
        ),
        ("AlluringCenoteR", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.eastCorridor in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout))
        ),
        ("AlluringCenoteR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((  # top
                (Screw in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenPirates in loadout) and
                (can_use_pbs(1) in loadout)
            ) or (  # bottom
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.epiphreaticCrag in loadout)
            )) and
            (PirateLab.constructionLToElevator in loadout)
        ),
    },
    "ServiceSector": {
        ("FieldAccessL", "TransferStationR"): lambda loadout: (
            loadout.has_all(GravityBoots, pinkDoor, DarkVisor, shootThroughWalls, can_bomb(1))
        ),
        ("FieldAccessL", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Super in loadout) and  # door from crumbling basement to cellar, and field access pink door
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            # If you fall in the water with nothing, it's a tight jump to get out.
            # But if you don't want to do that tight jump, then don't fall in the water.
            # It's not worth putting in logic that something is required when it's not required,
            # just for the case that someone falls in the water without it.
            (shootThroughWalls in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Super in loadout) and  # door into exhaust vent, and pink door in field access
            (can_bomb(1) in loadout) and  # can screw down, but not up
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            (shootThroughWalls in loadout) and
            (ServiceSector.wasteProcessingTraverse in loadout)
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(GravityBoots, pinkDoor, DarkVisor, can_bomb(1))
            # not putting shootThroughWalls in requirements here, don't close the door behind you
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Super in loadout) and
            (can_bomb(1) in loadout) and
            (DarkVisor in loadout) and
            (shootThroughWalls in loadout)
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (DarkVisor in loadout) and
            (Super in loadout) and  # door to exhaust vent
            (can_bomb(1) in loadout) and
            (shootThroughWalls in loadout) and
            (ServiceSector.wasteProcessingTraverse in loadout)
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # cellar to crumbling, and field access pink door
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            (shootThroughWalls in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(GravityBoots, pinkDoor, can_bomb(1), DarkVisor, shootThroughWalls)
            # door from cellar to crumbling
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Super in loadout) and  # door into exhaust vent, and pink door to crumbling
            (can_bomb(1) in loadout) and
            (ServiceSector.wasteProcessingTraverse in loadout) and
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout))
            # TODO: why did expert logic say dark visor was hard required here?
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (shootThroughWalls in loadout) and  # return logic
            (pinkDoor in loadout) and  # into field access
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout))
            # TODO: why did expert logic say dark visor was hard required here?
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (shootThroughWalls in loadout) and
            (DarkVisor in loadout)
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (Super in loadout) and  # door into cellar access
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            (can_bomb(1) in loadout)
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout))
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout))
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (canOpen(WestTerminalAccessL) in loadout) and
            (GravityBoots in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("MezzanineConcourseL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.mezzanineShaft in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("VulnarCanyonL", "CanyonPassageR"): lambda loadout: (
            GravityBoots in loadout
        ),
        ("VulnarCanyonL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            (canOpen(WestTerminalAccessL) in loadout)
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.perimBL in loadout)
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.perimBL in loadout)
        ),
        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (MetroidSuit in loadout)
        ),
    },
    "FireHive": {
        ("VulnarDepthsElevatorEL", "VulnarDepthsElevatorER"): lambda loadout: (
            True  # flat hallway to walk across
        ),
        ("VulnarDepthsElevatorER", "VulnarDepthsElevatorEL"): lambda loadout: (
            True  # flat hallway to walk across
        ),
        ("VulnarDepthsElevatorER", "HiveBurrowL"): lambda loadout: (
            False  # One way logic not respected, intended
        ),
        ("VulnarDepthsElevatorER", "SequesteredInfernoL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorER"): lambda loadout: (
            False  # One way
        ),
        ("HiveBurrowL", "SequesteredInfernoL"): lambda loadout: (
            False  # One way
        ),
        ("HiveBurrowL", "CollapsedPassageR"): lambda loadout: (
            False  # One way
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout) and
            (icePod in loadout) and
            (FireHive.hiveEntrance in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            False  # One way Hive Burrow not in logic
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.courtyardToCollapsed in loadout) and
            (pinkDoor in loadout) and  # into ancient basin
            (FireHive.crosswaysToCourtyard in loadout) and
            (FireHive.crossways in loadout) and
            (icePod in loadout) and
            (FireHive.hiveEntrance in loadout)
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            False  # One way hive burrow not in logic
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.courtyardToCollapsed in loadout) and
            (pinkDoor in loadout) and  # into ancient basin
            (FireHive.crosswaysToCourtyard in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
    },
    "Geothermal": {
        ("MagmaPumpL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            # matched (cept varia)
            (GravityBoots in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canBomb in loadout)
        ),
        ("MagmaPumpL", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((GravitySuit in loadout) or  # casual need gravity
             (HiJump in loadout)) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canUsePB in loadout) and
            (
                ((MetroidSuit in loadout) and (energy_req(250) in loadout)) or
                (Screw in loadout)
                )
        ),
        ("MagmaPumpL", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or  # casual needed
                (
                    (canBomb in loadout) and
                    (
                        (HiJump in loadout) or
                        (Ice in loadout)
                        )
                    )
                ) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("MagmaPumpL", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            (
                (GravitySuit in loadout) or  # casual needed
                (canBomb in loadout) and
                (LargeAmmo in loadout) and
                (
                     (HiJump in loadout) or
                     (Ice in loadout)
                     )
                ) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canBomb in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or  # casual gravity
             (HiJump in loadout)) and
            (
                ((MetroidSuit in loadout) and (energy_req(250) in loadout)) or
                (
                    (breakIce in loadout) and
                    (Screw in loadout)
                    )
                )
        ),
        ("ReservoirMaintenanceTunnelR", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or
                (
                    (canBomb in loadout and
                     (
                         (HiJump in loadout) or
                         (Ice in loadout)
                         )
                     )
                    ) 
                ) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
            # TODO: canBomb discrepancy?
        ),
        ("ReservoirMaintenanceTunnelR", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or  # casual need
                (
                    (HiJump in loadout) or
                    (Ice in loadout)
                    )
                ) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("IntakePumpR", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((GravitySuit in loadout) or  # casual need
             (HiJump in loadout)) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canUsePB in loadout) and
            (
                ((MetroidSuit in loadout) and (energy_req(250) in loadout))or
                (Screw in loadout)
                )
        ),
        ("IntakePumpR", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or # casual need
            # TODO: varia discrepancy?
             (HiJump in loadout)) and
            (
                ((MetroidSuit in loadout) and (energy_req(250) in loadout)) or
                (
                    (breakIce in loadout) and
                    (Screw in loadout)
                    )
                )
        ),
        ("IntakePumpR", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or # c
             (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (# expert add
                (energy_req(250) in loadout) or
                (breakIce in loadout)
                ) and  
            (varia_or_hell_run(350) in loadout)
        ),
        ("IntakePumpR", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout)) and #c
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (# expert add
                (energy_req(250) in loadout) or
                (breakIce in loadout)  
                )
        ),
        ("ThermalReservoir1R", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or#c
                (
                    (canBomb in loadout) and
                    (
                        (HiJump in loadout) or
                        (Ice in loadout)
                     )
                 )
                ) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("ThermalReservoir1R", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or#c
                (canBomb in loadout) and
                 (
                     (HiJump in loadout) or
                     (Ice in loadout)
                     )
                ) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("ThermalReservoir1R", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or#c
             (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (#expert add
                (energy_req(250) in loadout) or
                (breakIce in loadout)
                ) and
            (varia_or_hell_run(350) in loadout)
        ),
        ("ThermalReservoir1R", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(GravityBoots, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
        ("GeneratorAccessTunnelL", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            (
                (GravitySuit in loadout) or#c
                (canBomb in loadout) and
                (
                     (HiJump in loadout) or
                     (Ice in loadout)
                     )
                ) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("GeneratorAccessTunnelL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (GravitySuit in loadout) or#c
                (canBomb in loadout) and
                (
                     (HiJump in loadout) or
                     (Ice in loadout)
                     )
                ) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("GeneratorAccessTunnelL", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout)) and#c
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (#expert add
                (energy_req(250) in loadout) or
                (breakIce in loadout)
                )
        ),
        ("GeneratorAccessTunnelL", "ThermalReservoir1R"): lambda loadout: (
            loadout.has_all(GravityBoots, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
    },
    "DrayLand": {
        ("ElevatorToMagmaLakeR", "MagmaPumpAccessR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (
                    (GravitySuit in loadout) and#c
                    (Screw in loadout)
                    ) or
                (electricHyper in loadout)
                ) and
            (Varia in loadout) and 
            (MetroidSuit in loadout) and
            (canUsePB in loadout)
        ),
        ("MagmaPumpAccessR", "ElevatorToMagmaLakeR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (
                    (GravitySuit in loadout) and#c
                    (Screw in loadout)
                    ) or
                (electricHyper in loadout)
                ) and
            (Varia in loadout) and 
            (MetroidSuit in loadout) and
            (canUsePB in loadout)
        ),
    },
    "Verdite": {
        ("FieryGalleryL", "RagingPitL"): lambda loadout: (
            loadout.has_all(GravityBoots, Super, canBomb, varia_or_hell_run(450))
        ),
        ("FieryGalleryL", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            casual Speedball
            (varia_or_hell_run(550) in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (Super in loadout) and
            (Morph in loadout) and  # TODO: confirm needed
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or#c
                        (HiJump in loadout)
                        )
                    )
                )
        ),
        ("FieryGalleryL", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("RagingPitL", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (canUsePB in loadout)
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            loadout.has_all(GravityBoots, canUsePB, Super, varia_or_hell_run(450), icePod)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and
            is pb needed?
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (underwater in loadout)
                    )
                )
        ),
        ("RagingPitL", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canUsePB in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (hotSpring in loadout)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            casual Speedball
            (varia_or_hell_run(450) in loadout) and
            (pinkDoor in loadout) and
            (icePod in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
                )
        ),
        ("HollowChamberR", "RagingPitL"): lambda loadout: (
            loadout.has_all(GravityBoots, canBomb, varia_or_hell_run(450), Super, icePod)
            casual Speedball
            # can you screw into raging pit?
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(250) in loadout) and
            (icePod in loadout)
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            #casual Speedball
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout) and
            (pinkDoor in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
                ) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (
                    (GravitySuit in loadout) and
                    (Screw in loadout)
                    )
                )
        ),
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            casual Speedball
            (varia_or_hell_run(550) in loadout) and
            (pinkDoor in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)) and# and?
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or#c
                        (HiJump in loadout)
                        )
                    )
                )
        ),
        ("PlacidPoolR", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canBomb in loadout) and
            casual Speedball
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or#c
                        (HiJump in loadout)
                        )
                    )
                )
        ), #screw into raging pit?
        ("PlacidPoolR", "HollowChamberR"): lambda loadout: (
            loadout.has_all(GravityBoots, varia_or_hell_run(250), icePod)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Morph in loadout) and
            c Speedball
            (pinkDoor in loadout) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or#c
                        (HiJump in loadout)
                        )
                    )
                ) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (
                    (GravitySuit in loadout) and
                    (Screw in loadout)
                    )
                )
        ),
        ("SporousNookL", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("SporousNookL", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (hotSpring in loadout)
        ),  # screw into raging pit?
        ("SporousNookL", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            # casual ended with underwater here
            (Morph in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
                ) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (
                    (GravitySuit in loadout) and
                    (Screw in loadout)
                    )
                )
        ),
        ("SporousNookL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Morph in loadout) and#?
            (Super in loadout) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout)
                    )
                )
            ) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (
                    (GravitySuit in loadout) and
                    (Screw in loadout)
                )
            )
        ),
    },
}
