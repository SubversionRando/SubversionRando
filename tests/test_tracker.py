import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from location_data import pullCSV
import tracker
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
    assert t.loc_names_from_input("warrior shrine etank") == ["Warrior Shrine: Middle"]
    assert t.loc_names_from_input("briar bot") == ['Briar: Bottom']
    assert t.loc_names_from_input("briar top") == ["Briar: Top"]
    assert t.loc_names_from_input("archives right") == ["Archives: Front"]
    assert t.loc_names_from_input("archives left") == ["Archives: Back"]
    assert t.loc_names_from_input("sensor top") == ["Sensor Maintenance: Top"]
    assert t.loc_names_from_input("sensor bottom") == ["Sensor Maintenance: Bottom"]
    assert t.loc_names_from_input("docking port omega") == ["Docking Port 4"]
    assert t.loc_names_from_input("docking port o") == ["Docking Port 4"]
    assert t.loc_names_from_input("docking port 4") == ["Docking Port 4"]
    assert t.loc_names_from_input("docking port 3") == ["Docking Port 3"]
    assert t.loc_names_from_input("docking port gamma") == ["Docking Port 3"]
    assert t.loc_names_from_input("docking port g") == ["Docking Port 3"]
    assert t.loc_names_from_input("docking port y") == ["Docking Port 3"]
    assert t.loc_names_from_input("spore spawn") == ["Harmonic Growth Enhancer"]
    assert t.loc_names_from_input("spospo") == ["Harmonic Growth Enhancer"]
    assert t.loc_names_from_input("kraid") == ["Shrine Of The Penumbra"]
    assert t.loc_names_from_input("draygon") == ["Greater Inferno"]
    assert t.loc_names_from_input("mining site alpha") == ["Mining Site 1"]
    assert t.loc_names_from_input("mining site a") == ["Mining Site 1"]
    assert t.loc_names_from_input("armory cache beta") == ["Armory Cache 2"]
    assert t.loc_names_from_input("armory cache b") == ["Armory Cache 2"]
    assert t.loc_names_from_input("armory cache gamma") == ["Armory Cache 3"]
    assert t.loc_names_from_input("armory cache g") == ["Armory Cache 3"]
    assert t.loc_names_from_input("armory cache y") == ["Armory Cache 3"]
    assert t.loc_names_from_input("armory 2") == ["Armory Cache 2"]
    assert t.loc_names_from_input("armory 3") == ["Armory Cache 3"]
    assert t.loc_names_from_input("armory b") == ["Armory Cache 2"]
    assert t.loc_names_from_input("armory c") == ["Armory Cache 3"]
    assert t.loc_names_from_input("penumbra") == ["Shrine Of The Penumbra"]
    assert t.loc_names_from_input("fervor") == ["Shrine Of Fervor"]
    assert t.loc_names_from_input("animate spark") == ["Shrine Of The Animate Spark"]
    assert t.loc_names_from_input("animate") == ["Shrine Of The Animate Spark"]

    all_locations = pullCSV()
    for loc_name in all_locations:
        assert t.loc_names_from_input(("".join(loc_name.split(":"))).lower()) == [loc_name]


def test_alias_targets() -> None:
    """ make sure all the alias targets are location names """
    all_locations = pullCSV()
    aliases: dict[str, str] = getattr(tracker, "_name_aliases")
    for target in aliases.values():
        assert target in all_locations, f"{target} location name"
