from connection_data import area_doors_unpackable
from item_data import items_unpackable
from logicCommon import ammo_req, can_bomb, can_use_pbs, energy_req, varia_or_hell_run
from logic_shortcut import LogicShortcut
from logic_shortcut_data import (
    canFly, shootThroughWalls, breakIce, missileDamage, pinkDoor,
    missileBarrier, electricHyper, killRippers
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


class Verdite:
    hotSpring = LogicShortcut(lambda loadout: (
        # which hole you use in the top of hot spring determines
        # how much ammo you need if you need to use power bombs for the verdite mines entrance blocks
        # and whether you need morph and the 3 tile morph jump
        ((
            (Super in loadout) and
            ((
                (Morph in loadout) and
                (Bombs in loadout)
            ) or (
                (Screw in loadout)
            ) or (
                (PowerBomb in loadout) and
                (Morph in loadout) and
                (ammo_req(25) in loadout)
            ))
        ) or (
            (breakIce in loadout) and
            (Morph in loadout) and
            ((
                (GravitySuit in loadout) and
                ((can_bomb(3) in loadout) or loadout.has_all(Screw, can_bomb(1)))
            ) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout)) and
            ((
                (can_bomb(2) in loadout)
            ) or (
                (Screw in loadout)
            ))
        ) or (
            # bomb block hole
            (Morph in loadout) and
            ((
                (GravitySuit in loadout) and
                ((can_bomb(3) in loadout) or loadout.has_all(Screw, can_bomb(1)))
            ) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout)) and
            ((
                (can_bomb(3) in loadout)
            ) or (
                (Screw in loadout)
            ))
        )) and
        (
            (GravitySuit in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout) or
            ((HiJump in loadout) and (Ice in loadout))
        )
    ))
    """ traverse "Hot Spring" between Sporous Nook and Verdite Mines (including Verdite Mines Entrance) """


class SkyWorld:
    # TODO: make sure any "both ways" usages of this also check for Screw
    meetingHall = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        ((breakIce in loadout) or (
            (Speedball in loadout) and
            ((Tricks.clip_crouch in loadout) or (can_bomb(1) in loadout))
        ) or (
            (can_bomb(1) in loadout) and
            ((Tricks.morph_jump_3_tile in loadout) or (can_bomb(2) in loadout))
        ))
        # right to left, use clip by ice blocks or bomb furthest right block and then break bomb block with screw
        # left to right has a 2 tile space for morph jump if no plasma
    ))
    """
    Grand Promenade through Meeting Hall to Stair of Twilight

    Any "both ways" usages of this should also check for Screw, because this is used for some exit only logic.
    """

    mezzanineShaft = LogicShortcut(lambda loadout: (
        (SpaceJump in loadout) or
        ((
            (killRippers in loadout) or
            (Tricks.movement_moderate in loadout)
            # using movement_moderate to control speed of bomb jumping to not run into rippers
        ) and (canFly in loadout)) or
        (SpeedBooster in loadout) or
        ((HiJump in loadout) and (Tricks.wall_jump_precise in loadout)) or  # wall jump around 3 tiles
        (Ice in loadout) or
        ((Speedball in loadout) and (Tricks.sbj_wall in loadout))
    ))
    """ up mezzanine concourse """

    condenser = LogicShortcut(lambda loadout: (
        (  # up into the door from the platform below the door
            (GravitySuit in loadout) or
            ((Speedball in loadout) and (Tricks.sbj_underwater_no_hjb in loadout)) or
            (HiJump in loadout)
        ) and
        (
            ((Ice in loadout) and (Tricks.movement_moderate in loadout)) or
            # movement just because there are so many enemies in the room
            (
                (GravitySuit in loadout) and
                # aqua suit alone won't do it
                (loadout.has_any(Tricks.gravity_jump, HiJump, Ice, Grapple, canFly, Tricks.short_charge_2))
                # Yes. Some day we will find that person that can't do a gravity jump, but can do a 2-tap short charge.
            ) or
            ((Grapple in loadout) and (Tricks.movement_moderate in loadout)) or
            (Tricks.sbj_underwater_w_hjb in loadout)
        ) and
        (GravityBoots in loadout) and
        (varia_or_hell_run(90) in loadout)  # hell_run_hard won't need any tanks, but others will
    ))
    """ traverse condenser room """

    killPhantoon = LogicShortcut(lambda loadout: (
        (DarkVisor in loadout) and
        loadout.has_any(missileDamage, Charge) and
        ((Tricks.movement_zoast in loadout) or (
            (Tricks.movement_moderate in loadout) and
            (energy_req(250) in loadout)
        ) or (
            (energy_req(450) in loadout)
        ))
    ))

    killRidley = LogicShortcut(lambda loadout: (
        # These numbers are all guesses, they might need to be tuned.
        # TODO: Should these numbers depend on damage amp and accel charge?
        (
            (MetroidSuit in loadout) and
            (Varia in loadout) and
            ((energy_req(850) in loadout) or (
                (Tricks.movement_moderate in loadout) and
                (energy_req(650) in loadout)
            ) or (
                (Tricks.movement_zoast in loadout) and
                (energy_req(450) in loadout)
            ))
            # TODO: energy w/o varia?
        ) or (
            (Charge in loadout) and
            (Hypercharge in loadout) and
            ((
                (energy_req(480) in loadout) and
                (varia_or_hell_run(680) in loadout)
            ) or (
                (Tricks.movement_moderate in loadout) and
                (energy_req(280) in loadout) and
                (varia_or_hell_run(480) in loadout)
            ) or (
                (Tricks.movement_zoast in loadout) and
                (energy_req(80) in loadout) and
                (varia_or_hell_run(280) in loadout)
            ))
        )
    ))


