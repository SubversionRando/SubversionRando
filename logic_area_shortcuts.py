""" This is for logic shortcuts that apply only to 1 specific area. """

from item_data import items_unpackable
from logicCommon import ammo_req, can_bomb, can_use_pbs, energy_req, hell_run_energy, varia_or_hell_run
from logic_shortcut import LogicShortcut
from logic_shortcut_data import (
    canFly, shootThroughWalls, breakIce, missileDamage, pinkDoor,
    missileBarrier, electricHyper, killRippers, killYellowPirates,
    plasmaWaveGate, icePod, can_crash_spaceport, hiJumpSuperSink,
    bonkCeilingSuperSink, underwaterSuperSink
)
from trick_data import Tricks

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


class SkyWorld:
    meetingHallToLeft = LogicShortcut(lambda loadout: (
        ((
            # through top right
            (can_bomb(1) in loadout) and
            ((Tricks.morph_jump_3_tile in loadout) or (can_bomb(2) in loadout))
        ) or (
            # not through top right
            ((
                # through plasma tunnel
                (breakIce in loadout) and
                ((Morph in loadout) or (Tricks.morphless_tunnel_crawl in loadout))
            ) or (
                # not through plasma tunnel
                (Tricks.clip_crouch in loadout) and
                ((can_bomb(1) in loadout) or loadout.has_all(Screw, Morph))
            ))
        )) and
        # exit in grand promenade
        ((Screw in loadout) or (can_bomb(1) in loadout))
    ))
    """ including the exit in grand promenade """

    meetingHallToRight = LogicShortcut(lambda loadout: (
        # entrance in Grand Promenade
        ((Screw in loadout) or (hiJumpSuperSink in loadout)) and
        # meeting hall
        ((
            # through top right
            (Morph in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # break bomb blocks
            ((Speedball in loadout) or (can_bomb(1) in loadout))  # 2-tile space morph jump
        ) or (
            # not through top right
            # through plasma tunnel
            (breakIce in loadout) and
            ((Morph in loadout) or (Tricks.morphless_tunnel_crawl in loadout))
        ))
    ))
    """ including the entrance in grand promenade """

    meetingHall = LogicShortcut(lambda loadout: (
        (SkyWorld.meetingHallToLeft in loadout) and
        (SkyWorld.meetingHallToRight in loadout)
    ))
    """ Grand Promenade through Meeting Hall to Stair of Twilight """

    mezzanineShaft_withoutSpeedbooster = LogicShortcut(lambda loadout: (
        (SpaceJump in loadout) or
        ((
            (killRippers in loadout) or
            (Tricks.movement_zoast in loadout)
            # using movement_zoast to control speed of bomb jumping to not run into rippers
        ) and (canFly in loadout)) or
        ((HiJump in loadout) and (Tricks.wall_jump_precise in loadout)) or  # wall jump around 3 tiles
        (Ice in loadout) or
        ((Speedball in loadout) and (Tricks.sbj_wall in loadout))
    ))
    """ the reason for this is to figure whether energy is required for the shinespark up ruined concourse """

    mezzanineShaft = LogicShortcut(lambda loadout: (
        (SpeedBooster in loadout) or
        (SkyWorld.mezzanineShaft_withoutSpeedbooster in loadout)
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
                # TODO: test - I did this (no suits), but I had a few accel charges and damage amps.
                # Can it be done with no damage amp or accel charge?
            ))
        )
    ))

    anticipation = LogicShortcut(lambda loadout: (
        # this is mostly about exit logic, because it doesn't take anything to get into anticipation chamber
        (GravityBoots in loadout) and
        ((  # stair of dawn
            (Morph in loadout) and
            (pinkDoor in loadout)  # bottom of stair of dawn
        ) or (
            (Tricks.moonfall_clip in loadout)
        ) or (
            # get out by killing phantoon

            # first get to phantoon
            ((SkyWorld.killRidley in loadout) or (
                (can_bomb(1) in loadout) and
                (loadout.has_any(Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile))
            )) and
            (SkyWorld.killPhantoon in loadout) and

            # then get out
            (can_bomb(3) in loadout) and
            (SkyWorld.meetingHallToLeft in loadout)
        ))
    ))
    """ anticipation chamber to rail - hell run not included - gate to ridley not included """

    crackedCliffsideCave = LogicShortcut(lambda loadout: (
        (can_bomb(1) in loadout) or
        (Screw in loadout) or
        (
            (SpeedBooster in loadout) and

            # left to right
            (Tricks.short_charge_4 in loadout) and

            # right to left
            # get up to the 2nd platform holding shinespark charge
            (Tricks.movement_zoast in loadout) and
            ((HiJump in loadout) or (SpaceJump in loadout))
        )
    ))


