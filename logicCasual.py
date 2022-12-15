from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicCommon import ammo_req, can_bomb, canBomb, canUsePB, energy_req, varia_or_hell_run
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
))
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
    (jumpAble in loadout) and (GravitySuit in loadout)
))
icePod = LogicShortcut(lambda loadout: (
    ((Ice in loadout) and (missileDamage in loadout)) or ((Charge in loadout) and (Hypercharge in loadout))
))
suzi = LogicShortcut(lambda loadout: (
    loadout.has_all(jumpAble, canFly, SpeedBooster, Super, wave, canUsePB, GravitySuit)
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

waterGardenBottom = LogicShortcut(lambda loadout: (
    (GravitySuit in loadout) and
    (can_bomb(1) in loadout) and
    ((Speedball in loadout) or (Bombs in loadout))  # 4-tile morph jump
))
""" get into water garden from wellspring access - little morph tunnel with bomb blocks after water """

brook = LogicShortcut(lambda loadout: (
    (jumpAble in loadout) and
    (Morph in loadout) and
    ((GravitySuit in loadout) or (
        (SpaceJump in loadout) and
        (HiJump in loadout)
    ))
))
""" to get across Norak Brook (bottom right to left) """

veranda = LogicShortcut(lambda loadout: (
    loadout.has_any(Morph, HiJump, SpaceJump)
    # If you don't have HiJump or SpaceJump or Bombs,
    # you can wall jump off of the wall right above the door to Hopper Nest,
    # then wall jump off the ledge just outside the door to Jungle Map Station access,
    # to get to the middle level, then use the Morph tunnel in the top right to get up higher.

    # If you have HiJump and no Morph, then you wall jump off the green wall above the
    # door to Jungle Map Station Access, or the bricks across from it.

    # Some might think these techs are too advanced for casual,
    # but I think the combination being very unlikely to be required and not extremely difficult
    # (not nearly as hard as much of the stuff in expert) makes it ok.
))
""" to get from the bottom of Veranda to the top """

# TODO: put this in more of the places that reference FoyerR
eastCorridor = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (
        (Bombs in loadout) or (  # 4 tile morph jump
            (Speedball in loadout) and
            ((PowerBomb in loadout) or (wave in loadout))
            # PB or wave for getting the shot block at the top of east corridor
        )
    )
))
""" top of East Corridor to get to Foyer """