class PirateLab:
    constructionLToElevator = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((Screw in loadout) or (can_bomb(1) in loadout)) and  # through wall
        (  # through the passage lined with screw blocks
            (
                (GravitySuit in loadout) and
                (Morph in loadout) and
                (Tricks.morph_jump_4_tile in loadout)
            ) or (
                (Screw in loadout)
            ) or (
                ((Speedball in loadout) or (
                    (Bombs in loadout) and (GravitySuit in loadout)  # normal bomb jumping if have aqua
                )) and
                ((Bombs in loadout) or (GravitySuit)) and  # if no aqua, a combination of bouncing and bombs is easy
                (Morph in loadout)
            ) or (
                (Tricks.movement_moderate in loadout) and
                (can_bomb(1) in loadout) and
                (HiJump in loadout) and
                # I tried a single (pb) bomb jump without hi jump and couldn't get it to work.
                # If it does work, it's probably `movement_zoast` (pixel perfect?).
                (Speedball in loadout)
            )
        )
    ))
    """ from ConstructionSiteL door to the elevator that is under construction """

    epiphreaticCrag_left = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (
            # with no high jump, in the right shot block passage,
            # wall jump into morph
            (
                (Tricks.movement_moderate in loadout) and
                loadout.has_any(Tricks.morph_jump_4_tile, Speedball, Bombs) and
                (Tricks.crouch_or_downgrab in loadout)  # right to left under water
            ) or

            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Speedball in loadout) and
                (can_use_pbs(1) in loadout) and
                (Tricks.crouch_or_downgrab in loadout)
            )
        )
    ))
    """ up to the outside wall of the pirate lab """

    epiphreaticCrag_right = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (
            (shootThroughWalls in loadout) or
            (Tricks.spazer_into_lower_pirate_lab in loadout)
        ) and
        (Bombs in loadout)  # open gate from right side (and the 2-tile morph jump to get into that passage)
    ))
    """ gate into the pirate lab """

    epiphreaticCrag = LogicShortcut(lambda loadout: (
        (PirateLab.epiphreaticCrag_left in loadout) and
        (PirateLab.epiphreaticCrag_right in loadout)
    ))
    """ epiphreatic crag left and right, in and out of pirate lab """

    exitMainHydrologyResearch = LogicShortcut(lambda loadout: (
        (GravitySuit in loadout) or
        (Ice in loadout) or  # freeze pancake to stand on
        (Tricks.sbj_underwater_w_hjb in loadout)
    ))

    waterGauntlet_oneWay = LogicShortcut(lambda loadout: (
        (pinkDoor in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        (  # first room
            (HiJump in loadout) or

            # gravity jump through door - not gravity jump trick, because that requires gravity suit
            (Tricks.movement_moderate in loadout) or

            (GravitySuit in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout)
        ) and
        (  # last room
            (HiJump in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout) or
            (GravitySuit in loadout) or
            ((
                (can_use_pbs(2) in loadout)
            ) and (
                (Tricks.morph_jump_3_tile_water in loadout) or (Speedball in loadout)
            )) or
            ((Bombs in loadout) and (Speedball in loadout))
        ) and
        (PirateLab.exitMainHydrologyResearch in loadout)
    ))
    """
    from top or west corridor to right side of hydrodynamic chamber

    one way (never use this alone)
    """

    hydrodynamicChamber = LogicShortcut(lambda loadout: (
        (GravitySuit in loadout) or
        (HiJump in loadout) or
        (loadout.has_all(Ice, Tricks.freeze_hard, Tricks.movement_zoast)) or
        ((Speedball in loadout) and (Tricks.sbj_underwater_no_hjb in loadout))
    ))
    """ only inside the room, not including the super door """

    westCorridorToCentralTop = LogicShortcut(lambda loadout: (
        (PirateLab.hydrodynamicChamber in loadout) and
        (
            ((pinkDoor in loadout) and (PirateLab.waterGauntlet_oneWay in loadout)) or
            ((Super in loadout) and ((Morph in loadout) or (MetroidSuit in loadout)))
        )
    ))
    """ from west corridor to the top of central corridor (not through screw to go lower) """

    centralCorridorWater = LogicShortcut(lambda loadout: (
        ((
            (Tricks.movement_zoast in loadout)  # gravity jump through door
            # (not gravity jump trick because that requires gravity suit)
        ) or (
            (GravitySuit in loadout)
        ) or (
            (Ice in loadout)  # freeze atomic
        ) or (
            # high jump gets you high enough to wall jump
            (HiJump in loadout) and
            (Tricks.wall_jump_precise in loadout)
        ))
        # TODO: can springball jump get me out?
    ))
    """ get out of the water in central corridor """

    # TODO: make sure this is in all of the places that reference FoyerR
    eastCorridor = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (  # 4 tile morph jump
            (Bombs in loadout) or
            (Speedball in loadout) or
            (Tricks.morph_jump_4_tile in loadout)
        ) and
        (  # open the shot block from below
            ((Tricks.movement_moderate in loadout) and (electricHyper in loadout)) or
            (can_bomb(1) in loadout) or
            (shootThroughWalls in loadout)
        )
    ))
    """ top of East Corridor to get to Foyer """