class Early:
    cisternAccessTunnel = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        loadout.has_any(Speedball, Bombs, PowerBomb, Tricks.movement_moderate)
        # speedball or fast morph helps you follow your bullet to the shotblock
    ))
    """ Cistern Access Tunnel with a shot block in it """

    causeway = LogicShortcut(lambda loadout: (
        (
            (SpeedBooster in loadout)
        ) or (
            (can_bomb(2) in loadout) and
            ((Speedball in loadout) or (
                # This wave gate glitch seems a little bit harder than other, but still not hard
                ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
                ((GravitySuit in loadout) or (
                    (Tricks.crouch_or_downgrab in loadout) and
                    ((HiJump in loadout) or (Ice in loadout))
                ))
            ))
        ) or (
            # no bombs or speedbooster needed
            (GravitySuit in loadout) and
            (GravityBoots in loadout) and
            (Screw in loadout) and
            (Morph in loadout) and
            (
                (Speedball in loadout) or
                (shootThroughWalls in loadout) or
                (Tricks.wave_gate_glitch in loadout)
            ) and
            (
                (Tricks.morph_jump_3_tile in loadout) or
                (Speedball in loadout) or
                (can_bomb(1) in loadout)
            ) and

            # just left of the left switch
            (Tricks.clip_crouch in loadout)  # add a down press to the 1st clip, then up to get the second clip
        )
    ))

    concourseShinespark = LogicShortcut(lambda loadout: (
        (SpeedBooster in loadout) and
        # less than 180 is needed for this shinespark, (can be done with no energy tank)
        # but then you're very likely to need more health to shinespark in the next room (when it's not area rando)
        ((energy_req(180) in loadout) or (SkyWorld.mezzanineShaft_withoutSpeedbooster in loadout)) and
        (Morph in loadout)  # back down
    ))
    """ access to the top of ruined concourse """

    sporeFieldEntrance = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (
            (Tricks.morph_jump_3_tile_up_1 in loadout) or
            (Speedball in loadout) or
            (Bombs in loadout) or
            (PowerBomb in loadout)
        )
    ))
    """ through the small morph tunnel before entering spore field """