railAccess = LogicShortcut(lambda loadout: (
    (jumpAble in loadout) and
    (
        (WestTerminalAccessL in loadout) or
        (
            (MezzanineConcourseL in loadout) and
            ((canFly in loadout) or
             (SpeedBooster in loadout) or
             (Ice in loadout))
            ) or
        (
            (ElevatorToCondenserL in loadout) and
            (canBomb in loadout) and
            (breakIce in loadout) and
            (underwater in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (Grapple in loadout))
            )
        )        
))
""" access to the Sky Temple elevators at West Terminal and Transit Concourse """


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
            (Missile in loadout) and
            (canBomb in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(vulnar, canBomb, SpeedBooster, energy_req(180))
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or (
                (GravitySuit in loadout) and
                (wave in loadout)
            ))
            # TODO: Verify?
            # Casual can get through if they have supers and no missiles,
            # but expert needs missiles, they can't get through with just supers.
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            (vulnar in loadout) and
            ((canBomb in loadout) or
             ((Morph in loadout) and
              (Speedball in loadout)))
            # TODO: The old logic files didn't have any logic for going to SporeFieldTR
            # It only had logic coming from SporeFieldTR
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            (vulnar in loadout) and
            (wave in loadout) and
            ((canBomb in loadout) or
             ((Morph in loadout) and
              (Speedball in loadout)))
            # TODO: The old logic files didn't have any logic for going to SporeFieldBR
            # It only had logic coming from SporeFieldBR
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
            (canBomb in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or (
                (GravitySuit in loadout) and
                (wave in loadout)
            ))
            # TODO: expert can't do it without speedbooster, but casual can do it without speedbooster
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
            (Energy in loadout)
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
            (canBomb in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (vulnar in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout) and
            (DarkVisor in loadout)
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or (
                (GravitySuit in loadout) and
                (wave in loadout)
            )) and
            (canBomb in loadout)
            # TODO: this difference between casual and expert doesn't look right
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            True  # TODO: put requirements here. Don't assume that we start with Sunken Nest
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout) and
            (canBomb in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            (jumpAble in loadout) and
            (canBomb in loadout) and
            (SpeedBooster in loadout) and
            (energy_req(180) in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (jumpAble in loadout) and
            (wave in loadout) and
            (DarkVisor in loadout)
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            ((SpeedBooster in loadout) or (Speedball in loadout) or (
                (GravitySuit in loadout) and
                (wave in loadout)
            )) and
            (canBomb in loadout) and
            (wave in loadout)
            # TODO: this difference between casual and expert doesn't look right
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
            ) or
             (Screw in loadout)
            )
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
            (jumpAble in loadout) and (
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
            (electricHyper in loadout)
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
            (electricHyper in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            False  # One way Hive Burrow not in logic
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            loadout.has_all(jumpAble, canBomb, Super, Varia, electricHyper)
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
            loadout.has_all(jumpAble, canBomb, pinkDoor, Varia, electricHyper)
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

norakToLifeTemple = LogicShortcut(lambda loadout: (
    (
        (NorakBrookL in loadout) and
        (brook in loadout)
    ) or (
        (NorakPerimeterBL in loadout) and
        (Morph in loadout) and
        ((canBomb in loadout) or (Screw in loadout))
    ) or (
        (NorakPerimeterTR in loadout) and
        (MetroidSuit in loadout)
    )
))
""" from any of the Norak area doors to Life Temple """

location_logic: LocationLogicType = {
    "Impact Crater: AccelCharge": lambda loadout: (
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
        (OceanShoreR in loadout) and
        (pinkDoor in loadout) and
        (jumpAble in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            (Ice in loadout)
        ))
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (GravitySuit in loadout) and
        # if I don't have dark visor,
        # I need 3 pbs to safely be able to get in and then out with PBs
        # probably only 2, but blocks might respawn to require 3 if too slow
        ((
            (can_bomb(1) in loadout) and
            (DarkVisor in loadout)
        ) or (
            (can_bomb(3) in loadout)
        ))
    ),
    "Benthic Cache Access": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (underwater in loadout) and
        (canUsePB in loadout) and
        (Super in loadout) and
        (DarkVisor in loadout)
    ),
    "Benthic Cache": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (underwater in loadout) and
        (canBomb in loadout) and
        (Super in loadout) and
        (DarkVisor in loadout)
    ),
    "Ocean Vent Supply Depot": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (pinkDoor in loadout) and
        (underwater in loadout) and
        (Morph in loadout) and
        (DarkVisor in loadout) and
        ((Super in loadout) or (
            (GravitySuit in loadout) and
            (Screw in loadout)
        ))
    ),
    "Sediment Flow": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (underwater in loadout) and
        (Super in loadout)
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        (FieldAccessL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canBomb in loadout) and
        (wave in loadout) and
        (DarkVisor in loadout)
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (vulnar in loadout) and
        (canUsePB in loadout) and
        (Screw in loadout) and
        (MetroidSuit in loadout)
    ),
    "Grand Vault": lambda loadout: (
        (vulnar in loadout) and
        (Grapple in loadout)
    ),
    "Cistern": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout)
    ),
    "Warrior Shrine: ETank": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canUsePB in loadout)
    ),
    "Vulnar Caves Entrance": lambda loadout: (
        (vulnar in loadout)
    ),
    "Crypt": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and  # TODO: if using power bombs, I need 30 ammo to get in and out
        (
            (pinkDoor in loadout) or (
                (GravitySuit in loadout) and
                (
                    (HiJump in loadout) or
                    (SpaceJump in loadout) or
                    (Bombs in loadout)
                )
            )
        ) and (
            (wave in loadout) or
            (Bombs in loadout)
        )
    ),
    "Archives: SpringBall": lambda loadout: (
        (vulnar in loadout) and
        (Morph in loadout) and
        (Speedball in loadout)
    ),
    "Archives: SJBoost": lambda loadout: (
        (vulnar in loadout) and
        (Morph in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: ETank": lambda loadout: (  # front
        # TODO: check area door, don't assume start location
        (vulnar in loadout) and
        (canBomb in loadout) and
        (Speedball in loadout) and
        (LargeAmmo in loadout) and
        (SmallAmmo in loadout)
    ),
    "Eribium Apparatus Room": lambda loadout: (
        (
            (FieldAccessL in loadout) and
            (jumpAble in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (wave in loadout) and
            (DarkVisor in loadout)
        ) or (
            loadout.has_all(TransferStationR, DarkVisor, jumpAble, canBomb)
        )
    ),
    "Hot Spring": lambda loadout: (
        (SporousNookL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        ((GravitySuit in loadout) or (
            loadout.has_all(HiJump, Ice, Speedball)
        ))
    ),
    "Epiphreatic Crag": lambda loadout: (
        (ConstructionSiteL in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (GravitySuit in loadout)
    ),
    "Mezzanine Concourse": lambda loadout: (
        (MezzanineConcourseL in loadout) and
        (jumpAble in loadout) and
        (
            (canFly in loadout) or
            (SpeedBooster in loadout) or
            (Ice in loadout)
        )
        # TODO: 4-tile morph jump to get out
    ),
    "Greater Inferno": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Super in loadout) and
        (GravitySuit in loadout) and
        (Varia in loadout) and
        (MetroidSuit in loadout) and
        (
            (wave in loadout) or
            (plasmaWaveGate in loadout)
        )
    ),
    "Burning Depths Cache": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (GravitySuit in loadout) and
        (Varia in loadout) and
        (MetroidSuit in loadout) and
        (Spazer in loadout)
    ),
    "Mining Cache": lambda loadout: (
        (
            (
                (EleToTurbidPassageR in loadout) and
                (Varia in loadout)
            ) or (
                (SporousNookL in loadout) and
                (GravitySuit in loadout)
            )
        ) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (canBomb in loadout)
    ),
    "Infested Passage": lambda loadout: (
        (jumpAble in loadout) and
        (Varia in loadout) and
        (
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout)
        ) or (
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
            (Varia in loadout) and
            (icePod in loadout) and
            (wave in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (Varia in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (Super in loadout) and
            (Varia in loadout) and
            (canBomb in loadout)
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
            (Varia in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout) and
            (pinkDoor in loadout) and
            (Varia in loadout)
        ))
    ),
    "Ancient Shaft": lambda loadout: (
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (Varia in loadout) and
        (MetroidSuit in loadout) and
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
        (Varia in loadout) and
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
        (Varia in loadout) and
        (Morph in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (canBomb in loadout) and
            (GravitySuit in loadout) and
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
            (GravitySuit in loadout) and
            (Screw in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (Varia in loadout) and
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
            (canBomb in loadout) and
            (Speedball in loadout) and
            (
                (MetroidSuit in loadout) or
                (Screw in loadout)
            )
        ) or
        (
            (AlluringCenoteR in loadout) and
            (Grapple in loadout) and
            (SpeedBooster in loadout) and
            (Speedball in loadout) and
            (canUsePB in loadout)
        )
    ),
    "Briar: SJBoost": lambda loadout: (  # PB tube
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout)
    ),
    "Shrine Of Fervor": lambda loadout: (
        (jumpAble in loadout) and
        (veranda in loadout) and
        (norakToLifeTemple in loadout)
    ),
    "Chamber Of Wind": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canFly in loadout) and
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
        (jumpAble in loadout) and
        (SpeedBooster in loadout) and
        (veranda in loadout) and
        (norakToLifeTemple in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Crocomire's Energy Station": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (  # to get past the bomb blocks in the left side of Croc's room
            (
                (Morph in loadout) and
                (Speedball in loadout)
            ) or (canBomb in loadout) or (Screw in loadout)
        ) and
        (veranda in loadout) and
        (norakToLifeTemple in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Wellspring Cache": lambda loadout: (
        (ElevatorToWellspringL in loadout) and
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        (Super in loadout) and
        (Morph in loadout)
    ),
    "Frozen Lake Wall: DamageAmp": lambda loadout: (
        (ElevatorToCondenserL in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout)
    ),
    "Grand Promenade": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout)
    ),
    "Summit Landing": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (Speedball in loadout)
    ),
    "Snow Cache": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (varia_or_hell_run(350) in loadout)
    ),
    "Reliquary Access": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (DarkVisor in loadout) and
        ((Speedball in loadout) or (
            (Bombs in loadout) and
            (Morph in loadout)
        ))
    ),
    "Syzygy Observatorium": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (MetroidSuit in loadout) and
            (energy_req(650) in loadout)
        ) or (
            (Super in loadout) and
            (Hypercharge in loadout) and
            (Charge in loadout) and
            (energy_req(350) in loadout)
        ))
    ),
    "Armory Cache 2": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            ((Speedball in loadout) or (
                (Bombs in loadout) and
                (Morph in loadout)
            ))
        ))
    ),
    "Armory Cache 3": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        ((Screw in loadout) or (
            (Super in loadout) and
            (canBomb in loadout) and
            (DarkVisor in loadout) and
            ((Speedball in loadout) or (
                (Bombs in loadout) and
                (Morph in loadout)
            ))
        ))
    ),
    "Drawing Room": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (Super in loadout)
    ),
    "Impact Crater Overlook": lambda loadout: (  # TODO: check an area door, don't assume we start in this area
        (canFly in loadout) and
        (canBomb in loadout) and
        ((canUsePB in loadout) or  # TODO: if all I have is PB, I need 20 ammo
         (Super in loadout))
    ),
    "Magma Lake Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (icePod in loadout) and
        (Morph in loadout)
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
        # TODO: ((energy or (suits for defense)) and ammo) or metroid suit for hyper beam kill
        (canUsePB in loadout) and
        (
            (spaceDrop not in loadout) or (
                loadout.has_all(spaceDrop, LoadingDockSecurityAreaL, jumpAble, Grapple, MetroidSuit)
            )
        )
    ),
    "Impact Crater Alcove": lambda loadout: (  # TODO: check an area door, don't assume we start in this area
        (jumpAble in loadout) and
        (canFly in loadout) and
        (canBomb in loadout)
    ),
    "Ocean Shore: bottom": lambda loadout: (
        OceanShoreR in loadout
    ),
    "Ocean Shore: top": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (
            (canFly in loadout) or
            (HiJump in loadout) or
            ((SpeedBooster in loadout) and (GravitySuit in loadout))
        )
    ),
    "Sandy Burrow: ETank": lambda loadout: (  # top
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        ((Screw in loadout) or (canBomb in loadout)) and
        ((HiJump in loadout) or (SpaceJump in loadout))
    ),
    "Submarine Alcove": lambda loadout: (
        (jumpAble in loadout) and
        (DarkVisor in loadout) and
        (
            (OceanShoreR in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            (pinkDoor in loadout)
        ) or (
            (EleToTurbidPassageR in loadout) and
            (Super in loadout) and
            (underwater in loadout) and
            (Morph in loadout) and
            (Speedball in loadout)
        )
    ),
    "Sediment Floor": lambda loadout: (
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        (Morph in loadout) and
        (
            (OceanShoreR in loadout) and
            ((
                (DarkVisor in loadout) and
                (pinkDoor in loadout)
            ) or (Super in loadout))
        ) or (
            (EleToTurbidPassageR in loadout) and
            (Super in loadout) and
            (Speedball in loadout)
        )
    ),
    "Sandy Gully": lambda loadout: (
        (OceanShoreR in loadout) and
        (jumpAble in loadout) and
        (GravitySuit in loadout) and
        (Super in loadout)
    ),
    "Hall Of The Elders": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        ((
            (GravitySuit in loadout) and
            ((HiJump in loadout) or (canFly in loadout))
        ) or (pinkDoor in loadout))
    ),
    "Warrior Shrine: AmmoTank bottom": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (Morph in loadout) and
        (pinkDoor in loadout)
    ),
    "Warrior Shrine: AmmoTank top": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (pinkDoor in loadout) and
        (Speedball in loadout)
    ),
    "Path Of Swords": lambda loadout: (
        (vulnar in loadout) and
        ((canBomb in loadout) or
         ((Morph in loadout) and
          (Screw in loadout)))
    ),
    "Auxiliary Pump Room": lambda loadout: (
        (vulnar in loadout) and (canBomb in loadout)
    ),
    "Monitoring Station": lambda loadout: (  # TODO: check an area door, don't assume that we start by vulnar
        (vulnar in loadout) and
        (Morph in loadout) and
        ((Speedball in loadout) or (canBomb in loadout))
    ),
    "Sensor Maintenance: AmmoTank": lambda loadout: (  # back
        (vulnar in loadout) and
        (canBomb in loadout) and
        (Speedball in loadout) and
        (ammo_req(25) in loadout)
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
        (GravitySuit in loadout)
    ),
    "Blazing Chasm": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (GravitySuit in loadout) and
        (Varia in loadout) and
        (MetroidSuit in loadout)
    ),
    "Generator Manifold": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (canBomb in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (GravitySuit in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (canUsePB in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (Varia in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout)
        ))
    ),
    "Fiery Crossing Cache": lambda loadout: (
        (RagingPitL in loadout) and
        (jumpAble in loadout) and
        (Varia in loadout) and
        (canUsePB in loadout)
    ),
    "Dark Crevice Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout)) and
        (DarkVisor in loadout)
    ),
    "Ancient Basin": lambda loadout: (
        (Varia in loadout) and
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
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            (Ice in loadout)
        )) and
        (canBomb in loadout) and
        (eastCorridor in loadout)
    ),
    "Briar: AmmoTank": lambda loadout: (  # bottom
        (jumpAble in loadout) and
        (Morph in loadout) and
        (norakToLifeTemple in loadout)
    ),
    "Icy Flow": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (SpeedBooster in loadout) and
        (breakIce in loadout)
    ),
    "Ice Cave": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (breakIce in loadout)
    ),
    "Antechamber": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout)
    ),
    "Eddy Channels": lambda loadout: (
        (EleToTurbidPassageR in loadout) and
        (GravitySuit in loadout) and
        (DarkVisor in loadout) and
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
        (Super in loadout) and
        (energy_req(650) in loadout)
    ),
    "Tower Rock Lookout": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (energy_req(650) in loadout) and
        (GravitySuit in loadout) and
        (SpaceJump in loadout) and
        (HiJump in loadout)
    ),
    "Reef Nook": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (energy_req(650) in loadout) and
        (GravitySuit in loadout) and
        (SpaceJump in loadout) and
        (HiJump in loadout)
    ),
    "Saline Cache": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (Super in loadout) and
        (energy_req(650) in loadout) and
        (GravitySuit in loadout) and
        (canFly in loadout)
    ),
    "Enervation Chamber": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (suzi in loadout) and
        (energy_req(650) in loadout) and
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
        (NorakPerimeterBL in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Spazer in loadout) and
        (veranda in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Sandy Burrow: AmmoTank": lambda loadout: (  # bottom
        (OceanShoreR in loadout) and
        (GravitySuit in loadout) and
        (Morph in loadout) and
        # to get back in hole after getting this item
        (loadout.has_any(Speedball, Bombs, PowerBomb)) and
        ((HiJump in loadout) or (canFly in loadout))
    ),
    "Trophobiotic Chamber": lambda loadout: (
        (vulnar in loadout) and
        (Morph in loadout) and
        (Speedball in loadout)
    ),
    "Waste Processing": lambda loadout: (
        (SpeedBooster in loadout) and
        (jumpAble in loadout) and
        (
            (
                (SubbasementFissureL in loadout) and
                (canUsePB in loadout)
            ) or
            (
                (CellarR in loadout) and
                (pinkDoor in loadout) and
                (canBomb in loadout) and
                (underwater in loadout) and
                (DarkVisor in loadout)
            ) or
            (
                (TransferStationR in loadout) and
                (DarkVisor in loadout) and
                (wave in loadout) and
                (canBomb in loadout)
            )
        )
    ),
    "Grand Chasm": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (Screw in loadout)
    ),
    "Mining Site 1": lambda loadout: (  # (1 = letter Alpha)
        (canBomb in loadout) and
        ((Speedball in loadout) or (Bombs in loadout)) and  # short morph jump
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        ((
            (EleToTurbidPassageR in loadout) and
            (Varia in loadout)
        ) or (
            (SporousNookL in loadout) and
            (GravitySuit in loadout)
        ))
    ),
    "Colosseum": lambda loadout: (  # GT
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (Varia in loadout) and
        (Charge in loadout)
    ),
    "Lava Pool": lambda loadout: (  # No bath count in casual
        loadout.has_all(EleToTurbidPassageR, jumpAble, Varia, MetroidSuit, canBomb)
    ),
    "Hive Main Chamber": lambda loadout: (
        (VulnarDepthsElevatorEL in loadout) and
        (jumpAble in loadout) and
        (Varia in loadout) and
        (canBomb in loadout)
    ),
    "Crossway Cache": lambda loadout: (
        (jumpAble in loadout) and
        (Varia in loadout) and
        (
            (VulnarDepthsElevatorEL in loadout) and
            (canBomb in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (electricHyper in loadout)
        ) or (
            (CollapsedPassageR in loadout) and
            (pinkDoor in loadout) and
            (canBomb in loadout) and
            (wave in loadout)
        )
    ),
    "Slag Heap": lambda loadout: (  # No Metroid-less lava baths in casual
        (canBomb in loadout) and
        (jumpAble in loadout) and
        (Varia in loadout) and
        (MetroidSuit in loadout) and
        (SequesteredInfernoL in loadout)
    ),
    "Hydrodynamic Chamber": lambda loadout: (  # one of the only intended water rooms
        (Morph in loadout) and
        (Spazer in loadout) and
        (
            (WestCorridorR in loadout) and
            ((
                (pinkDoor in loadout) and
                ((GravitySuit in loadout) or (
                    (HiJump in loadout) and
                    (Ice in loadout)
                ))
            ) or (
                (Super in loadout) and
                ((GravitySuit in loadout) or (HiJump in loadout))
            ))
        ) or (
            (FoyerR in loadout) and
            (eastCorridor in loadout) and
            (Screw in loadout)
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
        (FoyerR in loadout) and
        (jumpAble in loadout) and
        (MetroidSuit in loadout) and
        (canBomb in loadout) and
        (Speedball in loadout)
    ),
    "Foundry": lambda loadout: (
        (FoyerR in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (Speedball in loadout) and
        (energy_req(250) in loadout)  # Worth testing
    ),
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and
        (jumpAble in loadout) and
        (canFly in loadout)
    ),
    "Glacier's Reach": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (varia_or_hell_run(650) in loadout)
    ),
    "Sitting Room": lambda loadout: (
        (railAccess in loadout) and
        (jumpAble in loadout) and
        (canUsePB in loadout) and
        (Speedball in loadout)
        # TODO: this is missing exit logic - what do you need to get mack to rail?
        # (at least supers or missiles or screw)
        # TODO: energy_req or varia
    ),
    "Suzi Ruins Map Station Access": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (energy_req(650) in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Obscured Vestibule": lambda loadout: (
        (TramToSuziIslandR in loadout) and
        (jumpAble in loadout) and
        (energy_req(650) in loadout) and
        (canBomb in loadout)
    ),
    "Docking Port 3": lambda loadout: (  # (3 = letter Gamma)
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (MetroidSuit in loadout)
        )
    ),
    "Arena": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (jumpAble in loadout) and
        (canBomb in loadout) and
        (
            (pinkDoor in loadout) or (
                (GravitySuit in loadout) and
                (
                    (HiJump in loadout) or
                    (SpaceJump in loadout) or
                    (Bombs in loadout)
                )
            )
        )
    ),
    "West Spore Field": lambda loadout: (
        (vulnar in loadout) and
        ((canBomb in loadout) or (
            (Morph in loadout) and
            (Screw in loadout)
        )) and
        (Super in loadout) and
        (Speedball in loadout) and
        (GravitySuit in loadout)
    ),
    "Magma Chamber": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (jumpAble in loadout) and
        (pinkDoor in loadout) and
        (canUsePB in loadout) and
        (Varia in loadout) and
        ((Charge in loadout) or (MetroidSuit in loadout))
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
            (
                (GravitySuit in loadout) or (
                    (HiJump in loadout) and
                    (Ice in loadout)  # freeze pancake to stand on
                )
            ) and
            ((
                (pinkDoor in loadout) and
                (Morph in loadout)
            ) or (
                (Super in loadout) and
                (
                    (Morph in loadout) or
                    (MetroidSuit in loadout)
                )
            ))
        ) or (
            (FoyerR in loadout) and
            (eastCorridor in loadout) and
            (Screw in loadout) and
            (
                (GravitySuit in loadout) or (
                    # gravity jump through hydrodynamic chamber door into main hydrology research from central corridor
                    (HiJump in loadout) and
                    (Ice in loadout)  # freeze pancake to stand on
                )
            )
        )
    ),
    "Weapon Research": lambda loadout: (
        # TODO: review this location logic
        (jumpAble in loadout) and
        (Speedball in loadout) and
        (Morph in loadout) and
        ((wave in loadout) or (MetroidSuit in loadout)) and
        (
            (FoyerR in loadout) and
            (canBomb in loadout)
        ) or
        (
            (WestCorridorR in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout)) and
            (pinkDoor in loadout) and
            (Spazer in loadout)
        )
    ),
    "Crocomire's Lair": lambda loadout: (
        (jumpAble in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (veranda in loadout) and
        (norakToLifeTemple in loadout)
    ),
}


class Casual(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return loadout.has_any(Morph, Missile, wave, Super)
