import csv
import pathlib
from typing import IO, Optional, TypedDict, cast

from .item_data import Item


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
    alternateplmparamlo: Optional[int]
    inlogic: bool
    item: Optional[Item]


def get_location_ids(loc: Location) -> list[int]:
    sv_loc_ids = [loc["plmparamlo"]]
    alt_id = loc["alternateplmparamlo"]
    if alt_id:
        # There is a plmparamlo 0, but none of the alternates are 0
        # so we can say `if loc['alternateplmparamlo']`
        sv_loc_ids.append(alt_id)
    return sv_loc_ids


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


def pullCSV(csv_file: Optional[IO[str]] = None) -> dict[str, Location]:
    locations: dict[str, Location] = {}

    def comment_filter(line: str) -> bool:
        return (line[0] != '#')

    file: IO[str]
    if not csv_file:
        path = pathlib.Path(__file__).parent.resolve()
        file = open(path.joinpath('subversiondata12.csv'), 'r')
    else:
        file = csv_file

    with file as csv_f:
        reader = csv.DictReader(filter(comment_filter, csv_f))
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
            if len(row['alternateplmparamlo']):
                row['alternateplmparamlo'] = int(row['alternateplmparamlo'], 16)
            else:
                # There is a plmparamlo 0, but none of the alternates are 0
                # so we can say `if loc['alternateplmparamlo']`
                row['alternateplmparamlo'] = None
            # new key: 'inlogic'
            row['inlogic'] = False
            # the item that we place in this location
            row["item"] = None
            locations[row['fullitemname']] = cast(Location, row)
    return locations