# TODO: SandLand location logic doesn't use these shortcuts as much as they should
class SandLand:
    """ not including any colored doors that are different colors in different directions """

    # Some SandLand logic shortcuts are chosen carefully to make a graph that can be connected at junctions
    # to make all the paths between Ocean Shore and Turbid Passage for the area logic.

    #                      * ocean shore
    #                     /
    #                  - *  green moon
    #         shaft  /   |
    #             - * -- *  canyon
    #           /        |
    #    lower * ---*--- *  sed floor
    #        /     sub    \
    #       *     crevice  * turbid passage
    # pile anchor

    oceanShoreTop = LogicShortcut(lambda loadout: (
        (
            (GravityBoots in loadout) and
            (
                loadout.has_all(Tricks.movement_moderate, Tricks.wall_jump_delayed) or
                (canFly in loadout) or
                (HiJump in loadout) or  # debating attaching a trick to this for the difficulty of the jumps
                (SpeedBooster in loadout)
            )
        ) or

        # Gravity boots are not required to get this.
        # The only difficulty is shooting the wall in the right place (when you'll fall quickly).
        ((SpeedBooster in loadout) and (Tricks.movement_moderate in loadout))
    ))
    """
    I wouldn't make a logic shortcut just for a single location.

    But if you can get to this item location,
    you can also get to the island between shore and shallows.
    (riding green platforms)
    """

    sedimentTunnel = LogicShortcut(lambda loadout: (
        loadout.has_all(GravitySuit, Morph, GravityBoots) and
        ((Speedball in loadout) or (Tricks.movement_zoast in loadout))
        # I don't know how Rusty and Joonie did this without speedball
    ))
    """ just from one side to the other - no door """

    lowerLowerToSubCrevice = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout)) and
        (  # bottom to Dark Hollow
            (GravitySuit in loadout) or
            ((HiJump in loadout) and (Tricks.crouch_precise in loadout)) or
            (Tricks.sbj_underwater_no_hjb in loadout) or
            (Tricks.freeze_hard in loadout)  # crab
            # not very hard, but easy to miss, then you have to look for another crab
        ) and
        (pinkDoor in loadout) and  # between submarine crevice and murky gallery
        (  # up from submarine crevice
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (
                    (Tricks.uwu_2_tile in loadout) or
                    ((Super in loadout) and (Tricks.freeze_hard in loadout)) or  # knock crab off wall and freeze
                    (Tricks.sbj_underwater_w_hjb in loadout)
                )
            )
        )
    ))
    """ bottom-right of sea caves lower hall to middle of submarine crevice """

    subCreviceToSedFloor = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout)) and
        (  # to not get stuck in sediment sand pits
            (GravitySuit in loadout) or
            (HiJump in loadout)
        ) and
        (Morph in loadout) and  # top of meandering passage
        (pinkDoor in loadout) and  # between submarine crevice and murky gallery
        (  # murky gallery
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Tricks.crouch_or_downgrab in loadout) and  # up from murky gallery
                (Tricks.movement_moderate in loadout)  # left from murky gallery
            )
        )
    ))
    """
    middle of submarine crevice to middle of sediment floor
    (not including door between sediment floor and meandering passage)
    """

    sedFloorToCanyon = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # between sediment floor and sediment canyon
        (  # to not get stuck in sand pit
            (GravitySuit in loadout) or
            (HiJump in loadout)
        )
    ))
    """ middle of sediment floor to bottom-left of sediment canyon """

    canyonToGreenMoon = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (
                    ((Tricks.uwu_2_tile in loadout) and (Tricks.crouch_precise in loadout)) or
                    (Tricks.freeze_hard in loadout) or
                    (Tricks.sbj_underwater_w_hjb in loadout)
                )
            )
        )
    ))
    """ bottom-left of sediment canyon to ocean shallows above green door """

    canyonToShaft = LogicShortcut(lambda loadout: (
        (Super in loadout) and  # door between Sediment Tunnel and Ocean Shallows
        (SandLand.sedimentTunnel in loadout)
    ))
    """ bottom-left of sediment canyon to sea cave shaft """

    shaftToGreenMoon = LogicShortcut(lambda loadout: (
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
    ))
    """ sea cave shaft to ocean shallows above green door """

    shaftToLowerLower = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # between shaft and sea cave narrows
        ((GravitySuit in loadout) or (HiJump in loadout) or (Tricks.sbj_underwater_no_hjb in loadout)) and
        # TODO: confirm springball jump can get you over narrows
        (pinkDoor in loadout) and  # between sea caves upper and sea caves lower
        (Morph in loadout) and  # passage right next to door in lower sea caves
        (  # top of lower hall, to bottom-right of lower hall
            ((GravitySuit in loadout) and (Screw in loadout)) or
            (
                (DarkVisor in loadout) and
                (Morph in loadout) and
                (
                    (Speedball in loadout) or
                    ((GravitySuit in loadout) and (can_bomb(1) in loadout))
                ) and

                # going up, shoot the switch through the wall, or use the shinespark path
                ((shootThroughWalls in loadout) or loadout.has_all(GravitySuit, SpeedBooster))
            )
            # joonie did the super sink into the visor switch tunnel
            # but with save states, and bob said he doesn't have a good setup for it
        ) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ))
    """ sea cave shaft to bottom-right of sea caves lower hall """

    eddy = LogicShortcut(lambda loadout: (
        (Morph in loadout) and
        (
            (Speedball in loadout) or
            (
                loadout.has_all(GravitySuit, Bombs, Tricks.movement_zoast)
                # Is this harder than movement_zoast? is it Tricks.bob?
                # Joonie did it after like 15 minutes of trying.
                # Azder made it look easy.
                # Azder gave up on doing it without bombs.
            )
        ) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ))
    """ get out of Eddy Channel """

    benthic = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and  # submarine crevice, in and out with nowhere to farm between
        (Super in loadout) and  # submarine crevice bottom left
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            # out of benthic shaft without aqua before the balls block you in
            (Tricks.movement_moderate in loadout) and
            # submarine crevice
            (loadout.has_any(Tricks.crouch_precise, Tricks.sbj_underwater_w_hjb, Tricks.uwu_2_tile))
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ))
    """ middle of submarine crevice to benthic cache """

    turbidToSedFloor = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            ((Tricks.movement_moderate in loadout) or (
                (Super in loadout) and
                (SandLand.eddy in loadout)
                # If no aqua suit, assume the player will fall into eddy channels
                # get out of eddy, and Supers to get back into Sediment Floor
            ))
        ))
    ))
    """ from turbid passage to the middle of sediment floor """

    directionalSedFloorToGreenMoonThroughSeaCaves = LogicShortcut(lambda loadout: (
        (pinkDoor in loadout) and  # door from sediment to meandering
        (SandLand.subCreviceToSedFloor in loadout) and
        (SandLand.lowerLowerToSubCrevice in loadout) and
        (SandLand.shaftToLowerLower in loadout) and
        (SandLand.shaftToGreenMoon in loadout)
    ))
    """ one-way sediment floor to green moon - because it's needed in a bunch of return logic """

    GreenMoonDown = LogicShortcut(lambda loadout: (
        (Super in loadout) or  # normal way
        (
            ((Tricks.moonfall_clip in loadout) or (underwaterSuperSink in loadout)) and
            (GravityBoots in loadout) and
            (  # get to the starting island
                (GravitySuit in loadout) or  # anything else needed with aqua? tricks?
                (SandLand.oceanShoreTop in loadout)
                # TODO: other ways to get up to the island?
            ) and
            ((Morph in loadout) or (GravitySuit in loadout)) and
            # without aqua, I couldn't do it without morph
            # I saw rusty do it with aqua, no morph
            # TODO: Can it be done with neither morph nor aqua?

            # and able to return back to above door
            (
                (can_use_pbs(1) in loadout) or  # yellow door up
                (
                    # this one redundant unless door changes color (doorcap rando)
                    (SandLand.canyonToShaft in loadout) and
                    (SandLand.shaftToGreenMoon in loadout)
                ) or
                (
                    (SandLand.sedFloorToCanyon in loadout) and
                    (SandLand.directionalSedFloorToGreenMoonThroughSeaCaves in loadout)
                )
            )
        )
    ))
    """
    directional - go down through the green door in ocean shallows to sediment canyon

    and able to return
    """


