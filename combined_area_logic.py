from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicCommon import ammo_req, can_bomb, can_use_pbs, energy_req, \
    hell_run_energy, lava_run, varia_or_hell_run
from logic_area_shortcuts import SpacePort, LifeTemple, SkyWorld, FireHive, \
    PirateLab, Verdite, Geothermal, Suzi, DrayLand
from logicInterface import AreaLogicType
from logic_shortcut import LogicShortcut
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
            (canFly in loadout)
        ),  # this location cares about area rando
        ("SunkenNestL", "CraterR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(CraterR) in loadout) and
            (
                (
                    (SpaceJump in loadout) and (HiJump in loadout)
                ) or
                (SpeedBooster in loadout) or
                (
                    (Morph in loadout) and (Bombs in loadout)
                )
            )
        ),  # this location cares about area rando
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and  # includes missile barriers
            (cisternSporefield in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(vulnar, cisternSporefield, concourseShinespark)
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (causeway in loadout)
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            (vulnar in loadout) and
            (cisternSporefield in loadout)
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            (vulnar in loadout) and
            (wave in loadout) and
            (cisternSporefield in loadout)
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (concourseShinespark in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (causeway in loadout)
        ),
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (concourseShinespark in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (causeway in loadout) and
            (concourseShinespark in loadout)
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (causeway in loadout)
        ),
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (causeway in loadout) and
            (concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout)
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (causeway in loadout) and
            (cisternSporefield in loadout)
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            (wave in loadout) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (concourseShinespark in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout)
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            (wave in loadout) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (causeway in loadout)
        ),
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, Morph, underwater, Speedball, DarkVisor, Super)
        ),
        ("OceanShoreR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple, DarkVisor)
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
            loadout.has_all(jumpAble, Morph, underwater, Speedball, DarkVisor, Super) and
            (
                (wave in loadout) or
                (SpeedBooster in loadout) or
                (Screw in loadout) or
                (Speedball in loadout) or
                (canUsePB in loadout)
            )
        ),
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster, DarkVisor, Speedball)
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple, DarkVisor)
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster, DarkVisor, Speedball)
        ),
    },
    "PirateLab": {
        ("ExcavationSiteL", "WestCorridorR"): lambda loadout: (
            (jumpAble in loadout) and (
                (pinkDoor in loadout) or
                (Charge in loadout) or
                (Ice in loadout) or
                (wave in loadout) or
                (breakIce in loadout) or
                (canUsePB in loadout) or
                (Spazer in loadout)
            )
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            (underwater in loadout) and (
                ((canUsePB in loadout) and (wave in loadout) and (Bombs in loadout)) or
                ((
                    (pinkDoor in loadout) or
                    (Charge in loadout) or
                    (Ice in loadout) or
                    (wave in loadout) or
                    (breakIce in loadout) or
                    (canUsePB in loadout) or
                    (Spazer in loadout)
                ) and (Morph in loadout) and (Screw in loadout))
            )
        ),
        ("ExcavationSiteL", "ConstructionSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            ((
                (canUsePB in loadout) and
                ((Speedball in loadout) or (Bombs in loadout))  # 4 tile morph jump
            ) or (
                # through central corridor
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("ExcavationSiteL", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (underwater in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (((wave in loadout) and (Bombs in loadout)) or (Screw in loadout))
        ),
        ("WestCorridorR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and (
                (pinkDoor in loadout) or
                (Charge in loadout) or
                (Ice in loadout) or
                (wave in loadout) or
                (breakIce in loadout) or
                (canUsePB in loadout) or
                (Spazer in loadout)
            )
        ),
        ("WestCorridorR", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            (underwater in loadout) and
            ((
                (canUsePB in loadout) and
                (pinkDoor in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (underwater in loadout) and
                (Morph in loadout) and
                (Screw in loadout)
            ))
        ),
        ("WestCorridorR", "ConstructionSiteL"): lambda loadout: (
            (underwater in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or (
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            )) and (
                (Screw in loadout) or
                (Speedball in loadout)
            )
        ),
        ("WestCorridorR", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (underwater in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout)
            ))
        ),
        ("FoyerR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and (
                ((canUsePB in loadout) and (wave in loadout) and (Bombs in loadout)) or
                ((
                    (pinkDoor in loadout) or
                    (Charge in loadout) or
                    (Ice in loadout) or
                    (wave in loadout) or
                    (breakIce in loadout) or
                    (canUsePB in loadout) or
                    (Spazer in loadout)
                ) and (canBomb in loadout) and (Screw in loadout))
            )
        ),
        ("FoyerR", "WestCorridorR"): lambda loadout: (
            (jumpAble in loadout) and
            ((
                (canUsePB in loadout) and
                (pinkDoor in loadout) and
                (underwater in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (underwater in loadout) and
                (canBomb in loadout) and
                (Screw in loadout)
            ))
        ),
        ("FoyerR", "ConstructionSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            ((
                (canUsePB in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout)
            ) or (
                (Morph in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("FoyerR", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout))
        ),
        ("ConstructionSiteL", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            ((canUsePB in loadout) or (
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (underwater in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or (
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            )) and (
                (Screw in loadout) or
                (Speedball in loadout)
            )
        ),
        ("ConstructionSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            (underwater in loadout) and
            ((
                (canUsePB in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout)
            ) or (
                (Morph in loadout) and
                (wave in loadout) and
                (canBomb in loadout)
            ))
        ),
        ("ConstructionSiteL", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout)
            ))
        ),
        ("AlluringCenoteR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (underwater in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (Screw in loadout))
        ),
        ("AlluringCenoteR", "WestCorridorR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (underwater in loadout) and
                (pinkDoor in loadout)
            ))
        ),
        ("AlluringCenoteR", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout))
        ),
        ("AlluringCenoteR", "ConstructionSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout)
            ))
        ),
    },
    "ServiceSector": {
        ("FieldAccessL", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, DarkVisor, wave, canBomb)
        ),
        ("FieldAccessL", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            (underwater in loadout)
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, DarkVisor, wave, canBomb)
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            (underwater in loadout)
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, DarkVisor, wave)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, DarkVisor, wave)
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (underwater in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
            (DarkVisor in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
            (DarkVisor in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (DarkVisor in loadout) and
            (underwater in loadout) and
            ((SpaceJump in loadout) or (SpeedBooster in loadout))
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canFly in loadout) or
             (SpeedBooster in loadout) or
             (Ice in loadout))
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (canOpen(WestTerminalAccessL) in loadout) and
            (jumpAble in loadout) and (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout)
            )
        ),
        ("MezzanineConcourseL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout)
            ) and
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "CanyonPassageR"): lambda loadout: (
            jumpAble in loadout
        ),
        ("VulnarCanyonL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (SpeedBooster in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            ) and
            (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            (GravitySuit in loadout) and
            (
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (Bombs in loadout) or
                (Grapple in loadout)
            )
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            (GravitySuit in loadout) and
            (
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (Bombs in loadout) or
                (Grapple in loadout)
            )
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            (GravitySuit in loadout) and
            (
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (Bombs in loadout) or
                (Grapple in loadout)
            )
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (brook in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout)
            # Note: If no canFly and no speedbooster,
            # this requires a wall jump around a 2 tile ledge (in Water Garden)
            # I think that's not too hard for casual, but some people might not like it.
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (brook in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (brook in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (brook in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (brook in loadout)
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and
            (waterGardenBottom in loadout)  # includes canBomb for the bomb blocks in Norak Perimeter
        ),
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (brook in loadout)
        ),
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (MetroidSuit in loadout)
        ),
    },
    "FireHive": {
        ("VulnarDepthsElevatorEL", "VulnarDepthsElevatorER"): lambda loadout: (
            True
        ),
        ("VulnarDepthsElevatorER", "VulnarDepthsElevatorEL"): lambda loadout: (
            True
        ),
        ("VulnarDepthsElevatorER", "HiveBurrowL"): lambda loadout: (
            False  # One way logic not respected, intended
        ),
        ("VulnarDepthsElevatorER", "SequesteredInfernoL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (Varia in loadout) and
            (crossways in loadout) and
            (infernalSequestration in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (canBomb in loadout) and
            (Super in loadout) and
            (Varia in loadout) and
            (electricHyper in loadout)
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorEL"): lambda loadout: (
            False  # One way logic not respected, intended
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorER"): lambda loadout: (
            False  # One way logic not respected, intended
        ),
        ("HiveBurrowL", "SequesteredInfernoL"): lambda loadout: (
            False  # One way logic not respected, intended
        ),
        ("HiveBurrowL", "CollapsedPassageR"): lambda loadout: (
            False  # One way logic not respected, intended
        ),

        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (Varia in loadout) and
            (crossways in loadout) and
            (infernalSequestration in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            False  # One way Hive Burrow not in logic
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, wave, Super, Varia, infernalSequestration)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (Varia in loadout) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (wave in loadout) and
            (canBomb in loadout)
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            False  # One way hive burrow not in logic
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, wave, pinkDoor, Varia, infernalSequestration)
        ),
    },
    "Geothermal": {
        ("MagmaPumpL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (jumpAble in loadout) and
            (plasmaWaveGate in loadout) and
            (Varia in loadout) and
            (canBomb in loadout)
        ),
        ("MagmaPumpL", "IntakePumpR"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (Varia in loadout) and
            (canUsePB in loadout) and
            (
                (MetroidSuit in loadout) or
                (Screw in loadout)
            )
        ),
        ("MagmaPumpL", "ThermalReservoir1R"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (Varia in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("MagmaPumpL", "GeneratorAccessTunnelL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (Varia in loadout) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "MagmaPumpL"): lambda loadout: (
            (jumpAble in loadout) and
            (plasmaWaveGate in loadout) and
            (Varia in loadout) and
            (canBomb in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "IntakePumpR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
            ((MetroidSuit in loadout) or (
                (breakIce in loadout) and
                (Screw in loadout)
            ))
        ),
        ("ReservoirMaintenanceTunnelR", "ThermalReservoir1R"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, underwater, Screw, MetroidSuit, Varia)
        ),
        ("ReservoirMaintenanceTunnelR", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("IntakePumpR", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, Varia, canUsePB) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ),
        ("IntakePumpR", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
            (Varia in loadout) and
            ((MetroidSuit in loadout) or (
                (breakIce in loadout) and
                (Screw in loadout)
            ))
        ),
        ("IntakePumpR", "ThermalReservoir1R"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (Varia in loadout)
        ),
        ("IntakePumpR", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("ThermalReservoir1R", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, Varia, MetroidSuit, Screw)
        ),
        ("ThermalReservoir1R", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, underwater, Screw, MetroidSuit, Varia)
        ),
        ("ThermalReservoir1R", "IntakePumpR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit, Varia)
        ),
        ("ThermalReservoir1R", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, Varia)
        ),
        ("GeneratorAccessTunnelL", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, Varia, canUsePB, MetroidSuit, Screw)
        ),
        ("GeneratorAccessTunnelL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("GeneratorAccessTunnelL", "IntakePumpR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("GeneratorAccessTunnelL", "ThermalReservoir1R"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, Varia)
        ),
    },
    "DrayLand": {
        ("ElevatorToMagmaLakeR", "MagmaPumpAccessR"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (MetroidSuit in loadout) and
            (Varia in loadout) and
            (canUsePB in loadout)
        ),
        ("MagmaPumpAccessR", "ElevatorToMagmaLakeR"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (MetroidSuit in loadout) and
            (Varia in loadout) and
            (canUsePB in loadout)
        ),
    },
    "Verdite": {
        ("FieryGalleryL", "RagingPitL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, Varia, Super)
        ),
        ("FieryGalleryL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (Super in loadout) and
            (icePod in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (Super in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
            ) and
            (
                (icePod in loadout) or
                ((canUsePB in loadout) and (GravitySuit in loadout))
            )
        ),
        ("FieryGalleryL", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (GravitySuit in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("RagingPitL", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (canUsePB in loadout)
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, Varia, icePod)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Varia in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (
                (icePod in loadout) or
                (GravitySuit in loadout)
            )
        ),
        ("RagingPitL", "SporousNookL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Varia, underwater)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (pinkDoor in loadout) and
            (icePod in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
            )
        ),
        ("HollowChamberR", "RagingPitL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, Speedball, Varia, Super, icePod)
            # can this be a screw instead of a bomb?
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (icePod in loadout)
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (icePod in loadout) and
            (GravitySuit in loadout) and
            (pinkDoor in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (pinkDoor in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
            ) and
            (
                (icePod in loadout) or
                ((canUsePB in loadout) and (GravitySuit in loadout))
            )
        ),
        ("PlacidPoolR", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (Super in loadout) and
            (
                (icePod in loadout) or
                ((canUsePB in loadout) and (GravitySuit in loadout))
            )
        ),
        ("PlacidPoolR", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, Varia, icePod)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Speedball in loadout) and
            (Varia in loadout) and
            (pinkDoor in loadout) and
            (GravitySuit in loadout) and
            (
                (icePod in loadout) or
                ((canUsePB in loadout) and (GravitySuit in loadout))
            ) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("SporousNookL", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (underwater in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("SporousNookL", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Varia in loadout) and
            (underwater in loadout) and
            (Super in loadout)
        ),  # screw into raging pit?
        ("SporousNookL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            (underwater in loadout)
        ),
        ("SporousNookL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (Varia in loadout) and
            (Super in loadout) and
            (underwater in loadout) and
            (
                (icePod in loadout) or
                (canUsePB in loadout)
            )
        ),
    },
}
