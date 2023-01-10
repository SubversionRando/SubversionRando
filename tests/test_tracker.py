import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from tracker import Tracker


def test_loc_names_from_input() -> None:
    t = Tracker()

    assert len(t.loc_names_from_input("benthic")) == 2  # cache and cache access
    assert t.loc_names_from_input("benthic access") == ['Benthic Cache Access']
    assert len(t.loc_names_from_input("briar")) == 2
    assert t.loc_names_from_input("briar ammo") == ['Briar: Bottom']
    assert len(t.loc_names_from_input("shrine")) == 3
    assert t.loc_names_from_input("shrine fervor") == ['Shrine Of Fervor']
    assert t.loc_names_from_input("tower") == ['Tower Rock Lookout']
    assert t.loc_names_from_input("antilere") == ['Antelier']
    assert len(t.loc_names_from_input("armory cache")) == 2
    assert t.loc_names_from_input("benthic cache") == ["Benthic Cache"]
    assert len(t.loc_names_from_input("weapon")) == 2

    # commands
    assert len(t.loc_names_from_input("List")) == 0
    assert len(t.loc_names_from_input("undo")) == 0
    assert len(t.loc_names_from_input("exit")) == 0
    assert len(t.loc_names_from_input("q et")) == 0

    # aliases
    assert t.loc_names_from_input("warrior shrine top") == ["Warrior Shrine: Top"]
    assert t.loc_names_from_input("warrior shrine bottom") == ["Warrior Shrine: Bottom"]
    assert t.loc_names_from_input("warrior shrine mid") == ["Warrior Shrine: Middle"]
    assert t.loc_names_from_input("briar bot") == ['Briar: Bottom']
    assert t.loc_names_from_input("briar top") == ["Briar: Top"]