class ServiceSector:
    wasteProcessingTraverse = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (
            ((HiJump in loadout) and (Ice in loadout) and (Tricks.wall_jump_precise in loadout)) or
            (Tricks.sbj_w_hjb in loadout) or
            ((SpaceJump in loadout) and (
                loadout.has_any(SpaceJumpBoost, HiJump)
            )) or
            (SpeedBooster in loadout) or
            (Bombs in loadout)
            # TODO: ice with sbj (no hjb)?
        )
    ))
    """ traverse from one door of waste processing to the other (not including colored door) """

    crumblingBasement = LogicShortcut(lambda loadout: (
        # This is useless, because there's no where else you can go without Gravity Boots.
        # But here it is.
        ((GravityBoots in loadout) or (SpeedBooster in loadout)) and

        (
            (can_bomb(1) in loadout) or
            (  # can use Screw to get down, but need something special to get up
                (Screw in loadout) and
                ((Tricks.morphless_tunnel_crawl in loadout) or (SpeedBooster in loadout))
            )
        ) and  # can screw down, but not up
        (
            (Tricks.super_sink_easy in loadout) or
            (shootThroughWalls in loadout)
        )
    ))
    """ between top-left and bottom (not to eribium) """

    eastSpore = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # between field access and field
        (can_bomb(1) in loadout) and
        ((DarkVisor in loadout) or (Tricks.dark_easy in loadout))
    ))
    """ east spore field access to crumbling basement top-left """

    westSpore = LogicShortcut(lambda loadout: (
        loadout.has_any(shootThroughWalls, Tricks.wave_gate_glitch)
    ))

    cellar = LogicShortcut(lambda loadout: (
        # If you fall in the water with nothing, it's a tight jump to get out.
        # But if you don't want to do that tight jump, then don't fall in the water.
        # It's not worth putting in logic that something is required when it's not required,
        # just for the case that someone falls in the water without it.
        (GravityBoots in loadout) and
        (Tricks.dark_easy in loadout) and
        (can_bomb(1) in loadout)
    ))

    transfer = LogicShortcut(lambda loadout: (
        # can get down with super sink and no dark visor, but not back up
        loadout.has_all(GravityBoots, DarkVisor, can_bomb(1))
    ))
    """ transfer station - not including shoot through walls, because that's only required in 1 direction """


