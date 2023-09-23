from .connection_data import area_doors
from .item_data import Items
from .logicCommon import ammo_req, can_bomb, can_use_pbs
from .logic_shortcut import LogicShortcut
from .logic_shortcut_data import can_crash_spaceport, electricHyper, missileDamage, pinkDoor
from .trick_data import Tricks

can_win = LogicShortcut(lambda loadout: (
    (
        (loadout.game.options.skip_crash_space_port) or
        (can_crash_spaceport in loadout)
    ) and
    (area_doors["RockyRidgeTrailL"] in loadout) and
    (Items.GravityBoots in loadout) and
    (Items.Morph in loadout) and
    (loadout.game.daphne_blocks.logic in loadout) and
    (can_bomb(2) in loadout) and  # wrecked main engineering (2 for exit)
    (pinkDoor in loadout) and  # top entrance to MB
    (  # to enter detonator room
        (loadout.game.options.skip_crash_space_port) or
        # skip_crash_space_port option removes the PB requirement
        (can_use_pbs(1) in loadout)
        # 1 because there's an enemy in the room where you need 2 pbs, that normally drops 10 ammo
    ) and

    # This next part for leaving the detonator room

    # to deal with the acid that starts rising up
    (loadout.has_any(Items.Aqua, Tricks.movement_moderate, can_use_pbs(4), Items.Speedball)) and

    # 2-tile space morph jump if you can't power bomb
    # (4 PBs is mostly for getting out after MB2, but also
    # because there was no opportunity to refill after the last one you used to get in)
    ((Items.Speedball in loadout) or (can_bomb(4) in loadout)) and

    # MB1, zebs, and glass (separate from pinkDoor to prepare for door cap rando)
    (missileDamage in loadout) and
    # kill MB 2
    (
        # all the different ways to do damage
        (
            (Items.Missile in loadout) and
            (ammo_req(385) in loadout)
            # these numbers padded for the PB logic getting in and out
            # 330 missiles is what it takes
        ) or (
            (electricHyper in loadout)
        ) or (
            (Items.Charge in loadout)
        )
    ) and
    # We don't want new players getting stuck behind the laser with no Metroid Suit.
    # So doing it without Metroid Suit requires something around expert logic.
    (loadout.has_any(Items.MetroidSuit, Tricks.movement_zoast)) and
    # back to ship
    ((area_doors["SunkenNestL"] in loadout) or (area_doors["CraterR"] in loadout))
    # TODO: this isn't enough for back to ship because some doors are grey
    # (non area rando needs speedbooster or super sink)
))
""" detonate daphne and get back to the ship """
