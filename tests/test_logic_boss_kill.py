from subversion_rando.item_data import Items
from subversion_rando.logic_boss_kill import BossKill
from subversion_rando.logic_presets import expert, medium

from utils import setup


def test_kraid_with_almost_nothing() -> None:
    """
    cheesy did it first try without speedball or aqua or space jump
    4 e tanks, hiJump, missiles
    """
    _game, loadout = setup(expert)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.HiJump)
    loadout.append(Items.Missile)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert BossKill.kraid in loadout

    _game, loadout = setup(medium)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.HiJump)
    loadout.append(Items.Missile)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert BossKill.kraid not in loadout

    _game, loadout = setup(expert)
    loadout.append(Items.GravityBoots)
    loadout.append(Items.Speedball)
    loadout.append(Items.Missile)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert BossKill.kraid not in loadout