# TODO: use more of these in location logic where relevant
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
                (Screw in loadout) and (GravitySuit in loadout)  # need aqua to come up through this hole with screw
            ))
        )) and
        (
            (GravitySuit in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout) or
            (Tricks.sbj_underwater_w_hjb in loadout) or
            ((HiJump in loadout) and (Ice in loadout)) or
            (loadout.has_all(Ice, Tricks.crouch_or_downgrab))  # and uwu 1-tile wide
        )
    ))
    """ traverse "Hot Spring" between Sporous Nook and Verdite Mines (including Verdite Mines Entrance) """

    # TODO: all the places where we only check for this and sporous nook should also check from raging pit
    # because it could require less energy if we have PBs
    fieryTrail = LogicShortcut(lambda loadout: (
        (varia_or_hell_run(550, heat_and_metroid_suit_not_required=True) in loadout)
        # TODO: a different amount if I have screw and space jump and shootThroughWalls
    ))
    """ fiery gallery and burning trail """

    pit = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        # you can super-sink to get down without morph, but I don't see a way to get back up
        # can't xray climb right wall because of some empty tiles in the same column as the door
        # TODO: check morphless tunnel crawl with screw?
        (Morph in loadout) and
        ((can_bomb(1) in loadout) or (Screw in loadout)) and  # shaktools won't do all of the work
        (
            # TODO: measure hell run with super sink no pbs
            (varia_or_hell_run(1120, heat_and_metroid_suit_not_required=True) in loadout) or
            (  # faster with pbs
                (can_use_pbs(5) in loadout) and
                # 5 pbs is to include the PB door that might be needed to go into verdite mines
                (varia_or_hell_run(320, heat_and_metroid_suit_not_required=True) in loadout)
            )
        )
    ))
    """ through raging pit and raging pit access """

    beta = LogicShortcut(lambda loadout: (
        # something to avoid taking damage from the
        # lava at the bottom of mining site beta during hell run
        loadout.has_any(Speedball, Varia, MetroidSuit, Tricks.mockball_hard, energy_req(1050)) and

        (GravityBoots in loadout) and
        # 4 pbs - beta, lava pool, vulnar elevator, placid pool
        (can_bomb(4) in loadout) and  # lava pool and mining site (lava pool could be screw, but not mining site)
        (
            (varia_or_hell_run(937, heat_and_metroid_suit_not_required=True) in loadout) or
            (
                (can_use_pbs(4) in loadout) and
                (varia_or_hell_run(523, heat_and_metroid_suit_not_required=True) in loadout)
            )
        )
        # the hell run to hollow chamber is about the same as the hell run going up the elevator
        # so this hell run will work for both
    ))
    """ through mining site beta and lava pool (hell run up elevator) """

    hollow = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        (icePod in loadout) and
        (varia_or_hell_run(346, heat_and_metroid_suit_not_required=True) in loadout)
    ))
    """ traverse hollow chamber - hell run includes elevator """

    placid = LogicShortcut(lambda loadout: (
        ((can_bomb(2) in loadout) or (Screw in loadout) or (SpeedBooster in loadout)) and  # wall by elevator
        ((icePod in loadout) or (
            (can_use_pbs(2) in loadout) and
            (
                (GravitySuit in loadout) or
                ((HiJump in loadout) and (Tricks.crouch_or_downgrab in loadout))
                # hint: for hi jump, lay power bomb on the second tile away from the power bomb blocks
            )
        ))
    ))
    """ through placid pool to elevator """


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
        (Tricks.sbj_underwater_w_hjb in loadout) or
        # joonie gave up on trying to get out with SBJ no HJB, he wondered if bob could do it
        ((Tricks.uwu_2_tile in loadout) and (HiJump in loadout))
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
            ((Super in loadout) and (
                (Morph in loadout) or
                (MetroidSuit in loadout) or
                (Tricks.morphless_tunnel_crawl in loadout)

                # TODO: should we separate turnaround cancel from the crawl that can go both ways?
                # This can be done with just the turnaround cancel if super_sink_easy is used to go down.
                # ((Tricks.morphless_tunnel_crawl in loadout) and (Tricks.super_sink_easy in loadout))
            ))
        )
    ))
    """ from west corridor to the top of central corridor (not through screw to go lower) """

    centralCorridorWater = LogicShortcut(lambda loadout: (
        ((
            (Tricks.movement_zoast in loadout)  # gravity jump through door
            # https://vimeo.com/user130979419
            # (not gravity jump trick because that requires gravity suit)
        ) or (
            (GravitySuit in loadout)
        ) or (
            (Ice in loadout)  # freeze atomic
        ) or (
            # high jump gets you high enough to wall jump
            (HiJump in loadout) and
            ((Tricks.wall_jump_precise in loadout) or (Tricks.uwu_2_tile_surface in loadout))
        ))
        # TODO: can springball jump get me out?
    ))
    """ get out of the water in central corridor """

    eastCorridor = LogicShortcut(lambda loadout: (
        # only morph needed to go down
        (Morph in loadout) and

        # go up
        ((
            (  # 4 tile morph jump
                (Bombs in loadout) or
                (Speedball in loadout) or
                (Tricks.morph_jump_4_tile in loadout)
            ) and
            (  # open the shot block from below
                ((Tricks.movement_moderate in loadout) and (electricHyper in loadout)) or
                (can_bomb(1) in loadout) or
                (shootThroughWalls in loadout) or
                (Spazer in loadout)
            )
        ) or (
            (Tricks.xray_climb in loadout)
        ))
    ))
    """ top of East Corridor to get to Foyer """

    cenote = LogicShortcut(lambda loadout: (
        (Grapple in loadout) and
        (SpeedBooster in loadout) and
        (Morph in loadout) and
        (Speedball in loadout) and
        (can_use_pbs(1) in loadout)
    ))
    """ use the cenote passage into pirate lab (not past the item) """


