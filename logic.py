import enum
from typing import Callable

from connection_data import area_doors_unpackable
from item_data import items_unpackable
from loadout import Loadout, LogicShortcut

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


class LogicLevel(enum.IntEnum):
    CASUAL = 0
    EXPERT = 2


Expert = LogicShortcut(lambda loadout: (
    loadout.logic_level >= LogicLevel.EXPERT
))
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
underwater = LogicShortcut(lambda loadout: (
    (jumpAble in loadout) and (
        (GravitySuit in loadout) or (loadout.has_all(HiJump, Expert))
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


ENERGY_PER_TANK = 100
STARTING_ENERGY = 99


# TODO: test hell run logic (I don't know if it needs a functools partial)
def varia_or_hell_run(energy_for_expert: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (Varia in loadout) or (
            (Expert in loadout) and (loadout.count(Energy) * ENERGY_PER_TANK + STARTING_ENERGY > energy_for_expert)
        )
    ))


area_logic: dict[str, dict[tuple[str, str], Callable[[Loadout], bool]]] = {
    "Early": {
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CraterR", "RuinedConcourseBL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CraterR", "RuinedConcourseTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CraterR", "CausewayR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CraterR", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CraterR", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseBL", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or ((GravitySuit in loadout) and (wave in loadout)))
        ),
        ("RuinedConcourseBL", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseBL", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseTR", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("RuinedConcourseTR", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("RuinedConcourseTR", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CausewayR", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or ((GravitySuit in loadout) and (wave in loadout)))
        ),
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("CausewayR", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("CausewayR", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldTR", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (vulnar in loadout) and
            ((SpeedBooster in loadout) or
             (Speedball in loadout) or
             ((GravitySuit in loadout) and (wave in loadout))) and
            (canBomb in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldBR", "CraterR"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            True  # TODO: verify no requirements here
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and (wave in loadout) and (canBomb in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and (canBomb in loadout) and (SpeedBooster in loadout) and (Energy in loadout)
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            (vulnar in loadout) and (
                (SpeedBooster in loadout) or
                (Speedball in loadout) or
                ((GravitySuit in loadout) and (wave in loadout))
            ) and (canBomb in loadout) and (wave in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            True  # TODO: verify no requirements here
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
            loadout.has_all(jumpAble, Morph, underwater, Speedball, DarkVisor, pinkDoor) and
            ((wave in loadout) or
             (SpeedBooster in loadout) or
             (Screw in loadout) or
             ((Super in loadout) and ((Speedball in loadout) or (canUsePB in loadout))))
        ),
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, DarkVisor, SpeedBooster, Speedball)
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, SpeedBooster, Grapple, DarkVisor)
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, GravitySuit, canUsePB, Super, Grapple, DarkVisor, SpeedBooster, Speedball)
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
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout) and
                (underwater in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canUsePB in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout)
            ))
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (SpeedBooster in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canUsePB in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout)
            ))
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, pinkDoor, DarkVisor, wave, canBomb)
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout) and
                (underwater in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canUsePB in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout)
            ))
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (SpeedBooster in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canUsePB in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout)
            ))
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(jumpAble, Super, canUsePB, DarkVisor, wave)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            loadout.has_all(jumpAble, Super, canUsePB, DarkVisor, wave)
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout) and
                (underwater in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (SpeedBooster in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout)
            ))
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
            ((DarkVisor in loadout) or (Expert in loadout))
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (jumpAble in loadout) and
            (Super in loadout) and
            (canUsePB in loadout) and
            (wave in loadout) and
            ((DarkVisor in loadout) or (Expert in loadout))
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canUsePB in loadout) and
                (DarkVisor in loadout) and
                (underwater in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Super in loadout) and
                (canBomb in loadout) and
                (DarkVisor in loadout)
            ))
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                ((canFly in loadout) or (SpeedBooster in loadout) or (Ice in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout))
            ))
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and (SpeedBooster in loadout)
            ))
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and (SpeedBooster in loadout)
            ))
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (jumpAble in loadout) and (
                (canFly in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout) or
                ((Expert in loadout) and (HiJump in loadout))
            )
        ),
        ("MezzanineConcourseL", "VulnarCanyonL"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (SpeedBooster in loadout)
            ))
        ),
        ("MezzanineConcourseL", "CanyonPassageR"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (SpeedBooster in loadout)
            ))
        ),
        ("MezzanineConcourseL", "ElevatorToCondenserL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (SpeedBooster in loadout)
            ))
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (SpeedBooster in loadout)
            ))
        ),
        ("VulnarCanyonL", "CanyonPassageR"): lambda loadout: (
            jumpAble in loadout
        ),
        ("VulnarCanyonL", "ElevatorToCondenserL"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and
                (SpeedBooster in loadout)
            ))
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (SpeedBooster in loadout) and
                ((canBomb in loadout) or (Screw in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (SpeedBooster in loadout)
            ))
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (jumpAble in loadout) and (SpeedBooster in loadout)
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (jumpAble in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (VulnarCanyonL in loadout) or (
                (Expert in loadout) and (
                    (jumpAble in loadout) and
                    (canBomb in loadout) and
                    (breakIce in loadout) and
                    (underwater in loadout) and
                    ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and
                    (SpeedBooster in loadout)
                )
            )
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (
                (WestTerminalAccessL in loadout) and
                (jumpAble in loadout) and
                ((canBomb in loadout) or (Screw in loadout)) and
                (SpeedBooster in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (breakIce in loadout) and
                (underwater in loadout) and
                ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout))
            ))
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Morph in loadout)) and
                (GravitySuit in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
            ))
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout)) and
                (MetroidSuit in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and
                (MetroidSuit in loadout)
            ))
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Morph in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
            ))
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout)) and
                (GravitySuit in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
            ))
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (jumpAble in loadout) and (MetroidSuit in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (jumpAble in loadout) and
            ((canBomb in loadout) or (Screw in loadout))
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout) or (Morph in loadout)) and
                (GravitySuit in loadout) and
                (MetroidSuit in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and
                (MetroidSuit in loadout)
            ))
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
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((HiJump in loadout) or (SpaceJump in loadout)) and
                (GravitySuit in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                ((canFly in loadout) or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout))
            ))
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
            (loadout.count(Energy) > 4) and  # TODO: no way to avoid this energy requirement?
            (electricHyper in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (pinkDoor in loadout) and
            (canUsePB in loadout) and
            (Super in loadout) and
            (loadout.count(Energy) > 7) and  # TODO: no way to avoid this energy requirement?
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
            (loadout.count(Energy) > 4) and  # TODO: no way to avoid this energy requirement?
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
            (
                (wave in loadout) and
                (canBomb in loadout)
            ) or ((Expert in loadout) and (
                (canUsePB in loadout)
            ))
            # TODO: expert needs PBs and casual doesn't?
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (jumpAble in loadout) and (canUsePB in loadout) and (Super in loadout) and (loadout.count(Energy) > 7)
            # TODO: no way to avoid this energy requirement?
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
            (loadout.count(Energy) > 3)  # TODO: no way to avoid this energy requirement?
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
            (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (MetroidSuit in loadout) and
                (Varia in loadout) and
                (canUsePB in loadout) and
                ((Screw in loadout) or (
                    (Hypercharge in loadout) and
                    (Charge in loadout)
                ))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (MetroidSuit in loadout) and
                (canUsePB in loadout)
            ))
        ),
        ("MagmaPumpAccessR", "ElevatorToMagmaLakeR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (MetroidSuit in loadout) and
                (Varia in loadout) and
                (canUsePB in loadout) and
                ((Screw in loadout) or (
                    (Hypercharge in loadout) and
                    (Charge in loadout)
                ))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (underwater in loadout) and
                (MetroidSuit in loadout) and
                (canUsePB in loadout)
            ))
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
            ((Expert in loadout) or (icePod in loadout)) and
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
            (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (canUsePB in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (canBomb in loadout) and  # TODO: verify expert doesn't need PBs
                (Super in loadout))  # TODO: expert needs supers and casual doesn't?
            )
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, Super, varia_or_hell_run(450), icePod)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (canUsePB in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (canBomb in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
                ((Ice in loadout) or (canUsePB in loadout))
            ))
        ),
        ("RagingPitL", "SporousNookL"): lambda loadout: (
            loadout.has_all(jumpAble, canUsePB, varia_or_hell_run(450), underwater)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (Morph in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (pinkDoor in loadout) and
                (icePod in loadout) and  # TODO: verify expert doesn't need ice
                ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (Morph in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
                ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout))
            ))
        ),
        ("HollowChamberR", "RagingPitL"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, varia_or_hell_run(450), Super, icePod)
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (varia_or_hell_run(250) in loadout) and
                (icePod in loadout)
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (varia_or_hell_run(250) in loadout) and
                (Ice in loadout)  # TODO: verify expert doesn't need any missile damage
            ))
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (icePod in loadout) and
                (underwater in loadout) and
                ((canBomb in loadout) or (Screw in loadout) or (Super in loadout) or (breakIce in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (Ice in loadout) and
                (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
                (underwater in loadout)
            ))
        ),
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (pinkDoor in loadout) and
                ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
                ((icePod in loadout) or (canUsePB in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
                ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and
                ((Ice in loadout) or (canUsePB in loadout))
            ))
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
            (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                ((icePod in loadout) or (canUsePB in loadout)) and
                (pinkDoor in loadout) and
                (underwater in loadout) and
                ((canBomb in loadout) or (Screw in loadout) or (Super in loadout) or (breakIce in loadout))
            ) or ((Expert in loadout) and (
                (jumpAble in loadout) and
                (varia_or_hell_run(450) in loadout) and
                ((Ice in loadout) or (canUsePB in loadout)) and
                (Super in loadout) and  # TODO: expert needs supers and casual doesn't?
                (underwater in loadout)
            ))
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
            (underwater in loadout) and
            ((Expert in loadout) or (Super in loadout))
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
