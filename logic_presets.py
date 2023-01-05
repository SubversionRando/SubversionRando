from trick import Trick
from trick_data import Tricks


casual: frozenset[Trick] = frozenset()  # empty

medium = frozenset([
    Tricks.crouch_or_downgrab,
    Tricks.dark_easy,
    Tricks.dark_medium,
    Tricks.ggg,
    Tricks.gravity_jump,
    Tricks.hell_run_easy,
    Tricks.hell_run_medium,
    Tricks.wall_jump_precise,
    Tricks.morph_jump_3_tile_water,
    Tricks.morph_jump_4_tile,
    Tricks.movement_moderate,
    Tricks.short_charge_2,
    Tricks.wave_gate_glitch,
])

expert = frozenset(t for t in vars(Tricks).values() if isinstance(t, Trick))  # all

assert all(isinstance(t, Trick) for t in expert), f"{list(expert)}"