class LifeTemple:
    waterGardenBottom = LogicShortcut(lambda loadout: (
        ((GravitySuit in loadout) or (Ice in loadout) or (Tricks.sbj_underwater_w_hjb in loadout)) and
        ((
            (Tricks.morph_jump_4_tile in loadout) and
            (can_bomb(3) in loadout)
        ) or (
            (Tricks.morph_jump_4_tile in loadout) and
            (can_bomb(1) in loadout) and
            (Speedball in loadout)
        ) or (
            (can_bomb(1) in loadout) and
            ((Speedball in loadout) or (Bombs in loadout))
        ))
    ))
    """ get into water garden from wellspring access """

    brook = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((
            (GravitySuit in loadout)
        ) or (
            (SpaceJump in loadout) and
            (HiJump in loadout)
        ) or (
            (Ice in loadout) and
            (Tricks.freeze_hard in loadout)
        ) or (
            (HiJump in loadout) and
            (Tricks.movement_moderate in loadout)
        ) or (
            (Speedball in loadout) and
            (Tricks.sbj_underwater_no_hjb in loadout)  # is this harder at the surface of the water?
        ) or (
            (SpaceJump in loadout) and
            (Tricks.movement_moderate in loadout)
        ) or (
            (Bombs in loadout) and
            (Tricks.movement_zoast in loadout)  # TODO: I don't know what trick this is
        ) or (
            (SpeedBooster in loadout) and  # 1-tap short charge from norak perimeter
            (Tricks.movement_moderate in loadout)
        ))
    ))
    """ to get across Norak Brook (bottom right to left) """

    perimBL = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((Morph in loadout) or (
            (Tricks.movement_zoast in loadout)
            # This isn't that hard, but I'm making it movement_zoast because
            # if you don't have morph, you're likely to softlock trying to do it.
            # TODO: You're not softlocked with the super-sink (slopekiller) trick.
        )) and
        ((can_bomb(1) in loadout) or (Screw in loadout) or (
            (Tricks.short_charge_2 in loadout) and
            ((
                (Tricks.movement_zoast in loadout) and
                (Morph in loadout)
            ) or (
                (Tricks.movement_moderate in loadout) and
                (Morph in loadout) and (Speedball in loadout)
            ))
        ))
    ))
    """ between Norak Perimeter bottom left and main area of norak perimeter """

    veranda = LogicShortcut(lambda loadout: (
        ((  # bottom to top
            (Tricks.short_charge_3 in loadout)
            # TODO: a patience trick with bomb jumping all the way?
        ) or (
            (  # bottom to middle
                ((
                    (Tricks.movement_moderate in loadout)
                    # If you don't have anything,
                    # you can wall jump off of the wall right above the door to Hopper Nest,
                    # then wall jump off the ledge just outside the door to Jungle Map Station access,
                    # to get to the middle level.
                ) or (
                    (HiJump in loadout)
                ) or (
                    (canFly in loadout)
                ))
            ) and
            (  # middle to top
                (Morph in loadout) or  # morph tunnel in top right
                (canFly in loadout) or
                ((HiJump in loadout) and (Tricks.movement_moderate in loadout))
                # If you have HiJump and no Morph, then you wall jump off the green wall above the
                # door to Jungle Map Station Access, or the bricks across from it.
            )
        )) and
        (GravityBoots in loadout)
    ))
    """ to get from the bottom of Veranda to the top """


