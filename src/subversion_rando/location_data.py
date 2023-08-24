import csv
from typing import Optional, TypedDict, cast

from item_data import Item


# other unused columns in Location:
# "roomid", "area", "xy","plmtypename","state","roomname","alternateroomid"
class Location(TypedDict):
    fullitemname: str
    locids: list[int]
    plmtypeid: int
    plmparamhi: int
    plmparamlo: int
    hiddenness: str
    alternateroomlocids: list[int]
    alternateroomdifferenthiddenness: str
    inlogic: bool
    item: Optional[Item]


spacePortLocs = ["Ready Room",
                 "Torpedo Bay",
                 "Extract Storage",
                 "Gantry",
                 "Docking Port 4",
                 "Docking Port 3",
                 "Weapon Locker",
                 "Aft Battery",
                 "Forward Battery"]


majorLocs = frozenset([
    "Ocean Vent Supply Depot",
    "Sandy Cache",
    "Shrine Of The Penumbra",
    "Subterranean Burrow",
    "Archives: Front",
    "Arena",
    "Grand Vault",
    "Harmonic Growth Enhancer",
    "West Spore Field",
    "Electromechanical Engine",
    "Fire's Bane Shrine",
    "Greater Inferno",
    "Magma Chamber",
    "Antelier",
    "Chamber Of Wind",
    "Crocomire's Lair",
    "Equipment Locker",
    "Weapon Research",
    "Armory Cache 2",
    "Syzygy Observatorium",
    "Shrine Of The Animate Spark",
    "Extract Storage",
    "Torpedo Bay",
])

eTankLocs = frozenset([
    "Sandy Burrow: Top",
    "Sediment Flow",
    "Epiphreatic Crag",
    "Mezzanine Concourse",
    "Sensor Maintenance: Top",
    "Trophobiotic Chamber",
    "Vulnar Caves Entrance",
    "Warrior Shrine: Middle",
    "Depressurization Valve",
    "Gymnasium",
    "Mining Cache",
    "Containment Area",
    "Water Garden",
    "Reliquary Access",
    "Summit Landing",
    "Ready Room"
])


def pullCSV() -> dict[str, Location]:
    csvdict: dict[str, Location] = {}

    def commentfilter(line: str) -> bool:
        return (line[0] != '#')

    with open('subversiondata12.csv', 'r') as csvfile:
        reader = csv.DictReader(filter(commentfilter, csvfile))
        for row in reader:
            # commas within fields -> array
            row['locids'] = row['locids'].split(',')
            row['alternateroomlocids'] = row['alternateroomlocids'].split(',')
            # hex fields we want to use -> int
            row['locids'] = [int(locstr, 16)
                             for locstr in row['locids'] if locstr != '']
            row['alternateroomlocids'] = [
                int(locstr, 16) for locstr in row['alternateroomlocids'] if locstr != '']
            row['plmtypeid'] = int(row['plmtypeid'], 16)
            row['plmparamhi'] = int(row['plmparamhi'], 16)
            row['plmparamlo'] = int(row['plmparamlo'], 16)
            # new key: 'inlogic'
            row['inlogic'] = False
            # the item that we place in this location
            row["item"] = None
            csvdict[row['fullitemname']] = cast(Location, row)
    return csvdict
