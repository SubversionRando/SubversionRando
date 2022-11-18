from typing import ClassVar
from connection_data import area_doors_unpackable
from item_data import items_unpackable
from logicCommon import energy_req, varia_or_hell_run
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
canFly = LogicShortcut(lambda loadout: (
    (SpaceJump in loadout) or loadout.has_all(Morph, Bombs)
))
canUsePB = LogicShortcut(lambda loadout: (
    loadout.has_all(Morph, PowerBomb)
))
canBomb = LogicShortcut(lambda loadout: (
    (Morph in loadout) and loadout.has_any(Bombs, PowerBomb)
))
# TODO: I think there may be places where canBomb is used for bomb jumping
# even though it might only have PBs
jumpAble = LogicShortcut(lambda loadout: (
    loadout.has_all(exitSpacePort, GravityBoots)
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
    loadout.has_all(jumpAble, SpeedBooster, Grapple, Super, canUsePB, Wave, GravitySuit)
    # TODO: capital "Wave"? so hypercharge can't get into suzi?
))
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


area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            canFly in loadout
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            loadout.has_all(canFly, canUsePB)
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Missile in loadout) and
            (Morph in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(jumpAble, Missile, Morph, SpeedBooster, Energy)
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (Missile in loadout) and
            (Morph in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout))
            # TODO: Verify?
            # Casual can get through if they have supers and no missiles,
            # but expert needs missiles, they can't get through with just supers.
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            False
            # TODO: The old logic files didn't have any logic for going to SporeFieldTR
            # It only had logic coming from SporeFieldTR
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            False
            # TODO: The old logic files didn't have any logic for going to SporeFieldBR
            # It only had logic coming from SporeFieldBR
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (Energy in loadout)
            # TODO: expert can't do it without speedbooster, but casual can do it without speedbooster
        ),
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or ((GravitySuit in loadout) and (wave in loadout)))
        ),
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout)) and
            (canBomb in loadout)
            # TODO: verify - this difference between casual and expert doesn't look right
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and (wave in loadout) and (canBomb in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout)) and
            (canBomb in loadout)
            # TODO: verify - this difference between casual and expert doesn't look right
        ),
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Super in loadout) and
            ((GravitySuit in loadout) or (Speedball in loadout))
        ),
        ("OceanShoreR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple)
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (Super in loadout) and
            ((GravitySuit in loadout) or (Speedball in loadout))
            # TODO: expert needs super and casual doesn't?
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
                (canUsePB in loadout) or
                (Spazer in loadout)
            )
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (jumpAble in loadout) and (underwater in loadout) and (
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
            ((canUsePB in loadout) or (
                (underwater in loadout) and
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
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (((wave in loadout) and (Bombs in loadout)) or ((Screw in loadout) and (underwater in loadout)))
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
            ((
                (canUsePB in loadout) and
                (pinkDoor in loadout) and
                (underwater in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (underwater in loadout) and
                (Morph in loadout) and
                (Screw in loadout)
            ))
        ),
        ("WestCorridorR", "ConstructionSiteL"): lambda loadout: (
            (pinkDoor in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or (
                (underwater in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("WestCorridorR", "AlluringCenoteR"): lambda loadout: (
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
        ("FoyerR", "ExcavationSiteL"): lambda loadout: (
            (jumpAble in loadout) and (underwater in loadout) and (
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
                (Morph in loadout) and
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
            ((canUsePB in loadout) or (
                (underwater in loadout) and
                (pinkDoor in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (pinkDoor in loadout) and
            (jumpAble in loadout) and
            ((canUsePB in loadout) or (
                (underwater in loadout) and
                (Morph in loadout) and
                (Screw in loadout) and
                (wave in loadout) and
                (Bombs in loadout)
            ))
        ),
        ("ConstructionSiteL", "FoyerR"): lambda loadout: (
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
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (wave in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout) and
                (underwater in loadout)
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
            (canUsePB in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout)
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout)
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, DarkVisor, wave, canBomb)
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout)
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (DarkVisor in loadout) and
            (wave in loadout)
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, Super, canUsePB, DarkVisor, wave)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, Super, canUsePB, DarkVisor, wave)
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
            (canUsePB in loadout) and
            (wave in loadout)
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (wave in loadout)
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout))
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and (SpeedBooster in loadout)
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and (SpeedBooster in loadout)
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout) or
                (HiJump in loadout)
            )
        ),
        ("MezzanineConcourseL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout)
        ),
        ("VulnarCanyonL", "CanyonPassageR"): lambda loadout: (
            jumpAble in loadout
        ),
        ("VulnarCanyonL", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and
            (SpeedBooster in loadout)
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and (MetroidSuit in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and (MetroidSuit in loadout)
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (MetroidSuit in loadout)
        ),
        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
        ),
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout)) and
            (MetroidSuit in loadout)
        ),
    },
    "FireHive": {
        ("VulnarDepthsElevatorEL", "VulnarDepthsElevatorER"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("VulnarDepthsElevatorEL", "HiveBurrowL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("VulnarDepthsElevatorEL", "SequesteredInfernoL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, varia_or_hell_run(450), electricHyper)
        ),
        ("VulnarDepthsElevatorEL", "CollapsedPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, wave, canBomb, Super, varia_or_hell_run(750), electricHyper)
            # TODO: verify that electricHyper is needed here
            # (casual logic said hyper wasn't needed)
        ),
        ("VulnarDepthsElevatorER", "VulnarDepthsElevatorEL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("VulnarDepthsElevatorER", "HiveBurrowL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("VulnarDepthsElevatorER", "SequesteredInfernoL"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (energy_req(450) in loadout) and  # TODO: want to make expert require less energy than casual?
            (electricHyper in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (pinkDoor in loadout) and
            (canUsePB in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout) and  # TODO: want to make expert require less energy than casual?
            (electricHyper in loadout)
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorEL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorER"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("HiveBurrowL", "SequesteredInfernoL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("HiveBurrowL", "CollapsedPassageR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorEL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, canBomb, varia_or_hell_run(450), electricHyper)
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (energy_req(450) in loadout) and  # TODO: want to make expert require less energy than casual?
            (electricHyper in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, varia_or_hell_run(750), electricHyper)
            # TODO: verify these requirements
            # It said casual doesn't need PB and expert does need PB.
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorEL"): lambda loadout: (
            (varia_or_hell_run(750) in loadout) and
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout)
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (Super in loadout) and
            (energy_req(750) in loadout)  # TODO: want to make expert require less energy than casual?
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, varia_or_hell_run(750), electricHyper)
            # TODO: verify these requirements
            # It said casual doesn't need PB and expert does need PB.
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
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canUsePB in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ),
        ("MagmaPumpL", "ThermalReservoir1R"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ),
        ("MagmaPumpL", "GeneratorAccessTunnelL"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (plasmaWaveGate in loadout) and
            (varia_or_hell_run(350) in loadout) and
            (canUsePB in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
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
            (underwater in loadout) and
            ((MetroidSuit in loadout) or (
                (breakIce in loadout) and
                (Screw in loadout)
            ))
        ),
        ("ReservoirMaintenanceTunnelR", "ThermalReservoir1R"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, underwater, Screw, MetroidSuit, varia_or_hell_run(350))
        ),
        ("ReservoirMaintenanceTunnelR", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("IntakePumpR", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, varia_or_hell_run(350), canUsePB) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ),
        ("IntakePumpR", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (jumpAble in loadout) and
            (canUsePB in loadout) and
            (underwater in loadout) and
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
            (energy_req(350) in loadout)  # TODO: want to make expert require less energy than casual?
        ),
        ("IntakePumpR", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("ThermalReservoir1R", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, varia_or_hell_run(350), MetroidSuit, Screw)
        ),
        ("ThermalReservoir1R", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, underwater, Screw, MetroidSuit, varia_or_hell_run(350))
        ),
        ("ThermalReservoir1R", "IntakePumpR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit, varia_or_hell_run(350))
        ),
        ("ThermalReservoir1R", "GeneratorAccessTunnelL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
        ("GeneratorAccessTunnelL", "MagmaPumpL"): lambda loadout: (
            loadout.has_all(jumpAble, underwater, plasmaWaveGate, varia_or_hell_run(350), canUsePB, MetroidSuit, Screw)
        ),
        ("GeneratorAccessTunnelL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("GeneratorAccessTunnelL", "IntakePumpR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, underwater, Screw, MetroidSuit)
        ),
        ("GeneratorAccessTunnelL", "ThermalReservoir1R"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, MetroidSuit, varia_or_hell_run(350))
        ),
    },
    "DrayLand": {
        ("ElevatorToMagmaLakeR", "MagmaPumpAccessR"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (MetroidSuit in loadout) and
            (canUsePB in loadout)
        ),
        ("MagmaPumpAccessR", "ElevatorToMagmaLakeR"): lambda loadout: (
            (jumpAble in loadout) and
            (underwater in loadout) and
            (MetroidSuit in loadout) and
            (canUsePB in loadout)
        ),
    },
    "Verdite": {
        ("FieryGalleryL", "RagingPitL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, varia_or_hell_run(450), Super)
        ),
        ("FieryGalleryL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
            ((Ice in loadout) or (canUsePB in loadout))
        ),
        ("FieryGalleryL", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (underwater in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (Super in loadout) or (breakIce in loadout))
        ),
        ("RagingPitL", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (canBomb in loadout) and  # TODO: verify expert doesn't need PBs
            (Super in loadout)  # TODO: expert needs supers and casual doesn't?
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, varia_or_hell_run(450), icePod)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
            ((Ice in loadout) or (canUsePB in loadout))
        ),
        ("RagingPitL", "SporousNookL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, varia_or_hell_run(450), underwater)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (Morph in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
        ),
        ("HollowChamberR", "RagingPitL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, varia_or_hell_run(450), Super, icePod)
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(250) in loadout) and
            (Ice in loadout)  # TODO: verify expert doesn't need any missile damage
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Ice in loadout) and
            (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
            (underwater in loadout)
        ),
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
            ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
            ((Ice in loadout) or (canUsePB in loadout))
        ),
        ("PlacidPoolR", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (Super in loadout) and
            ((icePod in loadout) or (canUsePB in loadout))
        ),
        ("PlacidPoolR", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, varia_or_hell_run(250), icePod)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            ((Ice in loadout) or (canUsePB in loadout)) and
            (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
            (underwater in loadout)
        ),
        ("SporousNookL", "FieryGalleryL"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (underwater in loadout) and
            ((canBomb in loadout) or (Screw in loadout) or (Super in loadout) or (breakIce in loadout))
        ),
        ("SporousNookL", "RagingPitL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (underwater in loadout)
        ),
        ("SporousNookL", "HollowChamberR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout) and
            (Super in loadout) and
            (underwater in loadout)
        ),
        ("SporousNookL", "PlacidPoolR"): lambda loadout: (
            (jumpAble in loadout) and
            (varia_or_hell_run(450) in loadout) and
            ((icePod in loadout) or (canUsePB in loadout)) and
            (Super in loadout) and
            (underwater in loadout)
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
        (Missile in loadout) and
        ((Morph in loadout) or (GravitySuit in loadout))
    ),
    "Submarine Nest": lambda loadout: (
        (OceanShoreR in loadout) and (pinkDoor in loadout) and (underwater in loadout)
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (GravitySuit in loadout) and
        ((canUsePB in loadout) or (
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ))
    ),
    "Benthic Cache Access": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (underwater in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Benthic Cache": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (underwater in loadout) and
        (canBomb in loadout) and
        (Super in loadout)
    ),
    "Ocean Vent Supply Depot": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (pinkDoor in loadout) and
        (underwater in loadout) and
        (Morph in loadout) and
        ((Super in loadout) or (
            (GravitySuit in loadout) and
            (Screw in loadout)
        ))
    ),
    "Sediment Flow": lambda loadout: (
        (OceanShoreR in loadout) and (jumpAble in loadout) and (underwater in loadout) and (Super in loadout)
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        (FieldAccessL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canBomb in loadout)
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (vulnar in loadout) and (canUsePB in loadout) and (Screw in loadout) and (MetroidSuit in loadout)
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
        ((pinkDoor in loadout) or (
            (GravitySuit in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Speedball in loadout))
        ) or (
            (HiJump in loadout) and
            (Speedball in loadout) or  # TODO: are these parentheses in the right place? (and mixed with or)
            (Ice in loadout)
        )) and
        ((Wave in loadout) or (Bombs in loadout))
    ),
    "Archives: SpringBall": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout)
    ),
    "Archives: SJBoost": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout) and (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: ETank": lambda loadout: (  # front
        (vulnar in loadout) and (Morph in loadout)
    ),
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
        ((GravitySuit in loadout) or (Speedball in loadout) or (
            (HiJump in loadout) and
            (Ice in loadout)
        ))
    ),
    "Epiphreatic Crag": lambda loadout: (
        (ConstructionSiteL in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        ((
            (Speedball in loadout) and
            (HiJump in loadout)
        ) or (GravitySuit in loadout))
    ),
    "Mezzanine Concourse": lambda loadout: (
        (MezzanineConcourseL in loadout) and (jumpAble in loadout) and (WestTerminalAccessL in loadout)
    ),
    "Greater Inferno": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Super in loadout) and
        (varia_or_hell_run(850) in loadout) and
        (MetroidSuit in loadout)
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
        (
            (EleToTurbidPassageR in loadout) and
            (varia_or_hell_run(550) in loadout)
        ) or (
            (SporousNookL in loadout) and
            ((GravitySuit in loadout) or (Speedball in loadout) or (
                (HiJump in loadout) and
                (Ice in loadout)
            )) and
            (jumpAble in loadout) and
            (Super in loadout) and
            (canBomb in loadout)
        )
    ),
    "Infested Passage": lambda loadout: (
        (jumpAble in loadout) and
        (varia_or_hell_run(450) in loadout) and
        (
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout)
        ) or (  # TODO: missing parentheses around this or?
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (Morph in loadout) and
            (icePod in loadout)
        )
    ),
    "Fire's Boon Shrine": lambda loadout: (
        (
            (VulnarDepthsElevatorEL in loadout) and
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(450) in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(350) in loadout)
        ) or (
            (CollapsedPassageR in loadout) and  # TODO: is PB needed here?
            (Super in loadout) and
            (varia_or_hell_run(750) in loadout) and
            (canBomb in loadout) and
            (wave in loadout)
        )
    ),
    "Fire's Bane Shrine": lambda loadout: (
        (icePod in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(750) in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (varia_or_hell_run(750) in loadout)
        ))
    ),
    "Ancient Shaft": lambda loadout: (
        (jumpAble in loadout) and
        (canUsePB in loadout) and  # TODO: expert needs PB and casual doesn't?
        ((varia_or_hell_run(650) in loadout) or (MetroidSuit in loadout)) and
        (
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout)
        )
    ),
    "Gymnasium": lambda loadout: (
        (jumpAble in loadout) and
        (varia_or_hell_run(650) in loadout) and
        (Grapple in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (Morph in loadout)
        ))
    ),
    "Electromechanical Engine": lambda loadout: (
        (jumpAble in loadout) and
        (Grapple in loadout) and
        (varia_or_hell_run(350) in loadout) and
        (Morph in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (canBomb in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout)) and
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
        (
            (FoyerR in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ) or  # TODO: verify parentheses in the right place (mixed and and or)
        (
            (AlluringCenoteR in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (canUsePB in loadout)
        )
    ),
    "Briar: SJBoost": lambda loadout: (  # top
        (NorakBrookL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),
    "Shrine Of Fervor": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout)
    ),
    "Chamber Of Wind": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((canBomb in loadout) or (
            (Screw in loadout) and
            (Speedball in loadout) and
            (Morph in loadout)
        ) and (SpeedBooster in loadout))
    ),
    "Water Garden": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (SpeedBooster in loadout)
    ),
    "Crocomire's Energy Station": lambda loadout: (
        (NorakBrookL in loadout) and
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
        (WestTerminalAccessL in loadout) and (jumpAble in loadout)
    ),
    "Summit Landing": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (canBomb in loadout)
    ),
    "Snow Cache": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (canBomb in loadout)
    ),
    "Reliquary Access": lambda loadout: (
        (WestTerminalAccessL in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (DarkVisor in loadout)
    ),
    "Syzygy Observatorium": lambda loadout: (
        (WestTerminalAccessL in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (MetroidSuit in loadout) and
            (energy_req(350) in loadout)
        ) or (
            (Hypercharge in loadout) and
            (Charge in loadout)
        ))
    ),
    "Armory Cache 2": lambda loadout: (
        (WestTerminalAccessL in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ))
    ),
    "Armory Cache 3": lambda loadout: (
        (WestTerminalAccessL in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ))
    ),
    "Drawing Room": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (Super in loadout)
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
        (canFly in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout)
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
            loadout.has_all(spaceDrop, LoadingDockSecurityAreaL, jumpAble, MetroidSuit, Grapple, Super)
        )
    ),
    "Torpedo Bay": lambda loadout: (
        True
    ),
    "Extract Storage": lambda loadout: (
        (
            (canUsePB in loadout) and
            (spaceDrop not in loadout)
        ) or (
            loadout.has_all(spaceDrop, LoadingDockSecurityAreaL, jumpAble, Grapple, MetroidSuit)
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
        (
            (OceanShoreR in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            ((
                (DarkVisor in loadout) and
                (pinkDoor in loadout)
            ) or (Super in loadout))
        ) or (
            (EleToTurbidPassageR in loadout) and
            (Super in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            (Speedball in loadout)
        )
    ),
    "Sediment Floor": lambda loadout: (
        (
            (OceanShoreR in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            ((
                (DarkVisor in loadout) and
                (pinkDoor in loadout)
            ) or (Super in loadout))
        ) or (
            (EleToTurbidPassageR in loadout) and
            (pinkDoor in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            (Speedball in loadout)
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
        (vulnar in loadout) and ((canBomb in loadout) or ((Morph in loadout) and (Screw in loadout)))
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
        (canBomb in loadout)
    ),
    "Causeway Overlook": lambda loadout: (
        (CausewayR in loadout) and (jumpAble in loadout) and (canBomb in loadout)
    ),
    "Placid Pool": lambda loadout: (
        (PlacidPoolR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (icePod in loadout)
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
        ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout)) and
        (DarkVisor in loadout)  # Shouldn't an expert be able to do this without visor?
    ),
    "Ancient Basin": lambda loadout: (
        (varia_or_hell_run(750) in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (pinkDoor in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (Morph in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (wave in loadout)
        ))
    ),
    "Central Corridor: right": lambda loadout: (
        (FoyerR in loadout) and
        (jumpAble in loadout) and
        ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout)) and
        (canBomb in loadout)
    ),
    "Briar: AmmoTank": lambda loadout: (  # bottom
        (NorakBrookL in loadout) and (jumpAble in loadout) and (Morph in loadout)
    ),
    "Icy Flow": lambda loadout: (
        (WestTerminalAccessL in loadout) and
        (jumpAble in loadout) and
        (SpeedBooster in loadout) and
        (breakIce in loadout)
    ),
    "Ice Cave": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (breakIce in loadout)
    ),
    "Antechamber": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),
    "Eddy Channels": lambda loadout: (
        (EleToTurbidPassageR in loadout) and
        (underwater in loadout) and
        (Morph in loadout) and
        (Speedball in loadout) and
        (Super in loadout)
    ),
    "Tram To Suzi Island": lambda loadout: (
        (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (Spazer in loadout) and (Morph in loadout)
    ),
    "Portico": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (energy_req(350) in loadout)
    ),
    "Tower Rock Lookout": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (energy_req(350) in loadout) and
        (GravitySuit in loadout) and
        ((
            (SpaceJump in loadout) and
            (HiJump in loadout)
        ) or (
            (canFly in loadout)
        ))
    ),
    "Reef Nook": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (energy_req(350) in loadout) and
        (GravitySuit in loadout) and
        ((
            (SpaceJump in loadout) and
            (HiJump in loadout)
        ) or (
            (canFly in loadout)
        ))
    ),
    "Saline Cache": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (energy_req(350) in loadout) and
        (GravitySuit in loadout) and
        (canFly in loadout)
    ),
    "Enervation Chamber": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (suzi in loadout) and
        (canFly in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout)
    ),
    "Weapon Locker": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (pinkDoor in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Grapple in loadout) and
            (pinkDoor in loadout)
        )
    ),
    "Aft Battery": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (Morph in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (MetroidSuit in loadout) and
            (Grapple in loadout) and
            (Morph in loadout)
        )
    ),
    "Forward Battery": lambda loadout: (
        (
            (spaceDrop not in loadout) and
            (pinkDoor in loadout) and
            (Morph in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (jumpAble in loadout) and
            (Grapple in loadout) and
            (MetroidSuit in loadout) and
            (pinkDoor in loadout)
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
            (pinkDoor in loadout)
        )
    ),
    "Garden Canal": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Spazer in loadout)
    ),
    "Sandy Burrow: AmmoTank": lambda loadout: (  # bottom
        (OceanShoreR in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            ((Speedball in loadout) or (Ice in loadout))
        )) and
        (Morph in loadout)
    ),
    "Trophobiotic Chamber": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout)
    ),
    "Waste Processing": lambda loadout: (
        (SpeedBooster in loadout) and
        (jumpAble in loadout) and
        ((
            (SubbasementFissureL in loadout) and
            (canUsePB in loadout)
        ) or (
            (CellarR in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout)
        ) or (
            (FieldAccessL in loadout) and  # expert required to access from this door
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
        (canBomb in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((
            (EleToTurbidPassageR in loadout) and
            (varia_or_hell_run(550) in loadout)
        ) or (
            (SporousNookL in loadout) and
            ((GravitySuit in loadout) or (Speedball in loadout) or (
                (HiJump in loadout) and
                (Ice in loadout)
            ))
        ))
    ),
    "Colosseum": lambda loadout: (  # GT
        (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (Varia in loadout) and (Charge in loadout)
    ),
    "Lava Pool": lambda loadout: (  # BATH ENERGY COUNT??
        loadout.has_all(EleToTurbidPassageR, jumpAble, Varia, MetroidSuit, canBomb)
    ),
    "Hive Main Chamber": lambda loadout: (
        (VulnarDepthsElevatorEL in loadout) and
        (jumpAble in loadout) and
        (varia_or_hell_run(650) in loadout) and
        (canBomb in loadout)
    ),
    "Crossway Cache": lambda loadout: (
        (
            (VulnarDepthsElevatorEL in loadout) and
            (jumpAble in loadout) and
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
            (canUsePB in loadout) and
            (wave in loadout)
        )
    ),
    "Slag Heap": lambda loadout: (  # Sequestered Inferno w Metroid Suit is simplest  Possibly a no-Metroid version?
        (canBomb in loadout) and
        (jumpAble in loadout) and
        (varia_or_hell_run(950) in loadout) and
        (MetroidSuit in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            ((Ice in loadout) or ((Hypercharge in loadout) and (Charge in loadout)))
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout)  # TODO: expert needs hyper and casual doesn't?
        ) or (
            (CollapsedPassageR in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (wave in loadout)
        ))
    ),
    "Hydrodynamic Chamber": lambda loadout: (  # one of the only intended water rooms
        (WestCorridorR in loadout) and
        ((GravitySuit in loadout) or (HiJump in loadout)) and
        (Morph in loadout) and
        (pinkDoor in loadout) and
        (Spazer in loadout)
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
        (FoyerR in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout)
    ),
    "Foundry": lambda loadout: (
        (FoyerR in loadout) and (jumpAble in loadout)
    ),
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        ((canFly in loadout) or (SpeedBooster in loadout))
    ),
    "Glacier's Reach": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (energy_req(350) in loadout)
    ),
    "Sitting Room": lambda loadout: (
        (WestTerminalAccessL in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (Speedball in loadout)
    ),
    "Suzi Ruins Map Station Access": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (energy_req(350) in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Obscured Vestibule": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
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
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout)
    ),
    "West Spore Field": lambda loadout: (
        (vulnar in loadout) and
        ((canBomb in loadout) or (
            (Morph in loadout) and
            (Screw in loadout)
        )) and
        (Super in loadout) and
        (Speedball in loadout)  # possible with space jump and no speedball
    ),
    "Magma Chamber": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        ((
            (Varia in loadout) and (Charge in loadout)
        ) or (
            (MetroidSuit in loadout) and
            (energy_req(650) in loadout)
            # REVIEW: the same energy required whether you have varia or not?
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
        (
            (WestCorridorR in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout)) and
            ((
                (pinkDoor in loadout) and
                (Morph in loadout)
            ) or (Super in loadout))
        ) or (
            (FoyerR in loadout) and
            (underwater in loadout) and
            (Screw in loadout)
        )
    ),
    "Weapon Research": lambda loadout: (
        (FoyerR in loadout) and
        (jumpAble in loadout) and
        ((wave in loadout) or (MetroidSuit in loadout)) and
        ((canBomb in loadout) or (Spazer in loadout))
    ),
    "Crocomire's Lair": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic
