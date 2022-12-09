from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicCommon import canUsePB, energy_req, varia_or_hell_run
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places.
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

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


exitSpacePort = LogicShortcut(lambda loadout: (
    True
    # TODO: Why did one definition have somethings different?
    # (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
))
canBomb = LogicShortcut(lambda loadout: (
    (Morph in loadout) and loadout.has_any(Bombs, PowerBomb)
))
# TODO: I think there may be places where canBomb is used for bomb jumping
# even though it might only have PBs
jumpAble = LogicShortcut(lambda loadout: (
    loadout.has_all(exitSpacePort, GravityBoots)
))
canFly = LogicShortcut(lambda loadout: (
    (jumpAble in loadout) and ((SpaceJump in loadout) or loadout.has_all(Morph, Bombs))
))
wave = LogicShortcut(lambda loadout: (
    (Wave in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
))
breakIce = LogicShortcut(lambda loadout: (
    (Plasma in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
))
missileDamage = LogicShortcut(lambda loadout: (
    loadout.has_any(Missile, Super)
))
pinkDoor = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))
vulnar = LogicShortcut(lambda loadout: (
    loadout.has_all(jumpAble, pinkDoor)
))
""" jumpAble and pinkDoor """

underwater = LogicShortcut(lambda loadout: (
    (jumpAble in loadout) and (
        (GravitySuit in loadout) or (HiJump in loadout)
    )
))
icePod = LogicShortcut(lambda loadout: (
    ((Ice in loadout) and (missileDamage in loadout)) or ((Charge in loadout) and (Hypercharge in loadout))
))
suzi = LogicShortcut(lambda loadout: (
    loadout.has_all(jumpAble, SpeedBooster, Super, canUsePB, wave, GravitySuit)
))
""" to complete all the suzi cyphers """
electricHyper = LogicShortcut(lambda loadout: (
    (MetroidSuit in loadout) or (
        (Charge in loadout) and
        (Hypercharge in loadout)
    )
))
""" hyper beam when electricity is available """

plasmaWaveGate = LogicShortcut(lambda loadout: (
    ((Plasma in loadout) and (wave in loadout)) or
    ((Hypercharge in loadout) and (Charge in loadout))
))
""" the switches that are blocked by plasma+wave barriers """

