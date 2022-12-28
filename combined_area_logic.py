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
            canFly in loadout
        ),
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
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and  # includes missile barriers
            (cisternSporefield in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, cisternSporefield, concourseShinespark)
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (causeway in loadout) and
            # expert: 
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (Morph in loadout) and
            (
                (SpeedBooster in loadout) or
                (
                    (canBomb in loadout) and
                    (
                        (Speedball in loadout) or
                        (
                            (wave in loadout) and
                            (
                                (GravitySuit in loadout) or
                                (HiJump in loadout) or
                                (Ice in loadout)
                            )
                        )
                    )
                )
            )
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            (vulnar in loadout) and
            (Morph in loadout)
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            (vulnar in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch)) and
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
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
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
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (concourseShinespark in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (jumpAble in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (cisternSporefield in loadout) and
            (causeway in loadout)
        ),
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, Morph, underwater, Speedball, DarkVisor, Super) and
            # expert:
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Super in loadout) and
            (
                (GravitySuit in loadout) or
                (HiJump in loadout) or
                (Ice in loadout)
                ) and
            (
                (GravitySuit in loadout) or
                (
                    (Speedball in loadout) and
                    (HiJump in loadout)
                    )
                ) and
            (
                (GravitySuit in loadout) or
                (Ice in loadout) or
                (
                    (wave in loadout) and
                    (DarkVisor in loadout)
                    ) 
                )
        ),
        ("OceanShoreR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Super in loadout) and
            # casual:
            loadout.has_all(underwater, Speedball, DarkVisor) and
            (
                (wave in loadout) or
                (SpeedBooster in loadout) or
                (Screw in loadout) or
                (Speedball in loadout) or
                (canUsePB in loadout)
            )
            # expert:
            (
                (GravitySuit in loadout) or
                (HiJump in loadout) or
                (Ice in loadout)
            ) and
            (
                (GravitySuit in loadout) or
                (
                    (Speedball in loadout) and
                    (HiJump in loadout)
                )
            ) and
            (
                (GravitySuit in loadout) or
                (Ice in loadout) or
                (
                    (wave in loadout) and
                    (DarkVisor in loadout)
                )
            )
        ),
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster) and
            (casual dark visor and speedball)
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster) and
            (casual dark visor and speedball)
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
                (canBomb in loadout) or  # casual needed pb?
                (Spazer in loadout)
            )
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            # casual:
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
            # expert:
            (canBomb in loadout) and
            (
                (
                    (canUsePB in loadout) and
                    ((wave in loadout) or (Spazer in loadout)) and
                    (Bombs in loadout)
                    ) or
                (
                    (pinkDoor in loadout) and
                    (Screw in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout) or
                        (Ice in loadout) or
                        (Speedball in loadout)
                        )
                    )
                )
        ),
        ("ExcavationSiteL", "ConstructionSiteL"): lambda loadout: (
            (redo jumpAble in loadout) and
            (
                (canUsePB in loadout) or
                (
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout) or
                        (Ice in loadout) or
                        (Speedball in loadout)
                        ) and
                    (pinkDoor in loadout) and
                    (Morph in loadout) and
                    (Screw in loadout) and
                    ((wave in loadout) or (Spazer in loadout)) and
                    (Bombs in loadout)
                    )
                )
        ),
        ("ExcavationSiteL", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ( redo
                (
                    ((wave in loadout) or (Spazer in loadout)) and
                    (Bombs in loadout)
                    ) or
                (
                    (Screw in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout) or
                        (Ice in loadout) or
                        (Speedball in loadout)
                        )
                    )
                )
        ),
        ("WestCorridorR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and (
                (pinkDoor in loadout) or
                (Charge in loadout) or
                (Ice in loadout) or
                (wave in loadout) or
                (breakIce in loadout) or
                (canBomb in loadout) or  # casual needed pb?
                (Spazer in loadout)
            )
        ),
        ("WestCorridorR", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            ((
                (canUsePB in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or (
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    ) and
                (pinkDoor in loadout) and
                (canBomb in loadout) and
                (Screw in loadout)
            ))
        ),
        ("WestCorridorR", "ConstructionSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            ( redo
                (canUsePB in loadout) or
                (
                    (pinkDoor in loadout) and
                    (Morph in loadout) and
                    (Screw in loadout) and
                    ((wave in loadout) or (Spazer in loadout)) and
                    (Bombs in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout) or
                        (Ice in loadout) or
                        (Speedball in loadout)
                        )
                    )
                )
        ),
        ("WestCorridorR", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
                )
             )
        ),
        ("FoyerR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ( redo
                (
                    (canUsePB in loadout) and
                    ((wave in loadout) or (Spazer in loadout)) and
                    (Bombs in loadout)
                    ) or
                (
                    (pinkDoor in loadout) and
                    (Screw in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
        ),
        ("FoyerR", "WestCorridorR"): lambda loadout: (
            (jumpAble in loadout) and
            ((
                (canUsePB in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (pinkDoor in loadout) and
                (canBomb in loadout) and
                (Screw in loadout) and
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
            ))
        ),
        ("FoyerR", "ConstructionSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            ((
                (canUsePB in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout)
                    )
                ) or
             (
                (Morph in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
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
            ((canUsePB in loadout) or (
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                ) and
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (pinkDoor in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or
             (
                ( redo 
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    ) and
                (Morph in loadout) and
                (Screw in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
            ((
                (canUsePB in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo 
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
                
            ) or (
                (Morph in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "AlluringCenoteR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo 
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
            ))
        ),
        ("AlluringCenoteR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or ( redo 
                (Screw in loadout) and
                (pinkDoor in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout)
                    )
            ))
        ),
        ("AlluringCenoteR", "WestCorridorR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo 
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
            ))
        ),
        ("AlluringCenoteR", "FoyerR"): lambda loadout: (
            # matched!
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
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (pinkDoor in loadout) and
                ( redo
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
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
            casual dark visor and gravity suit
            (wave in loadout) and
            (canBomb in loadout)
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            casual dark visor
            (wave in loadout) and
            (
                # expert
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                # casual and expert
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                # expert
                (Bombs in loadout)
                ) 
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, DarkVisor, wave, canBomb)
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout)  and casual underwater
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            (
                # expert
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                # casual and expert
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                # expert
                (Bombs in loadout)
                )
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, wave) and casual dark visor
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, DarkVisor, wave)
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and casual underwater and (spacejump or SpeedBooster)
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and casual replaced super with wave
            (canBomb in loadout) and casual needed pb
            (DarkVisor in loadout) and
            (
                # expert
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                # casual and expert
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                # expert
                (Bombs in loadout)
                )
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
             casual darkvisor
            (
                # expert
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                # casual and expert
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                # expert
                (Bombs in loadout)
                )
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            casual DarkVisor and underwater
            (
                # expert
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                # casual and expert
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                # expert
                (Bombs in loadout)
                )
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canFly in loadout) or
             (SpeedBooster in loadout) or
             (HiJump in loadout) or  # expert add
             (Ice in loadout) or
             ((Morph in loadout) and (Speedball in loadout))  # expert add
             )
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (SpeedBooster in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
                )
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            condenser
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (canOpen(WestTerminalAccessL) in loadout) and
            (jumpAble in loadout) and (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout) or
                (HiJump in loadout) or  # expert add
                ((Morph in loadout) and (Speedball in loadout))  # expert add
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
            condenser and
              # expert add this v ?
            ((HiJump in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (Grapple in loadout) or
             (Speedball in loadout))
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            casual need (canFly or SpeedBooster or Ice)
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
            (breakIce in loadout) and  # expert add
            (SpeedBooster in loadout) and
            condenser
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
            # canOpen needed?  There was also a canOpen a little bit above here that expert didn't have
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            condenser
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            condenser
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            condenser and

            # expert add v
            ((HiJump in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (Grapple in loadout) or
             (Speedball in loadout))
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            condenser
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and  # epxert add
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (breakIce in loadout) and
            condenser
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (brook in loadout) and  # casual add
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout)
            # Note: If no canFly and no speedbooster,
            # this requires a wall jump around a 2 tile ledge (in Water Garden)
            # I think that's not too hard for casual, but some people might not like it.
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (brook in loadout) and  # casual add
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Morph in loadout) and  # expert brook
            (loadout.has_any(GravitySuit, Ice, HiJump, Speedball, SpaceJump, Bombs, SpeedBooster))  # expert brook
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and  # expert brook
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)  # expert add
            ) and
            (loadout.has_any(GravitySuit, Ice, HiJump, Speedball, SpaceJump, Bombs, SpeedBooster))  # expert brook
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Morph in loadout) and  # expert brook
            (loadout.has_any(GravitySuit, Ice, HiJump, Speedball, SpaceJump, Bombs, SpeedBooster))  # expert brook
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            redo
            # TODO: are these parentheses in the right place? (mixed and/or at the same level)
            ((canBomb in loadout) or (Screw in loadout) or (
                (SpeedBooster in loadout) and
                (Morph in loadout)
            ) and
            (MetroidSuit in loadout))
        ),  # Test doing NorakPerimeterBL spark with/out morph

        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (veranda in loadout) and  # casual add
            (waterGardenBottom in loadout)  # includes canBomb for the bomb blocks in Norak Perimeter
        ),
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and  # expert brook
            (loadout.has_any(GravitySuit, Ice, HiJump, Speedball, SpaceJump, Bombs, SpeedBooster)) and  # expert brook
            ((canBomb in loadout) or
             (Screw in loadout) or
             (SpeedBooster in loadout))  # expert add
        ),  # and? anything else?
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            # TODO: are these parentheses in the right place? (mixed and/or at the same level)
            (jumpAble in loadout) and
            ((canBomb in loadout) or
             (Screw in loadout) or
             ((SpeedBooster in loadout) and
              (Morph in loadout)) and
            (MetroidSuit in loadout)
             ) redo
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
            redo
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (infernalSequestration in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            redo
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Super in loadout) and
            (varia_or_hell_run(750) in loadout) and  # TODO: want to make expert require less energy than casual?
            (electricHyper in loadout)
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorEL"): lambda loadout: (  # TODO: expert deleted this entry from the dict?
            False  # One way logic not respected, intended
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
        ("SequesteredInfernoL", "VulnarDepthsElevatorEL"): lambda loadout: (  # expert added entry to dict
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (infernalSequestration in loadout)
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            redo
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (infernalSequestration in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            False  # One way Hive Burrow not in logic
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            redo
            loadout.has_all(jumpAble, canBomb, Super, varia_or_hell_run(750), infernalSequestration)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorEL"): lambda loadout: ( need entry?
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            redo
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout)
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            False  # One way hive burrow not in logic
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            redo
            loadout.has_all(jumpAble, canBomb, pinkDoor, varia_or_hell_run(750), infernalSequestration)
        ),
    },
    "Geothermal": {
        ("MagmaPumpL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            # matched (cept varia)
            (jumpAble in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canBomb in loadout)
        ),
        ("MagmaPumpL", "IntakePumpR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canBomb in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "IntakePumpR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
        ("GeneratorAccessTunnelL", "MagmaPumpL"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
    },
    "DrayLand": {
        ("ElevatorToMagmaLakeR", "MagmaPumpAccessR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            loadout.has_all(jumpAble, Super, canBomb, varia_or_hell_run(450))
        ),
        ("FieryGalleryL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            casual Speedball
            (varia_or_hell_run(550) in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("RagingPitL", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (canUsePB in loadout)
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, varia_or_hell_run(450), icePod)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (hotSpring in loadout)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
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
            loadout.has_all(jumpAble, canBomb, varia_or_hell_run(450), Super, icePod)
            casual Speedball
            # can you screw into raging pit?
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(250) in loadout) and
            (icePod in loadout)
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
            loadout.has_all(jumpAble, varia_or_hell_run(250), icePod)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (hotSpring in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
            )
        ),
        ("SporousNookL", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (hotSpring in loadout)
        ),  # screw into raging pit?
        ("SporousNookL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
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
            (jumpAble in loadout) and
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