class LifeTemple:
    # TODO: use this in relevant location logic
    waterToVeranda = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((  # bottom of chamber of life
            (
                ((can_bomb(1) in loadout) and (Tricks.movement_moderate in loadout)) or
                (can_bomb(2) in loadout) or
                (loadout.has_all(Morph, Screw))
                # can't break blocks with screw going down, but easy to go down in chamber of stone
            ) and
            (
                (Tricks.movement_moderate in loadout) or
                loadout.has_all(HiJump, Speedball)
            )
        ) or (  # left-middle of chamber of stone
            ((HiJump in loadout) and (
                (Tricks.wall_jump_precise in loadout) or
                (SpeedBooster in loadout)
            )) or
            loadout.has_any(canFly, Tricks.freeze_hard) or
            loadout.has_all(Tricks.short_charge_4, Tricks.movement_zoast)  # stutter
        ))
    ))
    """ bottom of chamber of stone to bottom of veranda (top of chamber of stone) """

    waterGardenBottom = LogicShortcut(lambda loadout: (
        ((GravitySuit in loadout) or (Ice in loadout) or (Tricks.sbj_underwater_w_hjb in loadout)) and
        # There's a hole above the door that prevents xray climbing up.
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
        )) and
        (
            ((SpeedBooster in loadout) and (LifeTemple.waterToVeranda in loadout)) or  # top door
            (HiJump in loadout) or
            (Tricks.wall_jump_precise in loadout) or  # around 2-tile ledge with no hjb
            ((SpaceJump in loadout) and (SpaceJumpBoost in loadout)) or
            (loadout.has_all(Morph, Bombs) and loadout.has_any(GravitySuit, Tricks.movement_moderate))
            # have to start bomb jump mid-air if no aqua
        )
    ))
    """ get into chamber of stone from wellspring access """

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
        ) or (
            # but you're not softlocked with super-sink
            (Tricks.super_sink_easy in loadout)
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
        # tried to avoid bomb blocks with super sink and xray climb, but something stopped xray climb
    ))
    """ between Norak Perimeter bottom left and main area of norak perimeter """

    veranda = LogicShortcut(lambda loadout: (
        ((  # bottom to top
            (Tricks.short_charge_3 in loadout)
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
    """ sequestered inferno to the bottom of hive crossways """

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
        ) or (
            (Tricks.xray_climb in loadout)
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
        (pinkDoor in loadout) and  # between hive entrance and elevator
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

    This is contained in courtyardToCollapsed

    doesn't include hell runs, because that will need to be measured separately to wherever you're going
    """

    courtyardToCollapsed = LogicShortcut(lambda loadout: (
        (FireHive.ancientBasinAccess in loadout) and
        (  # ripper above fire temple courtyard door makes it hard to hell run
            (Varia in loadout) or
            (killRippers in loadout) or
            (HiJump in loadout) or
            (SpaceJump in loadout) or
            (Tricks.movement_moderate in loadout)
        ) and
        (GravityBoots in loadout) and
        # collapsed passage to fire temple courtyard
        (varia_or_hell_run(850, heat_and_metroid_suit_not_required=True) in loadout)
        # TODO: patience or more energy, because farming in fire temple courtyard would be really slow
    ))
    """ Fire Temple Courtyard to Collapsed Passage (no doors included because it depends on direction) """

    hiveBurrow = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        # hard requires super sink to be able to go both ways
        (bonkCeilingSuperSink in loadout) and
        (Grapple in loadout) and
        (Varia in loadout) and
        (Morph in loadout) and
        (
            (Tricks.morph_jump_3_tile in loadout) or
            (Speedball in loadout) or
            (can_bomb(1) in loadout)
        ) and
        ((MetroidSuit in loadout) or (energy_req(hell_run_energy(550, loadout)) in loadout))

        # I started trying to figure out what this would take without varia,
        # but that's just not going to be useful, because in non-area rando,
        # there's another big heated room on the other side of this area door.
        # And there's also the complexity of whether I can get to the farm in crossways.
        # So I'm just saying no hell runs through this passage.
    ))
    """ hive burrow left door to infested passage (varia and super sink required) """


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
    """ includes metroid suit for laser right outside left door """

    thermalResBeta = LogicShortcut(lambda loadout: (
        ((GravitySuit in loadout) or (
            (Tricks.freeze_hard in loadout) and
            (Ice in loadout) and
            ((Tricks.movement_zoast in loadout) or (HiJump in loadout)) and
            (can_bomb(1) in loadout)
        )) and
        (varia_or_hell_run(80) in loadout)  # cold room
    ))

    thermalResGamma = LogicShortcut(lambda loadout: (
        (GravityBoots in loadout) and
        ((plasmaWaveGate in loadout) or (Tricks.plasma_gate_glitch in loadout)) and
        ((
            # Subversion's full halfie
            # can shinespark across both ways,
            # but getting the right height (from the left) is tricky
            (killYellowPirates in loadout) and
            (Tricks.short_charge_3 in loadout) and
            (Tricks.movement_zoast in loadout) and
            (varia_or_hell_run(289) in loadout) and
            (energy_req(142) in loadout)
        ) or (
            ((varia_or_hell_run(318) in loadout) and (Tricks.wall_jump_precise in loadout)) or
            (varia_or_hell_run(529) in loadout)
        ))
    ))
    """ top left of Magma Pump to middle of Reservoir Maintenance Tunnel (includes plasma+wave gate) """

    intakePump = LogicShortcut(lambda loadout: (
        # TODO: super sink and xray climb up and down thermal res beta
        (Geothermal.thermalResBeta in loadout) and
        (
            (GravitySuit in loadout) or
            loadout.has_all(HiJump, Tricks.freeze_hard, Tricks.movement_moderate)  # uwu 1 tile wide
        ) and
        (can_use_pbs(2) in loadout) and
        (varia_or_hell_run(150) in loadout) and
        (
            ((MetroidSuit in loadout) and (energy_req(250) in loadout)) or
            ((Screw in loadout) and (breakIce in loadout))
        )
    ))
    """ including thermalResBeta """


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
        # TODO: can hell run with hypercharge, or lots of beams and damage amps, or a billion supers,
        # or patience and varia+missiles
    ))

    killDraygon = LogicShortcut(lambda loadout: (
        ((GravitySuit in loadout) or (
            (Tricks.movement_moderate in loadout) and (energy_req(850) in loadout)
        ) or (
            (Tricks.movement_zoast in loadout) and (energy_req(161) in loadout)
        ) or (
            # hypercharge makes up for not having aqua
            (Charge in loadout) and
            (Hypercharge in loadout)
        )) and
        ((energy_req(850) in loadout) or (
            (Tricks.movement_moderate in loadout) and
            (energy_req(450) in loadout)
        ) or (
            (Tricks.movement_zoast in loadout)
        ))
        # TODO: improve this logic
    ))


class SpacePort:
    spaceportTopFromElevator = LogicShortcut(lambda loadout: (
        (Grapple in loadout) or
        (can_crash_spaceport in loadout)
        # TODO: if I get up with xray, or (ice and super), then i can get back down with moonfall
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