hotSpring = LogicShortcut(lambda loadout: (
    (GravitySuit in loadout) or
    (Speedball in loadout) or
    ((HiJump in loadout) and (Ice in loadout))
))
""" traverse "Hot Spring" between Sporous Nook and Vulnar Depths Elevator W """


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
            (Missile in loadout) and
            (Morph in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(jumpAble, Missile, Morph, SpeedBooster, energy_req(180))
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
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
            (Morph in loadout)
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
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
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
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
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (vulnar in loadout) and
            (Morph in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (vulnar in loadout) and
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            (jumpAble in loadout)
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (vulnar in loadout) and
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
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (vulnar in loadout) and
            (Morph in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            (vulnar in loadout) and
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (jumpAble in loadout)
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            (vulnar in loadout) and
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
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
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
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple)
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
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
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster)
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple)
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, SpeedBooster)
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
                (canBomb in loadout) or
                (Spazer in loadout)
            )
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(FoyerR) in loadout) and
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
            (jumpAble in loadout) and
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
            (
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
                (canBomb in loadout) or
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
                (
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
            (
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
                (
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
                (
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
                (
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
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (pinkDoor in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or
             (
                (
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
                (
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
                (
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
            ) or (
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
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
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
                (
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
            (wave in loadout) and
            (canBomb in loadout)
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (wave in loadout) and
            (
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
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
            (wave in loadout)
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            (
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                (Bombs in loadout)
                )
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, wave)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, DarkVisor, wave)
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            (
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                (Bombs in loadout)
                )
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
            (
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                (Bombs in loadout)
                )
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (
                ((HiJump in loadout) and (Ice in loadout)) or
                ((HiJump in loadout) and (Speedball in loadout)) or
                (SpaceJump in loadout) or
                (SpeedBooster in loadout) or
                (Bombs in loadout)
                )
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canFly in loadout) or
             (SpeedBooster in loadout) or
             (HiJump in loadout) or
             (Ice in loadout) or
             ((Morph in loadout) and (Speedball in loadout))
             )
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (SpeedBooster in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout)
                )
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
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout) or
                (HiJump in loadout) or
                ((Morph in loadout) and (Speedball in loadout))
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
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                ) and
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
            (breakIce in loadout) and
            (SpeedBooster in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
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
            (jumpAble in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (SpeedBooster in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                ) and
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
            (breakIce in loadout) and
            (SpeedBooster in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (SpeedBooster in loadout) and
            (
                (
                    (Ice in loadout) or
                    (GravitySuit in loadout) or
                    (Grapple in loadout) or
                    ((Speedball in loadout) and (HiJump in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (Speedball in loadout) or
                    (HiJump in loadout)
                    )
                )
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout)))
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout))) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout)))
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout)))
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Morph in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             (HiJump in loadout) or
             (Speedball in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (SpeedBooster in loadout))
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)
                ) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             (HiJump in loadout) or
             (Speedball in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (SpeedBooster in loadout))
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout))) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Morph in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             (HiJump in loadout) or
             (Speedball in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (SpeedBooster in loadout))
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or
             (Screw in loadout) or
             ((SpeedBooster in loadout) and
              (Morph in loadout)) and
            (MetroidSuit in loadout)
             )
        ), #Test doing NorakPerimeterBL spark with/out morph
            
        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             ((HiJump in loadout) and (Speedball in loadout)))
        ), 
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            ((GravitySuit in loadout) or
             (Ice in loadout) or
             (HiJump in loadout) or
             (Speedball in loadout) or
             (SpaceJump in loadout) or
             (Bombs in loadout) or
             (SpeedBooster in loadout)) and
            ((canBomb in loadout) or
             (Screw in loadout) or
             (SpeedBooster in loadout))
        ), #and? anything else?
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or
             (Screw in loadout) or
             ((SpeedBooster in loadout) and
              (Morph in loadout)) and
            (MetroidSuit in loadout)
             )
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
            False  #One way logic not respected, intended
        ),
        ("VulnarDepthsElevatorER", "SequesteredInfernoL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (electricHyper in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Super in loadout) and
            (varia_or_hell_run(750) in loadout) and  # TODO: want to make expert require less energy than casual?
            (electricHyper in loadout)
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
        ("SequesteredInfernoL", "VulnarDepthsElevatorEL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (electricHyper in loadout)
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (electricHyper in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            False  # One way
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, Super, varia_or_hell_run(750), electricHyper)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorEL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout)
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            False  # One way
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, pinkDoor, varia_or_hell_run(750), electricHyper)
        ),
    },
    "Geothermal": {
        ("MagmaPumpL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (jumpAble in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canBomb in loadout)
        ),
        ("MagmaPumpL", "IntakePumpR"): lambda loadout: (
            (jumpAble in loadout) and
            ((GravitySuit in loadout) or
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
                (GravitySuit in loadout) or
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
                (GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or
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
        ),
        ("ReservoirMaintenanceTunnelR", "GeneratorAccessTunnelL"): lambda loadout: (
            (jumpAble in loadout) and
            (
                (GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or
             (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (
                (energy_req(250) in loadout) or
                (breakIce in loadout)
                ) and
            (varia_or_hell_run(350) in loadout)
        ),
        ("IntakePumpR", "GeneratorAccessTunnelL"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (
                (energy_req(250) in loadout) or
                (breakIce in loadout)
                )
        ),
        ("ThermalReservoir1R", "MagmaPumpL"): lambda loadout: (
            (jumpAble in loadout) and
            (
                (GravitySuit in loadout) or
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
                (GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or
             (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (
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
                (GravitySuit in loadout) or
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
                (GravitySuit in loadout) or
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
            ((GravitySuit in loadout) or (HiJump in loadout)) and
            (Screw in loadout) and
            (MetroidSuit in loadout) and
            (
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
                    (GravitySuit in loadout) and
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
                    (GravitySuit in loadout) and
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
            (varia_or_hell_run(550) in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (Super in loadout) and
            (Morph in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or
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
            # can you screw into raging pit?
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(250) in loadout) and
            (icePod in loadout)
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout) and
            (pinkDoor in loadout) and
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
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(550) in loadout) and
            (pinkDoor in loadout) and
            (Morph in loadout) and
            (
                (canBomb in loadout) or
                (Screw in loadout) or
                (SpeedBooster in loadout)) and
            (
                (icePod in loadout) or
                (
                    (canUsePB in loadout) and
                    (
                        (GravitySuit in loadout) or
                        (HiJump in loadout)
                        )
                    )
                )
        ),
        ("PlacidPoolR", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
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
                )
        ), #screw into raging pit?
        ("PlacidPoolR", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, varia_or_hell_run(250), icePod)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Morph in loadout) and
            (pinkDoor in loadout) and
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
            (Morph in loadout) and
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

location_logic: LocationLogicType = {
    "Impact Crater: AccelCharge": lambda loadout: (
        (exitSpacePort in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (Spazer in loadout) and
        ((HiJump in loadout) or (SpeedBooster in loadout) or (canFly in loadout))
    ),
    "Subterranean Burrow": lambda loadout: (
        (exitSpacePort in loadout) and
        ((Morph in loadout) or (GravityBoots in loadout))
    ),
    "Sandy Cache": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((Morph in loadout) or (GravitySuit in loadout))
    ),
    "Submarine Nest": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (
                (Morph in loadout) and
                (Speedball in loadout)
                )
            )
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Speedball in loadout)
                )
            ) and
        (
            (canUsePB in loadout) or
            (
                (canBomb in loadout) and
                (DarkVisor in loadout)
                )
            )
    ),
    "Benthic Cache Access": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Super in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Speedball in loadout)
                )
            )
    ),
    "Benthic Cache": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (underwater in loadout) and
        (canBomb in loadout) and
        (Super in loadout)
    ), #better underwater escape?
    "Ocean Vent Supply Depot": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (underwater in loadout) and
        (Morph in loadout) and
        ((Super in loadout) or (
            (GravitySuit in loadout) and
            (Screw in loadout)
        ))
    ), #better underwater escape?
    "Sediment Flow": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        (Super in loadout)
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        (FieldAccessL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canBomb in loadout)
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (vulnar in loadout) and
        (canUsePB in loadout) and
        (Screw in loadout) and
        (MetroidSuit in loadout)
    ),
    "Grand Vault": lambda loadout: (
        (vulnar in loadout) and (Grapple in loadout)
    ),
    "Cistern": lambda loadout: (
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (canBomb in loadout)
    ),
    "Warrior Shrine: ETank": lambda loadout: (
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (canUsePB in loadout)
    ),
    "Vulnar Caves Entrance": lambda loadout: (
        (vulnar in loadout)
    ),
    "Crypt": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (
            (pinkDoor in loadout) or
            (
                (
                    (HiJump in loadout) or
                    (SpaceJump in loadout) or
                    (Speedball in loadout)
                    ) and
                    (GravitySuit in loadout) or
                    (
                        (HiJump in loadout) and
                        (
                            (Speedball in loadout) or
                            (Ice in loadout)
                            )
                        )
                    )
             
                ) and
        (
            (wave in loadout) or
            (Bombs in loadout)
            )
    ),
    "Archives: SpringBall": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout)
    ),
    "Archives: SJBoost": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout) and (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: ETank": lambda loadout: (  # front
        (vulnar in loadout) and
        (Morph in loadout) and
        (
            (Super in loadout) or
            (canUsePB in loadout)
            )
    ), #hacky way of ensuring 20 ammo
    "Eribium Apparatus Room": lambda loadout: (
        (FieldAccessL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canBomb in loadout)
    ),
    "Hot Spring": lambda loadout: (
        ((SporousNookL in loadout) or (
            (EleToTurbidPassageR in loadout) and
            (varia_or_hell_run(550) in loadout)
        )) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (hotSpring in loadout)
    ),
    "Epiphreatic Crag": lambda loadout: (
        (ConstructionSiteL in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (Screw in loadout) and
                (
                    (canBomb in loadout) or
                    (Speedball in loadout)
                    )
                ) or
            (
                (Speedball in loadout) and
                (HiJump in loadout)
                )
            )
    ),
    "Mezzanine Concourse": lambda loadout: (
        (MezzanineConcourseL in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (
            (canFly in loadout) or
            (SpeedBooster in loadout) or
            (HiJump in loadout) or
            (Ice in loadout) or
            (Speedball in loadout)
            )
    ),
    "Greater Inferno": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Super in loadout) and
        (varia_or_hell_run(850) in loadout) and
        (MetroidSuit in loadout) and
        (
            (GravitySuit in loadout) or
            (Speedball in loadout)
            )
    ),
    "Burning Depths Cache": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (varia_or_hell_run(550) in loadout) and
        (MetroidSuit in loadout) and
        ((Spazer in loadout) or (Wave in loadout) or (
            (Charge in loadout) and
            (Bombs in loadout)
        ))
    ),
    "Mining Cache": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (canBomb in loadout) and
        (
            (EleToTurbidPassageR in loadout) and
            (varia_or_hell_run(550) in loadout)
        ) or
        (
            (SporousNookL in loadout) and
            (hotSpring in loadout)
        )
    ),
    "Infested Passage": lambda loadout: (
        (jumpAble in loadout) and
        (
            (
                (VulnarDepthsElevatorEL in loadout) and
                (canBomb in loadout) and
                (varia_or_hell_run(450) in loadout)
                ) or
            (
                (SequesteredInfernoL in loadout) and
                (electricHyper in loadout) and
                (Morph in loadout) and
                (icePod in loadout) and
                (varia_or_hell_run(250) in loadout)
                )
            )
    ),
    "Fire's Boon Shrine": lambda loadout: (
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (Morph in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (varia_or_hell_run(750) in loadout) and
            (canBomb in loadout) and
            (wave in loadout)
        ))
    ),
    "Fire's Bane Shrine": lambda loadout: (
        (icePod in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(450) in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(350) in loadout)
        ))
    ),
    "Ancient Shaft": lambda loadout: (
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (varia_or_hell_run(650) in loadout) and
        (
            (MetroidSuit in loadout) or
            (energy_req(1250) in loadout) or
            (
                (Varia in loadout) and
                (energy_req(650) in loadout) 
                )
            ) and
        (
            (
                (VulnarDepthsElevatorEL in loadout) and
                (canBomb in loadout) and
                (icePod in loadout)
            ) or (
                (SequesteredInfernoL in loadout) and
                (electricHyper in loadout)
                )
            )
    ),
    "Gymnasium": lambda loadout: (
        (jumpAble in loadout) and
        (Grapple in loadout) and
        (
            (
                (VulnarDepthsElevatorEL in loadout) and
                (canBomb in loadout) and
                (icePod in loadout) and
                (varia_or_hell_run(450) in loadout)
                ) or
            (
                (SequesteredInfernoL in loadout) and
                (electricHyper in loadout) and
                (Morph in loadout) and
                (varia_or_hell_run(250) in loadout)
                )
            )
    ),
    "Electromechanical Engine": lambda loadout: (
        (jumpAble in loadout) and
        (Grapple in loadout) and
        (varia_or_hell_run(350) in loadout) and
        (canBomb in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (
                (GravitySuit in loadout) or
                (HiJump in loadout) or
                (Ice in loadout)
                ) and
            (Screw in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (MetroidSuit in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout)
        ))
    ),
    "Depressurization Valve": lambda loadout: (
        (jumpAble in loadout) and
        (Morph in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout)) and
            (Screw in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (MetroidSuit in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout)
        ))
    ),
    "Loading Dock Storage Area": lambda loadout: (
        LoadingDockSecurityAreaL in loadout
    ),
    "Containment Area": lambda loadout: (
        (jumpAble in loadout) and
        ((
            (FoyerR in loadout) and
            (canBomb in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ) or
        (
            (AlluringCenoteR in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (canUsePB in loadout)
        ))
    ),
    "Briar: SJBoost": lambda loadout: (  # top
        (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),
    "Shrine Of Fervor": lambda loadout: (
        (jumpAble in loadout) and
        (
            (
                (NorakBrookL in loadout) and
                (Morph in loadout) and
                ((GravitySuit in loadout) or
                 (Ice in loadout) or
                 (HiJump in loadout) or
                 (Speedball in loadout) or
                 (SpaceJump in loadout) or
                 (Bombs in loadout) or
                 (SpeedBooster in loadout))
                ) or
            (
                (NorakPerimeterTR in loadout) and
                (MetroidSuit in loadout)
                ) or
            (
                (NorakPerimeterBL in loadout) and
                ((canBomb in loadout) or
                 (Screw in loadout) or
                 (SpeedBooster in loadout))
                )
            )
    ),
    "Chamber Of Wind": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (SpeedBooster in loadout) and
        (
            (canBomb in loadout) or
            (
                (Screw in loadout) and
                (Speedball in loadout) and
                (Morph in loadout)
                )
            )
    ),
    "Water Garden": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (SpeedBooster in loadout)
    ),
    "Crocomire's Energy Station": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
    "Wellspring Cache": lambda loadout: (
        (ElevatorToWellspringL in loadout) and
        (jumpAble in loadout) and
        loadout.has_any(HiJump, Speedball, Ice, GravitySuit) and
        (Super in loadout) and
        (Morph in loadout)
    ),
    "Frozen Lake Wall: DamageAmp": lambda loadout: (
        (ElevatorToCondenserL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),
    "Grand Promenade": lambda loadout: (
        (jumpAble in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Summit Landing": lambda loadout: (
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Snow Cache": lambda loadout: (
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Reliquary Access": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (DarkVisor in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Syzygy Observatorium": lambda loadout: (
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (MetroidSuit in loadout) and
            (energy_req(350) in loadout)
        ) or (
            (Hypercharge in loadout) and
            (Charge in loadout)
        )) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Armory Cache 2": lambda loadout: (
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        )) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Armory Cache 3": lambda loadout: (
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        )) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Drawing Room": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout))
                 )
                )
            )   
    ),
    "Impact Crater Overlook": lambda loadout: (  # TODO: check an area door, don't assume we start in this area
        ((canFly in loadout) or (SpeedBooster in loadout)) and
        (canBomb in loadout) and
        ((canUsePB in loadout) or (Super in loadout))
    ),
    "Magma Lake Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (icePod in loadout) and (Morph in loadout)
    ),
    "Shrine Of The Animate Spark": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (suzi in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout) and
        (energy_req(350) in loadout)
    ),
    "Docking Port 4": lambda loadout: (  # (4 = letter Omega)
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout)
        )
    ),
    "Ready Room": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (Super in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Super in loadout) and
            (
                (Grapple in loadout) or
                (Xray in loadout) or
                (Ice in loadout)
                )
        )
    ),
    "Torpedo Bay": lambda loadout: (
        True
    ),
    "Extract Storage": lambda loadout: (
        (
            (canUsePB in loadout) and
            (spaceDrop not in loadout)
        ) or
        (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (
                (Grapple in loadout) or
                (
                    (Super in loadout) and
                    (
                        (Xray in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "Impact Crater Alcove": lambda loadout: (  # TODO: check an area door, don't assume we start in this area
        (jumpAble in loadout) and
        ((canFly in loadout) or (SpeedBooster in loadout)) and
        (canBomb in loadout)
    ),
    "Ocean Shore: bottom": lambda loadout: (
        OceanShoreR in loadout
    ),
    "Ocean Shore: top": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout)
    ),
    "Sandy Burrow: ETank": lambda loadout: (  # top
        (OceanShoreR in loadout) and
        (underwater in loadout) and
        ((
            (GravitySuit in loadout) and
            ((Screw in loadout) or (canBomb in loadout))
        ) or (
            ((Speedball in loadout) or (HiJump in loadout)) and
            (canBomb in loadout)
        ))
    ),
    "Submarine Alcove": lambda loadout: (
        (jumpAble in loadout) and
        (Morph in loadout) and
        (
                (GravitySuit in loadout) or
                (HiJump in loadout) or
                (
                    (Speedball in loadout) and
                    (Ice in loadout)
                    )
                ) and
        ((
            (OceanShoreR in loadout) and
            (
                (Super in loadout) or
                (
                    (pinkDoor in loadout) and
                    (
                    (DarkVisor in loadout) or
                    (
                        (GravitySuit in loadout) and
                        (Screw in loadout)
                        )
                    )
                    )
                )
            ) or
         (
             (EleToTurbidPassageR in loadout) and
             (Super in loadout) and
             (Speedball in loadout)
             )
         )
    ), #check for speedball+ice entry
    "Sediment Floor": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (Super in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (
                (Speedball in loadout) and
                (Ice in loadout)
                )
            )
    ),
    "Sandy Gully": lambda loadout: (
        (OceanShoreR in loadout) and (underwater in loadout) and (Super in loadout)
    ),
    "Hall Of The Elders": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            (Ice in loadout)
        ) or (pinkDoor in loadout))
    ),
    "Warrior Shrine: AmmoTank bottom": lambda loadout: (
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (Morph in loadout) and (pinkDoor in loadout)
    ),
    "Warrior Shrine: AmmoTank top": lambda loadout: (
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout)
    ),
    "Path Of Swords": lambda loadout: (
        (vulnar in loadout) and
        (
            (canBomb in loadout) or
            (
                (Morph in loadout) and
                (Screw in loadout)
                )
            )
    ),
    "Auxiliary Pump Room": lambda loadout: (
        (vulnar in loadout) and (canBomb in loadout)
    ),
    "Monitoring Station": lambda loadout: (  # TODO: check an area door, don't assume that we start by vulnar
        (vulnar in loadout) and
        (Morph in loadout)
    ),
    "Sensor Maintenance: AmmoTank": lambda loadout: (  # back
        (vulnar in loadout) and
        (canBomb in loadout) and
        (
            (Super in loadout) or
            (canUsePB in loadout)
            )
    ),
    "Causeway Overlook": lambda loadout: (
        (CausewayR in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout)
    ),
    "Placid Pool": lambda loadout: (
        (PlacidPoolR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (icePod in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout)
            )
    ),
    "Blazing Chasm": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (varia_or_hell_run(850) in loadout) and
        (MetroidSuit in loadout)
    ),
    "Generator Manifold": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (canBomb in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout))
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (varia_or_hell_run(250) in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ))
    ),
    "Fiery Crossing Cache": lambda loadout: (
        (RagingPitL in loadout) and
        (jumpAble in loadout) and
        (varia_or_hell_run(550) in loadout) and
        (canUsePB in loadout)
    ),
    "Dark Crevice Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout))
    ),
    "Ancient Basin": lambda loadout: (
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (icePod in loadout) and
            (varia_or_hell_run(450) in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (Morph in loadout) and
            (varia_or_hell_run(350) in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (canBomb in loadout) and
            (wave in loadout) and
            (varia_or_hell_run(750) in loadout)
        ))
    ),
    "Central Corridor: right": lambda loadout: (
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (
            (FoyerR in loadout) or
            (
                (ConstructionSiteL in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
                ) or
            (
                (WestCorridorR in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
                )
            )        
    ),
    "Briar: AmmoTank": lambda loadout: (  # bottom
        (jumpAble in loadout) and
        (Morph in loadout) and
        ((
            (NorakBrookL in loadout) and
            (
                (GravitySuit in loadout) or
                (Ice in loadout) or
                (HiJump in loadout) or
                (Speedball in loadout) or
                (SpaceJump in loadout) or
                (Bombs in loadout) or
                (SpeedBooster in loadout)
                )
            ) or
         (
             (NorakPerimeterTR in loadout) and
             (MetroidSuit in loadout)
             ) or
         (
             (NorakPerimeterBL in loadout) and
             (canBomb in loadout)
             )
         ) 
    ),
    "Icy Flow": lambda loadout: (
        (MezzanineConcourseL in loadout) and
        (jumpAble in loadout) and
        (SpeedBooster in loadout) and
        (breakIce in loadout)
    ),
    "Ice Cave": lambda loadout: (
        (jumpAble in loadout) and
        (breakIce in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout)))
                )
            )
    ),
    "Antechamber": lambda loadout: (
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout)))
                )
            )
    ),
    "Eddy Channels": lambda loadout: (
        (EleToTurbidPassageR in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (Ice in loadout)
            ) and
        (Morph in loadout) and
        (Speedball in loadout) and
        (Super in loadout)
    ),
    "Tram To Suzi Island": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (Spazer in loadout) and
        (Morph in loadout)
    ),
    "Portico": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (Super in loadout) and
        (energy_req(350) in loadout)
    ),
    "Tower Rock Lookout": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (pinkDoor in loadout) and
        (energy_req(350) in loadout) and
        (GravitySuit in loadout) and
        (
            (
                (SpaceJump in loadout) and
                (HiJump in loadout)
                ) or
            (
                (Bombs in loadout) and
                (Morph in loadout)
                ) or
            (SpeedBooster in loadout)
            )
    ),
    "Reef Nook": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (pinkDoor in loadout) and
        (energy_req(350) in loadout) and
        (GravitySuit in loadout) and
        (Morph in loadout) and
        (
            (
                (SpaceJump in loadout) and
                (HiJump in loadout)
                ) or
            (Bombs in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Saline Cache": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (Super in loadout) and
        (energy_req(350) in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Speedball in loadout) and
                (Morph in loadout)
                )
            )
    ),
    "Enervation Chamber": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (suzi in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout)
    ),
    "Weapon Locker": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (pinkDoor in loadout)
        ) or
        (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (pinkDoor in loadout) and
            (
                (Grapple in loadout) or
                (
                    (Super in loadout) and
                    (
                        (Xray in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "Aft Battery": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (Morph in loadout)
        ) or
        (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Morph in loadout) and
            (
                (Grapple in loadout) or
                (
                    (Super in loadout) and
                    (
                        (Xray in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "Forward Battery": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (pinkDoor in loadout) and
            (Morph in loadout)
        ) or
        (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (Grapple in loadout) and
            (MetroidSuit in loadout) and
            (pinkDoor in loadout) and
            (
                (Grapple in loadout) or
                (
                    (Super in loadout) and
                    (
                        (Xray in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "Gantry": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (pinkDoor in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Grapple in loadout) and
            (pinkDoor in loadout) and
            (
                (Grapple in loadout) or
                (
                    (Super in loadout) and
                    (
                        (Xray in loadout) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "Garden Canal": lambda loadout: (
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Spazer in loadout) and
        (NorakPerimeterBL in loadout)
    ),
    "Sandy Burrow: AmmoTank": lambda loadout: (  # bottom
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (
                    (Speedball in loadout) or
                    (Ice in loadout)
                    )
                )
            )
    ),
    "Trophobiotic Chamber": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout)
    ),
    "Waste Processing": lambda loadout: (
        (jumpAble in loadout) and
        (SpeedBooster in loadout) and
        ((
            (SubbasementFissureL in loadout) and
            (canUsePB in loadout)
        ) or (
            (CellarR in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout)
        ) or (
            (FieldAccessL in loadout) and
            (pinkDoor in loadout) and
            (wave in loadout) and
            (canBomb in loadout)
        ) or (
            (TransferStationR in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout) and
            (canBomb in loadout)
        ))
    ),
    "Grand Chasm": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (Screw in loadout)
    ),
    "Mining Site 1": lambda loadout: (  # (1 = letter Alpha)
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (pinkDoor in loadout) and
        (
            (
                (FieryGalleryL in loadout) and
                (varia_or_hell_run(550) in loadout)
            ) or
            (
                (SporousNookL in loadout) and
                (hotSpring in loadout)
            )
        )
    ),
    "Colosseum": lambda loadout: (  # GT
        (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (Varia in loadout) and (Charge in loadout)
    ),
    "Lava Pool": lambda loadout: (
        loadout.has_all(jumpAble, varia_or_hell_run(950), MetroidSuit, canBomb) and
        (
            (FieryGalleryL in loadout) or
            (
                (SporousNookL in loadout) and
                (hotSpring in loadout)
            )
        )
    ),
    "Hive Main Chamber": lambda loadout: (
        (jumpAble in loadout) and
        (
            (
                (VulnarDepthsElevatorEL in loadout) and
                (varia_or_hell_run(650) in loadout) and
                (canBomb in loadout)
                ) or
            (
                (SequesteredInfernoL in loadout) and
                (varia_or_hell_run(250) in loadout) and
                (Morph in loadout) and
                (icePod in loadout)
                )
            )
    ),
    "Crossway Cache": lambda loadout: (
        (jumpAble in loadout) and
        (
            (VulnarDepthsElevatorEL in loadout) and
            (varia_or_hell_run(650) in loadout) and
            (canBomb in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (electricHyper in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (Super in loadout) and
            (varia_or_hell_run(750) in loadout) and
            (canBomb in loadout) and
            (wave in loadout)
        )
    ),
    "Slag Heap": lambda loadout: (  # Consider bath counts
        (canBomb in loadout) and
        (jumpAble in loadout) and
        (varia_or_hell_run(950) in loadout) and
        (MetroidSuit in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            ((Ice in loadout) or ((Hypercharge in loadout) and (Charge in loadout)))
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (wave in loadout)
        ))
    ),
    "Hydrodynamic Chamber": lambda loadout: (
        (jumpAble in loadout) and
        (Spazer in loadout) and
        (Morph in loadout) and
        (
            (
                (ConstructionSiteL in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout) and
                (Screw in loadout)
                ) or
            (
                (WestCorridorR in loadout) and
                (pinkDoor in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    ((Morph in loadout) and (Speedball in loadout))
                    )
                ) or
            (
                (FoyerR in loadout) and
                (canBomb in loadout) and
                (Screw in loadout)
                )
            )
    ),
    "Central Corridor: left": lambda loadout: (
        (FoyerR in loadout) and
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout) and
        (Morph in loadout)
    ),
    "Restricted Area": lambda loadout: (
        (jumpAble in loadout) and
        (MetroidSuit in loadout) and
        (
            (
                (WestCorridorR in loadout) and
                (pinkDoor in loadout) and
                (Screw in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
                ) or
            (
                (FoyerR in loadout) and
                (canBomb in loadout)
                ) or
            (
                (ConstructionSiteL in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
                )
            )
    ),
    "Foundry": lambda loadout: (
        (jumpAble in loadout) and
        (Morph in loadout) and
        (
            (
                (WestCorridorR in loadout) and
                (pinkDoor in loadout) and
                (Screw in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    (Speedball in loadout)
                    )
                ) or
            (
                (FoyerR in loadout) and
                (canBomb in loadout)
                ) or
            (
                (ConstructionSiteL in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
                )
            )
    ),
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (canFly in loadout)
    ), #might not always have room for speed
    "Glacier's Reach": lambda loadout: (
        (jumpAble in loadout) and
        (energy_req(350) in loadout) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout)))
                )
            )
    ),
    "Sitting Room": lambda loadout: (
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (
            (Bombs in loadout) or
            (Speedball in loadout)
            ) and
        (
            (WestTerminalAccessL in loadout) or
            (
                (MezzanineConcourseL in loadout) and
                ((canFly in loadout) or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout) or
                 (Ice in loadout) or
                 ((Morph in loadout) and (Speedball in loadout)))
                )
            )
    ),
    "Suzi Ruins Map Station Access": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (energy_req(350) in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Obscured Vestibule": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (wave in loadout) and
        (energy_req(350) in loadout) and
        (canBomb in loadout)
    ),
    "Docking Port 3": lambda loadout: (  # (3 = letter Gamma)
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout)
        )
    ),
    "Arena": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (
            (pinkDoor in loadout) or
            (
                (
                    (HiJump in loadout) or
                    (SpaceJump in loadout) or
                    ((Speedball in loadout) and (Morph in loadout))
                ) and
            (GravitySuit in loadout) or
                (
                    (HiJump in loadout) and
                    (
                        ((Speedball in loadout) and (Morph in loadout)) or
                        (Ice in loadout)
                        )
                    )
                )
            )
    ),
    "West Spore Field": lambda loadout: (
        (vulnar in loadout) and
        (Super in loadout) and
        (
            (canBomb in loadout) or
            (
                (Morph in loadout) and
                (Screw in loadout)
                )
            ) and
        (
            (GravitySuit in loadout) or
            (
                (SpaceJump in loadout) and
                (
                    (HiJump in loadout) or
                    (Speedball in loadout)
                    )
                )
            )
    ),
    "Magma Chamber": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        ((
            (Varia in loadout) and (Charge in loadout)
        ) or (
            (MetroidSuit in loadout) and
            (varia_or_hell_run(650) in loadout)
        ))
    ),
    "Equipment Locker": lambda loadout: (
        (WestCorridorR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((GravitySuit in loadout) or (HiJump in loadout) or (canBomb in loadout)) and
        ((MetroidSuit in loadout) or (Morph in loadout))
    ),
    "Antelier": lambda loadout: (  # spelled "Antilier" in subversion 1.1  
        (jumpAble in loadout) and
        (
            (
                (ConstructionSiteL in loadout) and
                (Morph in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout) and
                (Screw in loadout)
                ) or
            (
                (WestCorridorR in loadout) and
                (
                    ((pinkDoor in loadout) and (Morph in loadout)) or
                    ((MetroidSuit in loadout) and (Super in loadout))
                    ) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    ((Morph in loadout) and (Speedball in loadout))
                    )
                ) or
            (
                (FoyerR in loadout) and
                (canBomb in loadout) and
                (Screw in loadout)
                )
            )
    ),
    "Weapon Research": lambda loadout: (
        (jumpAble in loadout) and
        ((wave in loadout) or (MetroidSuit in loadout)) and
        ((canBomb in loadout) or ((Spazer in loadout) and (Morph in loadout))) and
        (
            (
                (ConstructionSiteL in loadout) and
                (Morph in loadout) and
                ((wave in loadout) or (Spazer in loadout)) and
                (Bombs in loadout)
                ) or
            (
                (WestCorridorR in loadout) and
                (Screw in loadout) and
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) or
                    (Ice in loadout) or
                    ((Morph in loadout) and (Speedball in loadout))
                    )
                ) or
            (
                (FoyerR in loadout) and
                (canBomb in loadout)
                )
            )
    ),
    "Crocomire's Lair": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
