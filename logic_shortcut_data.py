from connection_data import area_doors
from item_data import items_unpackable
from logic_shortcut import LogicShortcut
from logicCommon import ammo_req, can_bomb, can_use_pbs
from trick_data import Tricks

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
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
missileBarrier = LogicShortcut(lambda loadout: (
    (missileDamage in loadout) or loadout.has_all(Charge, Hypercharge)
))
icePod = LogicShortcut(lambda loadout: (
    ((Ice in loadout) and (missileDamage in loadout)) or ((Charge in loadout) and (Hypercharge in loadout))
))

electricHyper = LogicShortcut(lambda loadout: (
    (MetroidSuit in loadout) or (
        (Charge in loadout) and
        (Hypercharge in loadout)
    )
))
""" hyper beam when electricity is available """

plasmaWaveGate = LogicShortcut(lambda loadout: (
    ((Plasma in loadout) and (Wave in loadout)) or
    ((Hypercharge in loadout) and (Charge in loadout))
))
""" the switches that are blocked by plasma+wave barriers """

hiJumpSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    (HiJump in loadout) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))
""" hi jump and not bonking ceiling """

bonkCeilingSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    ((Speedball in loadout) or (Tricks.movement_zoast in loadout)) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))

underwaterSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))
""" no bonk, no gravity suit, no hi jump """

killRippers = LogicShortcut(lambda loadout: (
    (Super in loadout) or
    (can_use_pbs(1) in loadout) or
    (Screw in loadout) or
    loadout.has_all(Charge, Hypercharge)
))
""" GET OUT OF MY WAY!! """

killGreenPirates = LogicShortcut(lambda loadout: (
    (missileDamage in loadout) or
    (Charge in loadout) or
    (Ice in loadout) or
    (Wave in loadout) or
    (Plasma in loadout) or
    (can_bomb(1) in loadout) or
    (Spazer in loadout) or
    (Screw in loadout)
))

killYellowPirates = LogicShortcut(lambda loadout: (
    (Charge in loadout) or
    (Missile in loadout) or
    ((Super in loadout) and (ammo_req(15) in loadout)) or
    (can_use_pbs(3) in loadout) or
    (Screw in loadout) or
    ((Morph in loadout) and (Bombs in loadout) and (Tricks.patience in loadout))
))

# game objectives

can_fall_from_spaceport = LogicShortcut(lambda loadout: (
    loadout.has_any(Morph, Missile, shootThroughWalls, Super, Tricks.wave_gate_glitch)
))

can_crash_spaceport = LogicShortcut(lambda loadout: (
    (
        (spaceDrop not in loadout) and
        (MetroidSuit in loadout) and
        (Super in loadout)
        # This is dangerous because it messes up ocean logic.
    ) or (
        (spaceDrop in loadout) and
        (MetroidSuit in loadout) and
        (Super in loadout) and
        (
            (Grapple in loadout) or
            ((Xray in loadout) and (Tricks.xray_climb in loadout)) or
            ((Ice in loadout) and (Tricks.freeze_hard in loadout) and (Tricks.ice_clip in loadout))  # and super
        ) and
        (area_doors["LoadingDockSecurityAreaL"] in loadout) and
        (GravityBoots in loadout)
    )
))

can_win = LogicShortcut(lambda loadout: (
    (can_crash_spaceport in loadout) and
    (area_doors["RockyRidgeTrailL"] in loadout) and
    (GravityBoots in loadout) and
    (Screw in loadout) and
    (pinkDoor in loadout) and  # top entrance to MB
    (can_use_pbs(1) in loadout) and  # to enter detonator room
    # 1 because there's an enemy in the room where you need 2 pbs, that normally drops 10 ammo

    # This next part for leaving the detonator room
    # TODO: add tricks
    # (aqua suit because of the acid that starts rising up)
    # (4 PBs is mostly for getting out after MB2, but also
    # because there was no opportunity to refill after the last one you used to get in)
    ((Speedball in loadout) or (GravitySuit in loadout) or (can_bomb(4) in loadout)) and
    # MB1, zebs, and glass (separate from pinkDoor to prepare for door cap rando)
    (missileDamage in loadout) and
    # kill MB 2
    (
        # all the different ways to do damage
        (
            (Missile in loadout) and
            (ammo_req(385) in loadout)  # these numbers padded for the PB logic getting in and out
        ) or (
            (electricHyper in loadout)
        ) or (
            (Charge in loadout)
        )
    ) and
    # back to ship
    ((area_doors["SunkenNestL"] in loadout) or (area_doors["CraterR"] in loadout))
    # TODO: this isn't enough for back to ship because some doors are grey
    # (non area rando needs speedbooster or super sink)
))
""" detonate daphne and get back to the ship """
