# You can edit the "options" section of this file
# and then run it to generate a seed.
#
# You can make copies and name them anything you want
# for different sets of options.
#
# A logic line starting with "#" means that trick is NOT in logic.
#
# It's all case-sensitive. ("True" or "False", not "true" or "false")

from subversion_rando.game import CypherItems, GameOptions
from subversion_rando.main_generation import generate, write_rom, write_spoiler_file
from subversion_rando.trick_data import Tricks


options = GameOptions(
    logic=frozenset([
        Tricks.infinite_bomb_jump,
        # Tricks.sbj_underwater_no_hjb,
        # Tricks.sbj_underwater_w_hjb,
        # Tricks.sbj_no_hjb,
        # Tricks.sbj_w_hjb,
        # Tricks.sbj_wall,
        # Tricks.uwu_2_tile,
        # Tricks.uwu_2_tile_surface,
        Tricks.gravity_jump,
        # Tricks.hell_run_hard,
        Tricks.hell_run_medium,
        Tricks.hell_run_easy,
        Tricks.movement_moderate,
        # Tricks.movement_zoast,
        # Tricks.wall_jump_delayed,
        Tricks.wall_jump_precise,
        Tricks.crumble_jump,
        Tricks.mockball_hard,
        Tricks.morphless_tunnel_crawl,
        # Tricks.morph_jump_3_tile,
        # Tricks.morph_jump_4_tile,
        # Tricks.morph_jump_3_tile_up_1,
        Tricks.morph_jump_3_tile_water,
        Tricks.crouch_or_downgrab,
        Tricks.crouch_precise,
        Tricks.dark_easy,
        Tricks.dark_medium,
        Tricks.dark_hard,
        # Tricks.freeze_hard,
        Tricks.wave_gate_glitch,
        Tricks.ggg,
        Tricks.clip_crouch,
        Tricks.short_charge_2,
        # Tricks.short_charge_3,
        # Tricks.short_charge_4,
        Tricks.xray_climb,
        # Tricks.ice_clip,
        Tricks.moonfall_clip,
        Tricks.super_sink_easy,
        Tricks.super_sink_hard,
        # Tricks.patience,
        Tricks.plasma_gate_glitch,
        # Tricks.searing_gate_tricks,
        Tricks.spazer_into_lower_pirate_lab,
    ]),
    area_rando=False,
    fill_choice="B",  # "D" full random, "MM" major/minor, "B" major/minor bias
    small_spaceport=True,
    escape_shortcuts=True,
    cypher_items=CypherItems.SmallAmmo,  # SmallAmmo Anything NotRequired
    daphne_gate=True
)

game = generate(options)
rom_name = write_rom(game)
write_spoiler_file(game, rom_name)