class FireHive:
    infernalSequestration = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((MetroidSuit in loadout) or (
            # passage underneath laser
            (Charge in loadout) and
            (Hypercharge in loadout) and
            # This is kind of like electricHyper,
            # except you can't use it without morph and breaking bomb blocks and jumping in lava.
            (Morph in loadout) and
            ((Screw in loadout) or (can_bomb(1) in loadout)) and
            # have to go in lava to get to this passage
            (varia_or_hell_run(650) in loadout) and  # without varia
            (energy_req(250) in loadout)  # with varia
            # hell run tips without metroid suit:
            #   from left to right:
            #     hold charge beam and dash as you run in
            #     run off the edge without jumping
            #     release charge beam to kill ki hunter
            #     land on platform
            #     jump into lava as far right as possible
            #       should have to touch spikes only once before getting out of lava
            #     (if you need to crystal flash, do it on the slope as soon as you get out of the lava)
            #     go through hyper beam and bomb block passage
            #     platform - wall jump - door
            #   from right to left:
            #     unequip hi jump boots before entering
            #     hold charge beam and dash as you run in
            #     fall straight down off the edge
            #     face right
            #     land on platform
            #     release charge beam to kill red ball
            #     go through hyper beam and bomb block passage
            #     (if you need to crystal flash, do it on the slope next to the lava or in the corner)
            #     With dash and jump (no hi jump boots),
            #       you can jump over all the spikes and land where there are no spikes.
            #     then wall jump up to the door
        )) and
        (varia_or_hell_run(150) in loadout) and  # with metroid suit
        (electricHyper in loadout)
    ))
    """ sequestered infernal to the bottom of hive crossways """

    crossways = LogicShortcut(lambda loadout: (
        # The speedway is not in logic because it's one-way
        ((
            # freeze enemies to stand on
            (Ice in loadout)
        ) or (
            # dodging enemies
            (Tricks.movement_moderate in loadout) and
            (
                (Tricks.wall_jump_delayed in loadout) or
                (SpaceJump in loadout)
                # no SJB needed with easy wall jumps - 1 space jump can get you to the long walls
            )
        ) or (
            # kill the enemies so you don't have to dodge them
            (killRippers in loadout) and
            ((canFly in loadout) or (Tricks.wall_jump_delayed in loadout))
            # no SJB needed with easy wall jumps - 1 space jump can get you to the long walls
        )) and
        (Morph in loadout) and  # required for either bottom or east hive tunnel
        (GravityBoots in loadout)
    ))
    """ top of hive crossways """

    crosswaysToCourtyard = LogicShortcut(lambda loadout: (
        # east hive tunnel
        (Morph in loadout) and
        (pinkDoor in loadout) and  # this also serves to kill the red pirate on a platform we might need
        (varia_or_hell_run(366, heat_and_metroid_suit_not_required=True) in loadout)

        # going through the guard station takes about the same energy, but also requires PBs
        # (requires more energy if you use normal bombs)
        # so it's not worth writing logic for
    ))
    """ middle of hive crossways (bug farm) to fire temple courtyard """

    hiveEntrance = LogicShortcut(lambda loadout: (
        ((can_bomb(4) in loadout) or (
            (Speedball in loadout) and
            (can_bomb(3) in loadout)
        )) and
        # if I don't have access to crossways farm,
        # I have to turn around and come back,
        # which means double the hell run energy cost
        ((
            (FireHive.crossways in loadout) and
            (varia_or_hell_run(550, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            (varia_or_hell_run(1050, heat_and_metroid_suit_not_required=True) in loadout)
        )) and
        (GravityBoots in loadout)
    ))
    """ from elevator to infested passage """

    ancientBasinAccess = LogicShortcut(lambda loadout: (
        (
            (can_bomb(3) in loadout) or
            ((Speedball in loadout) and (can_bomb(2) in loadout))
        ) and
        (shootThroughWalls in loadout)
        # from the right, it can be opened with most of the beams, but not from the left
    ))
    """
    collapsed passage and ancient basin access

    doesn't include hell runs, because that will need to be measured separately to wherever you're going
    """


class Geothermal:
    thermalResAlpha = LogicShortcut(lambda loadout: (
        (MetroidSuit in loadout) and  # just outside left door
        (varia_or_hell_run(140) in loadout) and
        (
            (Tricks.wall_jump_precise in loadout) or
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (Grapple in loadout) or
            (loadout.has_all(GravitySuit, Morph, Bombs)) or
            ((GravitySuit in loadout) and (Tricks.gravity_jump in loadout))
        )
    ))

    thermalResBeta = LogicShortcut(lambda loadout: (
        ((GravitySuit in loadout) or (
            (Tricks.freeze_hard in loadout) and
            (Ice in loadout) and
            ((Tricks.movement_zoast in loadout) or (HiJump in loadout)) and
            (can_bomb(1) in loadout)
        )) and
        (varia_or_hell_run(80) in loadout)  # cold room
    ))


class DrayLand:
    lakeMonitoringStation = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (
            ((Tricks.short_charge_2 in loadout) and (Tricks.movement_moderate in loadout)) or
            (
                (missileBarrier in loadout) and
                loadout.has_any(Speedball, Bombs, Tricks.morph_jump_4_tile)
            )
        ) and
        # this should only be used somewhere that checks for PBs, but just in case someone forgets
        (can_use_pbs(1) in loadout)  # because this is 1-way if you use speedbooster
    ))
    """ to lower lava in magma chamber """

    killGT = LogicShortcut(lambda loadout: (
        loadout.has_all(Varia, Charge)
        # TODO: can hell run with hypercharge, or lots of beams and damage amps, or a billion supers
    ))


class SpacePort:
    spaceportTopFromElevator = LogicShortcut(lambda loadout: (
        (Grapple in loadout) or
        loadout.game.logic.can_crash_spaceport(loadout)
    ))


class Suzi:
    crossOceans = LogicShortcut(lambda loadout: (
        ((
            (SpaceJump in loadout) and
            (HiJump in loadout) and
            (SpaceJumpBoost in loadout)
            # TODO: how many sjb required?
            # TODO: how many sjb required without hjb?
        ) or (
            (Bombs in loadout) and
            (Morph in loadout) and
            (Tricks.movement_moderate in loadout)
            # TODO: how hard is this in spine reef? Do we need separate for spine reef and moughra lagoon?
        ) or (
            (SpeedBooster in loadout) and
            (Tricks.movement_moderate in loadout)
            # There are places to shinespark from the bottom of the big ocean rooms.
            # TODO: check if they require short charge
        ))
    ))

    cyphers = LogicShortcut(lambda loadout: (
        loadout.has_all(GravityBoots,
                        SpeedBooster,
                        Super,
                        shootThroughWalls,
                        can_use_pbs(1),
                        GravitySuit,
                        pinkDoor,
                        Suzi.crossOceans)
    ))
    """ get all of the cyphers """
