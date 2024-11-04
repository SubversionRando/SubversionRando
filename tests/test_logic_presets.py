import random

from subversion_rando import logic_presets
from subversion_rando.logic_presets import custom_logic_str_from_tricks, custom_logic_tricks_from_str
from subversion_rando.trick_data import Tricks, trick_name_lookup


def test_custom_logic_str() -> None:
    empty_trick_str = custom_logic_str_from_tricks(frozenset())
    assert empty_trick_str == "000000000000", f"empty: {empty_trick_str}"

    for _ in range(10):
        l_int = random.randrange(0x1000_0000_0000, 0x1_0000_0000_0000)
        l_int &= 0xffff_ffff_fff0
        l_str = hex(l_int)[2:]
        l_t = custom_logic_tricks_from_str(l_str)
        # print(l_str)
        # pprint([trick_name_lookup[t] for t in l_t])
        assert l_str == custom_logic_str_from_tricks(l_t)

    # print(custom_logic_str_from_tricks(frozenset()))


def test_specific_set() -> None:
    # just some random set to see if something changes
    test_str = "3b0489a4fbb0"
    test_set = frozenset([
        Tricks.uwu_2_tile,
        Tricks.crouch_precise,
        Tricks.ice_clip,
        Tricks.spazer_into_lower_pirate_lab,
        Tricks.sbj_w_hjb,
        Tricks.crumble_jump,
        Tricks.wave_gate_glitch,
        Tricks.xray_climb,
        Tricks.uwu_2_tile_surface,
        Tricks.short_charge_2,
        Tricks.searing_gate_tricks,
        Tricks.short_charge_4,
        Tricks.super_sink_easy,
        Tricks.movement_zoast,
        Tricks.crouch_or_downgrab,
        Tricks.patience,
        Tricks.sbj_underwater_w_hjb,
        Tricks.morph_jump_4_tile,
        Tricks.dark_medium,
        Tricks.short_charge_3,
        Tricks.sbj_no_hjb,
        Tricks.super_sink_hard
    ])
    assert custom_logic_str_from_tricks(test_set) == test_str
    assert custom_logic_tricks_from_str(test_str) == test_set


def test_str_2_tricks_reference() -> None:
    for mask_str, t in logic_presets.mask_2_trick.items():
        fs = frozenset([t])
        assert custom_logic_str_from_tricks(fs) == mask_str, f"{trick_name_lookup[t]} {mask_str}"
        assert custom_logic_tricks_from_str(mask_str) == fs, f"{mask_str} {trick_name_lookup[t]}"


if __name__ == "__main__":
    test_custom_logic_str()
    test_str_2_tricks_reference()
    test_specific_set()
