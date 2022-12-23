from typing import Callable

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import Item, items_unpackable
from loadout import Loadout
from logicCommon import can_bomb, can_use_pbs, varia_or_hell_run, canUsePB
from logic_shortcut import LogicShortcut
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

canFly = LogicShortcut(lambda loadout: (
    (GravityBoots in loadout) and ((SpaceJump in loadout) or loadout.has_all(Morph, Bombs))
))
shootThroughWalls = LogicShortcut(lambda loadout: (
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
pinkSwitch = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))

electricHyper = LogicShortcut(lambda loadout: (
    (MetroidSuit in loadout) or (
        (Charge in loadout) and
        (Hypercharge in loadout)
    )
))
""" hyper beam when electricity is available """

location_logic: dict[str, Callable[[Loadout], bool]] = {
    "Impact Crater: AccelCharge": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (Spazer in loadout) and
        ((HiJump in loadout) or (SpeedBooster in loadout) or (canFly in loadout))
    ),
    "Subterranean Burrow": lambda loadout: (
        (SunkenNestL in loadout) and
        ((Morph in loadout) or (GravityBoots in loadout))
    ),
    "Sandy Cache": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        ((
            # top path
            (pinkDoor in loadout)  # Ocean Shallows left
        ) or (
            # bottom path (no pink door needed)
            (Morph in loadout) and
            ((GravitySuit in loadout) or (HiJump in loadout) or (Tricks.sbj_underwater_no_hjb in loadout))
            # TODO: confirm springball jump can get you back through bottom path
        ))
    ),
    "Submarine Nest": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (
                    (Ice in loadout) or
                    (Tricks.crouch_precise in loadout)
                )
            ) or
            (Tricks.sbj_underwater_no_hjb in loadout)
        )
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (missileDamage in loadout) and  # eye door
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))
        ((GravitySuit in loadout) or (Tricks.sbj_underwater_w_hjb in loadout)) and
        ((
            (can_bomb(1) in loadout) and
            (DarkVisor in loadout)
        ) or (
            (can_use_pbs(2) in loadout)
        ))
    ),
    "Benthic Cache Access": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (GravityBoots in loadout) and
        # if you don't have bombs, you'll need 3 pbs
        (can_bomb(3) in loadout) and
        # and even if you do have bombs, you'll need 1 pb
        (can_use_pbs(1) in loadout) and
        (Super in loadout) and  # submarine crevice bottom left - and some pink doors
        ((GravitySuit in loadout) or (
            (Tricks.sbj_underwater_w_hjb in loadout) and
            # out of benthic shaft without aqua before the balls block you in
            (Tricks.movement_moderate in loadout)
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ),
    "Benthic Cache": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and  # submarine crevice, in and out with nowhere to farm between
        (Super in loadout) and  # submarine crevice bottom left - and some pink doors
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            # out of benthic shaft without aqua before the balls block you in
            (Tricks.movement_moderate in loadout) and
            # submarine crevice
            ((Tricks.crouch_precise in loadout) or (Tricks.sbj_underwater_w_hjb) or (Tricks.uwu_2_tile in loadout))
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ),
    "Ocean Vent Supply Depot": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (GravityBoots in loadout) and
        (Morph in loadout) and  # inside the room with the item
        (pinkDoor in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            ((Super in loadout) or (  # don't need these tricks if I can go through sediment floor
                (Tricks.crouch_or_downgrab in loadout) and  # up from murky gallery
                (Tricks.movement_moderate in loadout) and  # left from murky gallery
                (Tricks.uwu_2_tile in loadout)  # up from submarine crevice
            ))
            # hint: snail will help you up meandering passage
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout)) and
        ((Super in loadout) or ((GravitySuit in loadout) and (Screw in loadout)))  # TODO: or PBs and a laval dive
        # if you don't have gravity and screw, there's a 3-tile morph jump that might require speedball or some skill
        # not making a trick for it because it's not very hard underwater if you unequip high jump boots
    ),
    "Sediment Flow": lambda loadout: (
        loadout.has_all(OceanShoreR, GravityBoots, GravitySuit, Super)
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        ((
            (FieldAccessL in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ) or (
            (TransferStationR in loadout) and
            (DarkVisor in loadout) and
            (pinkDoor in loadout)  # between east spore field and ESF access
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_easy)) and
        (can_bomb(1) in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        # 5-tile morph jump
        (pinkDoor in loadout)  # between spore collection and spore generator access
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # impact crater bottom right
        (missileDamage in loadout) and  # missile barrier
        # if you don't have (grapple or can fly), you can get up on the right wall with screw
        (Screw in loadout) and
        (can_use_pbs(2) in loadout) and  # if 20 ammo, you'll need to get drops from red balls
        (MetroidSuit in loadout)
    ),
    "Grand Vault": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # impact crater bottom right
        (missileDamage in loadout) and  # missile barrier
        (Grapple in loadout)
    ),
    "Cistern": lambda loadout: (
        (RuinedConcourseBL in loadout) and (GravityBoots in loadout) and (can_bomb(1) in loadout)
    ),
    "Warrior Shrine: ETank": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (GravityBoots in loadout) and
        (pinkSwitch in loadout) and  # TODO: logic for other paths if doors change colors (beneath missile barriers)
        (pinkDoor in loadout) and  # to warrior shrine access
        (can_use_pbs(1) in loadout) and  # PB placement is important if you only have 10 ammo
        ((Speedball in loadout) or (Tricks.mockball_hard in loadout))
    ),
    "Vulnar Caves Entrance": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # impact crater bottom right
        (missileDamage in loadout)  # missile barrier
    ),
    "Crypt": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(3) in loadout) and
        (
            (pinkDoor in loadout) or (
                (
                    (GravitySuit in loadout) and
                    (
                        (HiJump in loadout) or (canFly in loadout)
                    )
                ) or (
                    (HiJump in loadout) and
                    (Ice in loadout) and  # freeze fish
                    ((Tricks.movement_moderate in loadout) or (SpaceJump in loadout))
                    # tight wall jump from lower chozo statue to higher chozo statue
                ) or (
                    (Tricks.sbj_underwater_w_hjb) and  # TODO: verify this
                    ((Tricks.movement_moderate in loadout) or (SpaceJump in loadout))
                )
                # TODO: more tricks for coming through cistern without aqua suit?
            )
        ) and
        (
            (shootThroughWalls in loadout) or
            (Bombs in loadout) or
            (
                (Speedball in loadout) and  # follow your bullet with speedball to hit the switch
                (Tricks.movement_moderate in loadout)
            )
        )
    ),
    "Archives: SpringBall": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # a few
        (missileDamage in loadout) and  # missile barriers
        (Morph in loadout) and
        (Speedball in loadout)
    ),
    "Archives: SJBoost": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # a few
        (missileDamage in loadout) and  # missile barrier
        (Morph in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: ETank": lambda loadout: (
            # Casual: ( (vulnar in loadout) and (canBomb in loadout) and (Speedball in loadout) and (LargeAmmo in loadout) and (SmallAmmo in loadout) ))
            # Expert: (vulnar in loadout) and (Morph in loadout) and ( (Super in loadout) or (canUsePB in loadout) )))
    ),  # front  front  TODO: check area door, don't assume start location
    "Eribium Apparatus Room": lambda loadout: (
            # Casual: ((FieldAccessL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (canBomb in loadout) and (wave in loadout) and (DarkVisor in loadout) ) or ( loadout.has_all(TransferStationR ))
            # Expert: (FieldAccessL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (canBomb in loadout)))
    ),
    "Hot Spring": lambda loadout: (
            # Casual: (SporousNookL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and ((GravitySuit in loadout) or ( loadout.has_all(HiJump )))
            # Expert: (SporousNookL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (hotSpring in loadout)))
    ),  # TODO: verify you can get this item and get out with  hi-jump, ice, morph, pb, gravity boots  (with the 2 tile morph jump?) Does it need?  ((Speedball in loadout) or (GravitySuit in loadout))
    "Epiphreatic Crag": lambda loadout: (
            # Casual: (ConstructionSiteL in loadout) and (jumpAble in loadout) and (Morph in loadout) and (GravitySuit in loadout))
            # Expert: (ConstructionSiteL in loadout) and (jumpAble in loadout) and (Morph in loadout) and ( (GravitySuit in loadout) or ( (Screw in loadout) and ( (canBomb in loadout) or (Speedball in loadout) ) ) or ( (Speedball in loadout) and (HiJump in loadout) ) )))
    ),
    "Mezzanine Concourse": lambda loadout: (
            # Casual: (MezzanineConcourseL in loadout) and (jumpAble in loadout) and ( (canFly in loadout) or (SpeedBooster in loadout) or (Ice in loadout) ))
            # Expert: (MezzanineConcourseL in loadout) and (jumpAble in loadout) and (Morph in loadout) and ( (canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout) or (Speedball in loadout) )))
    ),  # TODO: 4-tile morph jump to get out
    "Greater Inferno": lambda loadout: (
            # Casual: (MagmaPumpAccessR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (Super in loadout) and (GravitySuit in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and ( (wave in loadout) or (plasmaWaveGate in loadout) ))
            # Expert: (MagmaPumpAccessR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (Super in loadout) and (varia_or_hell_run(850) in loadout) and (MetroidSuit in loadout) and ( (GravitySuit in loadout) or (Speedball in loadout) )))
    ),
    "Burning Depths Cache": lambda loadout: (
            # Casual: (MagmaPumpAccessR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (GravitySuit in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and (Spazer in loadout))
            # Expert: (MagmaPumpAccessR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (varia_or_hell_run(550) in loadout) and (MetroidSuit in loadout) and ((Spazer in loadout) or (Wave in loadout) or ( (Charge in loadout) and (Bombs in loadout) ))))
    ),
    "Mining Cache": lambda loadout: (
            # Casual: (( (EleToTurbidPassageR in loadout) and (Varia in loadout) ) or ( (SporousNookL in loadout) and (GravitySuit in loadout) ) ) and (jumpAble in loadout) and (Super in loadout) and (canBomb in loadout))
            # Expert: (jumpAble in loadout) and (Super in loadout) and (canBomb in loadout) and ( (EleToTurbidPassageR in loadout) and (varia_or_hell_run(550) in loadout) ) or ( (SporousNookL in loadout) and (hotSpring in loadout) )))
    ),
    "Infested Passage": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Varia in loadout) and ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (Morph in loadout) and (icePod in loadout) ))
            # Expert: (jumpAble in loadout) and ( ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (varia_or_hell_run(450) in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (Morph in loadout) and (icePod in loadout) and (varia_or_hell_run(250) in loadout) ) )))
    ),
    "Fire's Boon Shrine": lambda loadout: (
            # Casual: ((VulnarDepthsElevatorEL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and (Varia in loadout) and (icePod in loadout) and (wave in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (pinkDoor in loadout) and (Varia in loadout) ) or ( (CollapsedPassageR in loadout) and (Super in loadout) and (Varia in loadout) and (canBomb in loadout) ))
            # Expert: (jumpAble in loadout) and (pinkDoor in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (varia_or_hell_run(450) in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (varia_or_hell_run(350) in loadout) and (Morph in loadout) ) or ( (CollapsedPassageR in loadout) and (varia_or_hell_run(750) in loadout) and (canBomb in loadout) and (wave in loadout) ))))
    ),
    "Fire's Bane Shrine": lambda loadout: (
            # Casual: (icePod in loadout) and (jumpAble in loadout) and (Morph in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and (Varia in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (pinkDoor in loadout) and (Varia in loadout) )))
            # Expert: (icePod in loadout) and (jumpAble in loadout) and (Morph in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and (varia_or_hell_run(450) in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (pinkDoor in loadout) and (varia_or_hell_run(350) in loadout) ))))
    ),  # TODO: include path from CollapsedPassageR?
    "Ancient Shaft": lambda loadout: (
            # Casual: (jumpAble in loadout) and (canBomb in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) ))
            # Expert: (jumpAble in loadout) and (canBomb in loadout) and (varia_or_hell_run(650) in loadout) and ( (MetroidSuit in loadout) or (energy_req(1250) in loadout) or ( (Varia in loadout) and (energy_req(650) in loadout) ) ) and ( ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) ) )))
    ),
    "Gymnasium": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Varia in loadout) and (Grapple in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (Morph in loadout) )))
            # Expert: (jumpAble in loadout) and (Grapple in loadout) and ( ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) and (varia_or_hell_run(450) in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (Morph in loadout) and (varia_or_hell_run(250) in loadout) ) )))
    ),
    "Electromechanical Engine": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Grapple in loadout) and (Varia in loadout) and (Morph in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and (canBomb in loadout) and (GravitySuit in loadout) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (MetroidSuit in loadout) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) )))
            # Expert: (jumpAble in loadout) and (Grapple in loadout) and (varia_or_hell_run(350) in loadout) and (canBomb in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) ) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (MetroidSuit in loadout) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) ))))
    ),
    "Depressurization Valve": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Morph in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and (canBomb in loadout) and (GravitySuit in loadout) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (Varia in loadout) and (MetroidSuit in loadout) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) )))
            # Expert: (jumpAble in loadout) and (Morph in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and (canBomb in loadout) and ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout)) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (varia_or_hell_run(350) in loadout) and (MetroidSuit in loadout) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) ))))
    ),
    "Loading Dock Storage Area": lambda loadout: (
        (LoadingDockSecurityAreaL in loadout )
    ),
    "Containment Area": lambda loadout: (
            # Casual: (jumpAble in loadout) and ( (FoyerR in loadout) and (canBomb in loadout) and (Speedball in loadout) and ( (MetroidSuit in loadout) or (Screw in loadout) ) ) or ( (AlluringCenoteR in loadout) and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and (canUsePB in loadout) ))
            # Expert: (jumpAble in loadout) and (( (FoyerR in loadout) and (canBomb in loadout) and ((MetroidSuit in loadout) or (Screw in loadout)) ) or ( (AlluringCenoteR in loadout) and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and (canUsePB in loadout) ))))
    ),
    "Briar: SJBoost": lambda loadout: (
        (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),  # top  PB tube
    "Shrine Of Fervor": lambda loadout: (
            # Casual: (jumpAble in loadout) and (veranda in loadout) and (norakToLifeTemple in loadout))
            # Expert: (jumpAble in loadout) and ( ( (NorakBrookL in loadout) and (Morph in loadout) and ((GravitySuit in loadout) or (Ice in loadout) or (HiJump in loadout) or (Speedball in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (SpeedBooster in loadout)) ) or ( (NorakPerimeterTR in loadout) and (MetroidSuit in loadout) ) or ( (NorakPerimeterBL in loadout) and ((canBomb in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) ) )))
    ),
    "Chamber Of Wind": lambda loadout: (
            # Casual: (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (canFly in loadout) and (SpeedBooster in loadout) and ( (canBomb in loadout) or ( (Screw in loadout) and (Speedball in loadout) and (Morph in loadout) ) ))
            # Expert: (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (SpeedBooster in loadout) and ( (canBomb in loadout) or ( (Screw in loadout) and (Speedball in loadout) and (Morph in loadout) ) )))
    ),
    "Water Garden": lambda loadout: (
            # Casual: (jumpAble in loadout) and (SpeedBooster in loadout) and (veranda in loadout) and (norakToLifeTemple in loadout))
            # Expert: (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (SpeedBooster in loadout)))
    ),  # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    "Crocomire's Energy Station": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Super in loadout) and (SpeedBooster in loadout) and ( ( (Morph in loadout) and (Speedball in loadout) ) or (canBomb in loadout) or (Screw in loadout) ) and (veranda in loadout) and (norakToLifeTemple in loadout))
            # Expert: (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (Super in loadout) and (SpeedBooster in loadout)))
    ),  # to get past the bomb blocks in the left side of Croc's room  TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    "Wellspring Cache": lambda loadout: (
            # Casual: (ElevatorToWellspringL in loadout) and (jumpAble in loadout) and (GravitySuit in loadout) and (Super in loadout) and (Morph in loadout))
            # Expert: (ElevatorToWellspringL in loadout) and (jumpAble in loadout) and loadout.has_any(HiJump (Super in loadout) and (Morph in loadout)))
    ),
    "Frozen Lake Wall: DamageAmp": lambda loadout: (
        (ElevatorToCondenserL in loadout) and (jumpAble in loadout) and (canUsePB in loadout)
    ),
    "Grand Promenade": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout))
            # Expert: (jumpAble in loadout) and (railAccess in loadout)))
    ),
    "Summit Landing": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (Speedball in loadout))
            # Expert: (jumpAble in loadout) and (canBomb in loadout) and (railAccess in loadout)))
    ),
    "Snow Cache": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (varia_or_hell_run(350) in loadout))
            # Expert: (jumpAble in loadout) and (canBomb in loadout) and (railAccess in loadout)))
    ),
    "Reliquary Access": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (Super in loadout) and (DarkVisor in loadout) and ((Speedball in loadout) or ( (Bombs in loadout) and (Morph in loadout) )))
            # Expert: (jumpAble in loadout) and (Super in loadout) and (DarkVisor in loadout) and (railAccess in loadout)))
    ),
    "Syzygy Observatorium": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (( (Screw in loadout) and (Morph in loadout) and (varia_or_hell_run(150) in loadout) ) or ( (Super in loadout) and (MetroidSuit in loadout) and (Varia in loadout) and (energy_req(650) in loadout) ) or ( (Super in loadout) and (Hypercharge in loadout) and (Charge in loadout) and   (varia_or_hell_run(550) in loadout) and (energy_req(350) in loadout) )))
            # Expert: (jumpAble in loadout) and    ((Screw in loadout) or ( (Super in loadout) and (MetroidSuit in loadout) and    (energy_req(350) in loadout) ) or ( (Super in loadout) and (Hypercharge in loadout) and (Charge in loadout) )) and (railAccess in loadout)))
    ),  # TODO: verify you can get in and out with no varia and no e-tank  TODO: Can you get in and out with just grav boots and screw? (no morph)  I see how to get in with no morph, but not how to get out.  TODO: Metroid suit kills you a lot faster if you don't have varia.  Are you sure you can do it with only 350?  (varia_or_hell_run(1050) in loadout) and  can get in without morph, but can't get out  You lose health way too fast with metroid and no varia.  350 with varia, 550 without varia  TODO: Should these numbers depend on damage amp and accel charge?
    "Armory Cache 2": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and ((meetingHall in loadout) or ( (Super in loadout) and (canBomb in loadout) and (DarkVisor in loadout) and ((Speedball in loadout) or ( (Bombs in loadout) and (Morph in loadout) )) )))
            # Expert: (jumpAble in loadout) and ((meetingHall in loadout) or ( (Super in loadout) and (canBomb in loadout) and (DarkVisor in loadout) )) and (railAccess in loadout)))
    ),
    "Armory Cache 3": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and ((meetingHall in loadout) or ( (Super in loadout) and (canBomb in loadout) and (DarkVisor in loadout) and ((Speedball in loadout) or ( (Bombs in loadout) and (Morph in loadout) )) )))
            # Expert: (jumpAble in loadout) and ((meetingHall in loadout) or ( (Super in loadout) and (canBomb in loadout) and (DarkVisor in loadout) )) and (railAccess in loadout)))
    ),
    "Drawing Room": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (Super in loadout))
            # Expert: (jumpAble in loadout) and (Super in loadout) and (railAccess in loadout)))
    ),
    "Impact Crater Overlook": lambda loadout: (
            # Casual: (canFly in loadout) and (canBomb in loadout) and ((canUsePB in loadout) or (Super in loadout)))
            # Expert: ((canFly in loadout) or (SpeedBooster in loadout)) and (canBomb in loadout) and ((canUsePB in loadout) or (Super in loadout))))
    ),  # TODO: check an area door, don't assume we start in this area  TODO: check an area door, don't assume we start in this area  TODO: if all I have is PB, I need 20 ammo
    "Magma Lake Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (icePod in loadout) and (Morph in loadout)
    ),
    "Shrine Of The Animate Spark": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (suzi in loadout) and (canFly in loadout) and (Hypercharge in loadout) and (Charge in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (suzi in loadout) and (Hypercharge in loadout) and (Charge in loadout) and (energy_req(350) in loadout)))
    ),
    "Docking Port 4": lambda loadout: (
        ((spaceDrop not in loadout) and (Grapple in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) )
    ),  # (4 = letter Omega)  (4 = letter Omega)
    "Ready Room": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (Super in loadout) ) or ( loadout.has_all(spaceDrop ))
            # Expert: ((spaceDrop not in loadout) and (Super in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Super in loadout) and ( (Grapple in loadout) or (Xray in loadout) or (Ice in loadout) ) )))
    ),
    "Torpedo Bay": lambda loadout: (
        (True )
    ),
    "Extract Storage": lambda loadout: (
            # Casual: ( (canUsePB in loadout) and ( (spaceDrop not in loadout) or ( loadout.has_all(spaceDrop ) ) ))
            # Expert: ((canUsePB in loadout) and (spaceDrop not in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and ( (Grapple in loadout) or ( (Super in loadout) and ( (Xray in loadout) or (Ice in loadout) ) ) ) )))
    ),  # TODO: ((energy or (suits for defense)) and ammo) or metroid suit for hyper beam kill
    "Impact Crater Alcove": lambda loadout: (
            # Casual: (jumpAble in loadout) and (canFly in loadout) and (canBomb in loadout))
            # Expert: (jumpAble in loadout) and ((canFly in loadout) or (SpeedBooster in loadout)) and (canBomb in loadout)))
    ),  # TODO: check an area door, don't assume we start in this area  TODO: check an area door, don't assume we start in this area
    "Ocean Shore: bottom": lambda loadout: (
        (OceanShoreR in loadout)
    ),
    "Ocean Shore: top": lambda loadout: (
            # Casual: (OceanShoreR in loadout) and (jumpAble in loadout) and ( (canFly in loadout) or (HiJump in loadout) or ((SpeedBooster in loadout) and (GravitySuit in loadout)) ))
            # Expert: (OceanShoreR in loadout) and (jumpAble in loadout)))
    ),
    "Sandy Burrow: ETank": lambda loadout: (
            # Casual: (OceanShoreR in loadout) and (jumpAble in loadout) and (GravitySuit in loadout) and ((Screw in loadout) or (canBomb in loadout)) and ((HiJump in loadout) or (SpaceJump in loadout)))
            # Expert: (OceanShoreR in loadout) and (underwater in loadout) and (( (GravitySuit in loadout) and ((Screw in loadout) or (canBomb in loadout)) ) or ( ((Speedball in loadout) or (HiJump in loadout)) and (canBomb in loadout) ))))
    ),  # top  top
    "Submarine Alcove": lambda loadout: (
            # Casual: (jumpAble in loadout) and (DarkVisor in loadout) and ( (OceanShoreR in loadout) and (underwater in loadout) and (Morph in loadout) and (pinkDoor in loadout) ) or ( (EleToTurbidPassageR in loadout) and (Super in loadout) and (underwater in loadout) and (Morph in loadout) and (Speedball in loadout) ))
            # Expert: (jumpAble in loadout) and (Morph in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or ( (Speedball in loadout) and (Ice in loadout) ) ) and (( (OceanShoreR in loadout) and ( (Super in loadout) or ( (pinkDoor in loadout) and ( (DarkVisor in loadout) or ( (GravitySuit in loadout) and (Screw in loadout) ) ) ) ) ) or ( (EleToTurbidPassageR in loadout) and (Super in loadout) and (Speedball in loadout) ) )))
    ),
    "Sediment Floor": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (Super in loadout) and
        (
            (
                (GravitySuit in loadout)
            ) or (
                (HiJump in loadout) and
                (
                    ((Tricks.uwu_2_tile in loadout) and (Tricks.crouch_precise)) or
                    (Tricks.freeze_hard in loadout)
                )
            ) or (
                (Tricks.sbj_underwater_no_hjb in loadout) and
                (Tricks.freeze_hard in loadout)
            )
        )
    ),
    "Sandy Gully": lambda loadout: (
            # Casual: (OceanShoreR in loadout) and (jumpAble in loadout) and (GravitySuit in loadout) and ((HiJump in loadout) or ( (SpaceJump in loadout) and (SpaceJumpBoost in loadout) )) and (Super in loadout))
            # Expert: (OceanShoreR in loadout) and (underwater in loadout) and (Super in loadout)))
    ),  # TODO: sjb in logical fill and maybe a logic shortcut for how many
    "Hall Of The Elders": lambda loadout: (
            # Casual: (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (( (GravitySuit in loadout) and ((HiJump in loadout) or (canFly in loadout)) ) or (pinkDoor in loadout)))
            # Expert: (RuinedConcourseBL in loadout) and ((GravitySuit in loadout) or ( (HiJump in loadout) and (Ice in loadout) ) or (pinkDoor in loadout))))
    ),
    "Warrior Shrine: AmmoTank bottom": lambda loadout: (
        (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (Morph in loadout) and (pinkDoor in loadout)
    ),
    "Warrior Shrine: AmmoTank top": lambda loadout: (
            # Casual: (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and (Speedball in loadout))
            # Expert: (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout)))
    ),
    "Path Of Swords": lambda loadout: (
            # Casual: (vulnar in loadout) and ((canBomb in loadout) or ((Morph in loadout) and (Screw in loadout))))
            # Expert: (vulnar in loadout) and ( (canBomb in loadout) or ( (Morph in loadout) and (Screw in loadout) ) )))
    ),
    "Auxiliary Pump Room": lambda loadout: (
        (vulnar in loadout) and (canBomb in loadout)
    ),
    "Monitoring Station": lambda loadout: (
            # Casual: (vulnar in loadout) and (Morph in loadout) and ((Speedball in loadout) or (canBomb in loadout)))
            # Expert: (vulnar in loadout) and (Morph in loadout)))
    ),  # TODO: check an area door, don't assume that we start by vulnar  TODO: check an area door, don't assume that we start by vulnar
    "Sensor Maintenance: AmmoTank": lambda loadout: (
            # Casual: (vulnar in loadout) and (canBomb in loadout) and (Speedball in loadout) and (ammo_req(25) in loadout))
            # Expert: (vulnar in loadout) and (canBomb in loadout) and ( (Super in loadout) or (canUsePB in loadout) )))
    ),  # back  back
    "Causeway Overlook": lambda loadout: (
        (CausewayR in loadout) and (jumpAble in loadout) and (canBomb in loadout)
    ),
    "Placid Pool": lambda loadout: (
            # Casual: (PlacidPoolR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (icePod in loadout) and (GravitySuit in loadout))
            # Expert: (PlacidPoolR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (icePod in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) )))
    ),
    "Blazing Chasm": lambda loadout: (
            # Casual: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (GravitySuit in loadout) and (Varia in loadout) and (MetroidSuit in loadout))
            # Expert: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (varia_or_hell_run(850) in loadout) and (MetroidSuit in loadout)))
    ),
    "Generator Manifold": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Super in loadout) and (canBomb in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and (GravitySuit in loadout) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and (Screw in loadout) )))
            # Expert: (jumpAble in loadout) and (Super in loadout) and (canBomb in loadout) and (( (ReservoirMaintenanceTunnelR in loadout) and ((GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout)) ) or ( (GeneratorAccessTunnelL in loadout) and (canUsePB in loadout) and (MetroidSuit in loadout) and (Screw in loadout) ) or ( (ThermalReservoir1R in loadout) and (varia_or_hell_run(250) in loadout) and (MetroidSuit in loadout) and (Screw in loadout) ))))
    ),
    "Fiery Crossing Cache": lambda loadout: (
            # Casual: (RagingPitL in loadout) and (jumpAble in loadout) and (Varia in loadout) and (canUsePB in loadout))
            # Expert: (RagingPitL in loadout) and (jumpAble in loadout) and (varia_or_hell_run(550) in loadout) and (canUsePB in loadout)))
    ),
    "Dark Crevice Cache": lambda loadout: (
            # Casual: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (canBomb in loadout) and ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout)) and (DarkVisor in loadout))
            # Expert: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (canBomb in loadout) and ((canFly in loadout) or (SpeedBooster in loadout) or (HiJump in loadout))))
    ),
    "Ancient Basin": lambda loadout: (
            # Casual: (Varia in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (pinkDoor in loadout) and (Morph in loadout) ) or ( (CollapsedPassageR in loadout) and (Super in loadout) and (canUsePB in loadout) and (wave in loadout) )))
            # Expert: (jumpAble in loadout) and (pinkDoor in loadout) and (( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) and (varia_or_hell_run(450) in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) and (Morph in loadout) and (varia_or_hell_run(350) in loadout) ) or ( (CollapsedPassageR in loadout) and (canBomb in loadout) and (wave in loadout) and (varia_or_hell_run(750) in loadout) ))))
    ),
    "Central Corridor: right": lambda loadout: (
            # Casual: (FoyerR in loadout) and (jumpAble in loadout) and ((GravitySuit in loadout) or ( (HiJump in loadout) and (Ice in loadout) )) and (canBomb in loadout) and (eastCorridor in loadout))
            # Expert: (jumpAble in loadout) and (canBomb in loadout) and ( (FoyerR in loadout) or ( (ConstructionSiteL in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) ) or ( (WestCorridorR in loadout) and (Screw in loadout) and (pinkDoor in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or (Speedball in loadout) ) ) )))
    ),
    "Briar: AmmoTank": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Morph in loadout) and (norakToLifeTemple in loadout))
            # Expert: (jumpAble in loadout) and (Morph in loadout) and (( (NorakBrookL in loadout) and ( (GravitySuit in loadout) or (Ice in loadout) or (HiJump in loadout) or (Speedball in loadout) or (SpaceJump in loadout) or (Bombs in loadout) or (SpeedBooster in loadout) ) ) or ( (NorakPerimeterTR in loadout) and (MetroidSuit in loadout) ) or ( (NorakPerimeterBL in loadout) and (canBomb in loadout) ) )))
    ),  # bottom  bottom
    "Icy Flow": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (SpeedBooster in loadout) and (breakIce in loadout))
            # Expert: (MezzanineConcourseL in loadout) and (jumpAble in loadout) and (SpeedBooster in loadout) and (breakIce in loadout)))
    ),
    "Ice Cave": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (breakIce in loadout))
            # Expert: (jumpAble in loadout) and (breakIce in loadout) and (railAccess in loadout)))
    ),
    "Antechamber": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (canUsePB in loadout))
            # Expert: (jumpAble in loadout) and (canUsePB in loadout) and (railAccess in loadout)))
    ),
    "Eddy Channels": lambda loadout: (
            # Casual: (EleToTurbidPassageR in loadout) and (GravitySuit in loadout) and (DarkVisor in loadout) and (Morph in loadout) and (Speedball in loadout) and (Super in loadout))
            # Expert: (EleToTurbidPassageR in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) ) and (Morph in loadout) and (Speedball in loadout) and (Super in loadout)))
    ),
    "Tram To Suzi Island": lambda loadout: (
        (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (Spazer in loadout) and (Morph in loadout)
    ),
    "Portico": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (Super in loadout) and (energy_req(650) in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (Super in loadout) and (energy_req(350) in loadout)))
    ),
    "Tower Rock Lookout": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (energy_req(650) in loadout) and (GravitySuit in loadout) and (SpaceJump in loadout) and (HiJump in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (pinkDoor in loadout) and (energy_req(350) in loadout) and (GravitySuit in loadout) and ( ( (SpaceJump in loadout) and (HiJump in loadout) ) or ( (Bombs in loadout) and (Morph in loadout) ) or (SpeedBooster in loadout) )))
    ),
    "Reef Nook": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (energy_req(650) in loadout) and (GravitySuit in loadout) and (SpaceJump in loadout) and (HiJump in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (pinkDoor in loadout) and (energy_req(350) in loadout) and (GravitySuit in loadout) and (Morph in loadout) and ( ( (SpaceJump in loadout) and (HiJump in loadout) ) or (Bombs in loadout) or (SpeedBooster in loadout) )))
    ),
    "Saline Cache": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (Super in loadout) and (energy_req(650) in loadout) and (GravitySuit in loadout) and (canFly in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (Super in loadout) and (energy_req(350) in loadout) and ( (GravitySuit in loadout) or ( (HiJump in loadout) and (Speedball in loadout) and (Morph in loadout) ) )))
    ),
    "Enervation Chamber": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (suzi in loadout) and (energy_req(650) in loadout) and (canFly in loadout) and (Hypercharge in loadout) and (Charge in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (suzi in loadout) and (Hypercharge in loadout) and (Charge in loadout)))
    ),
    "Weapon Locker": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (pinkDoor in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Grapple in loadout) and (pinkDoor in loadout) ))
            # Expert: ((spaceDrop not in loadout) and (pinkDoor in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (pinkDoor in loadout) and ( (Grapple in loadout) or ( (Super in loadout) and ( (Xray in loadout) or (Ice in loadout) ) ) ) )))
    ),
    "Aft Battery": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (Morph in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Grapple in loadout) and (Morph in loadout) ))
            # Expert: ((spaceDrop not in loadout) and (Morph in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Morph in loadout) and ( (Grapple in loadout) or ( (Super in loadout) and ( (Xray in loadout) or (Ice in loadout) ) ) ) )))
    ),
    "Forward Battery": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (pinkDoor in loadout) and (Morph in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (Grapple in loadout) and (MetroidSuit in loadout) and (pinkDoor in loadout) ))
            # Expert: ((spaceDrop not in loadout) and (pinkDoor in loadout) and (Morph in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (Grapple in loadout) and (MetroidSuit in loadout) and (pinkDoor in loadout) and ( (Grapple in loadout) or ( (Super in loadout) and ( (Xray in loadout) or (Ice in loadout) ) ) ) )))
    ),
    "Gantry": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (pinkDoor in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Grapple in loadout) and (pinkDoor in loadout) ))
            # Expert: ((spaceDrop not in loadout) and (pinkDoor in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (Grapple in loadout) and (pinkDoor in loadout) and ( (Grapple in loadout) or ( (Super in loadout) and ( (Xray in loadout) or (Ice in loadout) ) ) ) )))
    ),
    "Garden Canal": lambda loadout: (
            # Casual: (NorakPerimeterBL in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (Spazer in loadout) and (veranda in loadout))
            # Expert: (jumpAble in loadout) and (canUsePB in loadout) and (Spazer in loadout) and (NorakPerimeterBL in loadout)))
    ),  # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    "Sandy Burrow: AmmoTank": lambda loadout: (
            # Casual: (OceanShoreR in loadout) and (GravitySuit in loadout) and (Morph in loadout) and  (loadout.has_any(Speedball ((HiJump in loadout) or (canFly in loadout)))
            # Expert: (OceanShoreR in loadout) and (jumpAble in loadout) and (Morph in loadout) and ( (GravitySuit in loadout) or ( (HiJump in loadout) and ( (Speedball in loadout) or (Ice in loadout) ) ) )))
    ),  # bottom  bottom  to get back in hole after getting this item
    "Trophobiotic Chamber": lambda loadout: (
        (vulnar in loadout) and (Morph in loadout) and (Speedball in loadout)
    ),
    "Waste Processing": lambda loadout: (
            # Casual: (SpeedBooster in loadout) and (jumpAble in loadout) and ( ( (SubbasementFissureL in loadout) and (canUsePB in loadout) ) or ( (CellarR in loadout) and (pinkDoor in loadout) and (canBomb in loadout) and (underwater in loadout) and (DarkVisor in loadout) ) or ( (TransferStationR in loadout) and (DarkVisor in loadout) and (wave in loadout) and (canBomb in loadout) ) ))
            # Expert: (jumpAble in loadout) and (SpeedBooster in loadout) and (( (SubbasementFissureL in loadout) and (canUsePB in loadout) ) or ( (CellarR in loadout) and (pinkDoor in loadout) and (canBomb in loadout) ) or ( (FieldAccessL in loadout) and (pinkDoor in loadout) and (wave in loadout) and (canBomb in loadout) ) or ( (TransferStationR in loadout) and (DarkVisor in loadout) and (wave in loadout) and (canBomb in loadout) ))))
    ),
    "Grand Chasm": lambda loadout: (
        (railAccess in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (Screw in loadout)
    ),
    "Mining Site 1": lambda loadout: (
            # Casual: (canBomb in loadout) and ((Speedball in loadout) or (Bombs in loadout)) and (jumpAble in loadout) and (pinkDoor in loadout) and (( (EleToTurbidPassageR in loadout) and (Varia in loadout) ) or ( (SporousNookL in loadout) and (GravitySuit in loadout) )))
            # Expert: (jumpAble in loadout) and (canBomb in loadout) and (pinkDoor in loadout) and ( ( (FieryGalleryL in loadout) and (varia_or_hell_run(550) in loadout) ) or ( (SporousNookL in loadout) and (hotSpring in loadout) ) )))
    ),  # (1 = letter Alpha)  (1 = letter Alpha)  short morph jump
    "Colosseum": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (Varia in loadout) and (Charge in loadout)
    ),  # GT  GT
    "Lava Pool": lambda loadout: (
            # Casual: (loadout.has_all(EleToTurbidPassageR ))
            # Expert: (loadout.has_all(jumpAble ( (FieryGalleryL in loadout) or ( (SporousNookL in loadout) and (hotSpring in loadout) ) ) )))
    ),  # No bath count in casual
    "Hive Main Chamber": lambda loadout: (
            # Casual: (VulnarDepthsElevatorEL in loadout) and (jumpAble in loadout) and (Varia in loadout) and (canBomb in loadout))
            # Expert: (jumpAble in loadout) and ( ( (VulnarDepthsElevatorEL in loadout) and (varia_or_hell_run(650) in loadout) and (canBomb in loadout) ) or ( (SequesteredInfernoL in loadout) and (varia_or_hell_run(250) in loadout) and (Morph in loadout) and (icePod in loadout) ) )))
    ),
    "Crossway Cache": lambda loadout: (
            # Casual: (jumpAble in loadout) and (Varia in loadout) and ( (VulnarDepthsElevatorEL in loadout) and (canBomb in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) ) or ( (CollapsedPassageR in loadout) and (pinkDoor in loadout) and (canBomb in loadout) and (wave in loadout) ))
            # Expert: (jumpAble in loadout) and ( (VulnarDepthsElevatorEL in loadout) and (varia_or_hell_run(650) in loadout) and (canBomb in loadout) and (icePod in loadout) ) or ( (SequesteredInfernoL in loadout) and (varia_or_hell_run(350) in loadout) and (electricHyper in loadout) ) or ( (CollapsedPassageR in loadout) and (Super in loadout) and (varia_or_hell_run(750) in loadout) and (canBomb in loadout) and (wave in loadout) )))
    ),
    "Slag Heap": lambda loadout: (
            # Casual: (canBomb in loadout) and (jumpAble in loadout) and (icePod in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and (SequesteredInfernoL in loadout))
            # Expert: (canBomb in loadout) and (jumpAble in loadout) and (varia_or_hell_run(950) in loadout) and (MetroidSuit in loadout) and (icePod in loadout) and (( (VulnarDepthsElevatorEL in loadout) and ((Ice in loadout) or ((Hypercharge in loadout) and (Charge in loadout))) ) or ( (SequesteredInfernoL in loadout) and (electricHyper in loadout) ) or ( (CollapsedPassageR in loadout) and (Super in loadout) and (canBomb in loadout) and (wave in loadout) ))))
    ),  # Consider bath counts  for getting out  No Metroid-less lava baths in casual  TODO: include paths from other doors?  unit test works from CollapsedPassageR
    "Hydrodynamic Chamber": lambda loadout: (
            # Casual: (Morph in loadout) and (Spazer in loadout) and ( (WestCorridorR in loadout) and (( (pinkDoor in loadout) and ((GravitySuit in loadout) or ( (HiJump in loadout) and (Ice in loadout) )) ) or ( (Super in loadout) and ((GravitySuit in loadout) or (HiJump in loadout)) )) ) or ( (FoyerR in loadout) and (eastCorridor in loadout) and (Screw in loadout) ))
            # Expert: (jumpAble in loadout) and (Spazer in loadout) and (Morph in loadout) and ( ( (ConstructionSiteL in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) and (Screw in loadout) ) or ( (WestCorridorR in loadout) and (pinkDoor in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or ((Morph in loadout) and (Speedball in loadout)) ) ) or ( (FoyerR in loadout) and (canBomb in loadout) and (Screw in loadout) ) )))
    ),  # one of the only intended water rooms
    "Central Corridor: left": lambda loadout: (
        (FoyerR in loadout) and (jumpAble in loadout) and (GravitySuit in loadout) and (Speedball in loadout) and (SpeedBooster in loadout) and (Morph in loadout)
    ),
    "Restricted Area": lambda loadout: (
            # Casual: (FoyerR in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) and (canBomb in loadout) and (Speedball in loadout))
            # Expert: (jumpAble in loadout) and (MetroidSuit in loadout) and ( ( (WestCorridorR in loadout) and (pinkDoor in loadout) and (Screw in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or (Speedball in loadout) ) ) or ( (FoyerR in loadout) and (canBomb in loadout) ) or ( (ConstructionSiteL in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) ) )))
    ),
    "Foundry": lambda loadout: (
            # Casual: (FoyerR in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (Speedball in loadout) and (energy_req(250) in loadout))
            # Expert: (jumpAble in loadout) and (Morph in loadout) and ( ( (WestCorridorR in loadout) and (pinkDoor in loadout) and (Screw in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or (Speedball in loadout) ) ) or ( (FoyerR in loadout) and (canBomb in loadout) ) or ( (ConstructionSiteL in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) ) )))
    ),  # Worth testing
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and (jumpAble in loadout) and (canFly in loadout)
    ),
    "Glacier's Reach": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (canBomb in loadout) and (varia_or_hell_run(650) in loadout))
            # Expert: (jumpAble in loadout) and (varia_or_hell_run(350) in loadout) and (railAccess in loadout)))
    ),
    "Sitting Room": lambda loadout: (
            # Casual: (railAccess in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (Speedball in loadout))
            # Expert: (jumpAble in loadout) and (canUsePB in loadout) and ( (Bombs in loadout) or (Speedball in loadout) ) and (railAccess in loadout)))
    ),  # TODO: this is missing exit logic - what do you need to get mack to rail?  (at least supers or missiles or screw)  TODO: energy_req or varia
    "Suzi Ruins Map Station Access": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (energy_req(650) in loadout) and (canUsePB in loadout) and (Super in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (energy_req(350) in loadout) and (canUsePB in loadout) and (Super in loadout)))
    ),
    "Obscured Vestibule": lambda loadout: (
            # Casual: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (energy_req(650) in loadout) and (canBomb in loadout))
            # Expert: (TramToSuziIslandR in loadout) and (jumpAble in loadout) and (wave in loadout) and (energy_req(350) in loadout) and (canBomb in loadout)))
    ),
    "Docking Port 3": lambda loadout: (
            # Casual: ((spaceDrop not in loadout) and (Grapple in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (MetroidSuit in loadout) ))
            # Expert: ((spaceDrop not in loadout) and (Grapple in loadout) ) or ( (spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and (jumpAble in loadout) and (MetroidSuit in loadout) )))
    ),  # (3 = letter Gamma)  (3 = letter Gamma)
    "Arena": lambda loadout: (
            # Casual: (RuinedConcourseBL in loadout) and (jumpAble in loadout) and (canBomb in loadout) and ( (pinkDoor in loadout) or ( (GravitySuit in loadout) and ( (HiJump in loadout) or (SpaceJump in loadout) or (Bombs in loadout) ) ) ))
            # Expert: (RuinedConcourseBL in loadout) and (jumpAble in loadout) and ( (pinkDoor in loadout) or ( ( (HiJump in loadout) or (SpaceJump in loadout) or ((Speedball in loadout) and (Morph in loadout)) ) and (GravitySuit in loadout) or ( (HiJump in loadout) and ( ((Speedball in loadout) and (Morph in loadout)) or (Ice in loadout) ) ) ) )))
    ),
    "West Spore Field": lambda loadout: (
            # Casual: (vulnar in loadout) and ((canBomb in loadout) or ( (Morph in loadout) and (Screw in loadout) )) and (Super in loadout) and (Speedball in loadout) and (GravitySuit in loadout))
            # Expert: (vulnar in loadout) and (Super in loadout) and ( (canBomb in loadout) or ( (Morph in loadout) and (Screw in loadout) ) ) and ( (GravitySuit in loadout) or ( (SpaceJump in loadout) and ( (HiJump in loadout) or (Speedball in loadout) ) ) )))
    ),
    "Magma Chamber": lambda loadout: (
            # Casual: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and (canUsePB in loadout) and (Varia in loadout) and ((Charge in loadout) or (MetroidSuit in loadout)))
            # Expert: (ElevatorToMagmaLakeR in loadout) and (jumpAble in loadout) and (canUsePB in loadout) and (( (Varia in loadout) and (Charge in loadout) ) or ( (MetroidSuit in loadout) and (varia_or_hell_run(650) in loadout) ))))
    ),
    "Equipment Locker": lambda loadout: (
        (WestCorridorR in loadout) and (jumpAble in loadout) and (pinkDoor in loadout) and ((GravitySuit in loadout) or (HiJump in loadout) or (canBomb in loadout)) and ((MetroidSuit in loadout) or (Morph in loadout))
    ),
    "Antelier": lambda loadout: (
            # Casual: ((WestCorridorR in loadout) and ( (GravitySuit in loadout) or ( (HiJump in loadout) and (Ice in loadout) ) ) and (( (pinkDoor in loadout) and (Morph in loadout) ) or ( (Super in loadout) and ( (Morph in loadout) or (MetroidSuit in loadout) ) )) ) or ( (FoyerR in loadout) and (eastCorridor in loadout) and (Screw in loadout) and ( (GravitySuit in loadout) or (  (HiJump in loadout) and (Ice in loadout) ) ) ))
            # Expert: (jumpAble in loadout) and ( ( (ConstructionSiteL in loadout) and (Morph in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) and (Screw in loadout) ) or ( (WestCorridorR in loadout) and ( ((pinkDoor in loadout) and (Morph in loadout)) or ((MetroidSuit in loadout) and (Super in loadout)) ) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or ((Morph in loadout) and (Speedball in loadout)) ) ) or ( (FoyerR in loadout) and (canBomb in loadout) and (Screw in loadout) ) )))
    ),  # spelled "Antilier" in subversion 1.1  spelled "Antilier" in subversion 1.1  freeze pancake to stand on  gravity jump through hydrodynamic chamber door into main hydrology research from central corridor  freeze pancake to stand on
    "Weapon Research": lambda loadout: (
            # Casual: ( (jumpAble in loadout) and (Speedball in loadout) and (Morph in loadout) and ((wave in loadout) or (MetroidSuit in loadout)) and ( (FoyerR in loadout) and (canBomb in loadout) ) or ( (WestCorridorR in loadout) and ((GravitySuit in loadout) or (HiJump in loadout)) and (pinkDoor in loadout) and (Spazer in loadout) ) ))
            # Expert: (jumpAble in loadout) and ((wave in loadout) or (MetroidSuit in loadout)) and ((canBomb in loadout) or ((Spazer in loadout) and (Morph in loadout))) and ( ( (ConstructionSiteL in loadout) and (Morph in loadout) and ((wave in loadout) or (Spazer in loadout)) and (Bombs in loadout) ) or ( (WestCorridorR in loadout) and (Screw in loadout) and (pinkDoor in loadout) and (Morph in loadout) and ( (GravitySuit in loadout) or (HiJump in loadout) or (Ice in loadout) or ((Morph in loadout) and (Speedball in loadout)) ) ) or ( (FoyerR in loadout) and (canBomb in loadout) ) )))
    ),  # TODO: review this location logic
    "Crocomire's Lair": lambda loadout: (
            # Casual: ((jumpAble in loadout) and (Super in loadout) and (SpeedBooster in loadout) and (veranda in loadout) and (norakToLifeTemple in loadout) ) }   class Casual(LogicInterface):)
            # Expert: ((NorakPerimeterBL in loadout) and (jumpAble in loadout) and (Super in loadout) and (SpeedBooster in loadout) ) }   class Expert(LogicInterface):))
    ),
}
