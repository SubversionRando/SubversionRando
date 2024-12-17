# pyscript entry point

import json
from typing import Any, Literal, Optional, TypedDict

from pyscript import document  # type: ignore
# pyscript library
import js  # type: ignore

from subversion_rando.game import CypherItems, Game, GameOptions
from subversion_rando.item_marker import ItemMarkersOption
from subversion_rando.logic_presets import casual, expert, medium, custom_logic_str_from_tricks
from subversion_rando.romWriter import RomWriter
from subversion_rando.trick import Trick
from subversion_rando.trick_data import Tricks, trick_name_lookup, tricks_from_names
from subversion_rando.main_generation import generate, get_spoiler, write_rom

document: Any = document  # TODO: type stubs
js: Any = js


def populate_tricks() -> None:
    table_rows: list[str] = []
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick):
            html = (
                f'<tr><td><input type="checkbox" id="{trick_name}"/></td>'
                f'<td><label for="{trick_name}">{trick_name}</label></td>'
                f'<td><span>{trick.desc}</span></td></tr>'
            )
            table_rows.append(html)
    tricks_element = document.querySelector("#tricks")
    tricks_element.innerHTML = "<tbody>" + ("".join(table_rows)) + "</tbody>"


def make_presets() -> list[tuple[str, list[str]]]:
    tr: list[tuple[str, list[str]]] = [
        ("casual", [trick_name_lookup[t] for t in casual]),
        ("medium", [trick_name_lookup[t] for t in medium]),
        ("expert", [trick_name_lookup[t] for t in expert]),
    ]
    return tr


def populate_presets() -> None:
    preset_data = make_presets()
    js.populate_presets(preset_data)


class WebParams(TypedDict):
    area_rando: bool
    small_spaceport: bool
    escape_shortcuts: bool
    fill: Literal["D", "B", "MM"]
    cypher: str
    tricks: list[str]
    daphne_gate: bool
    item_markers: Literal["Simple", "ThreeTiered"]
    objective_rando: int
    skip_crash_space_port: bool


# the roll process is divided up to make the ui more responsive,
# because there's no way to run it asynchronously in js
# https://github.com/pyscript/pyscript/discussions/1406

# global state between roll functions
rom_writer: Optional[RomWriter] = None
options: Optional[GameOptions] = None
game: Optional[Game] = None


def roll1() -> bool:
    global rom_writer
    try:
        base64_data = js.rom_data
    except AttributeError:
        base64_data = ""

    if len(base64_data) == 0:
        print("no rom loaded")
        return False

    rom_writer = RomWriter.fromBase64(base64_data)
    return True


def roll2(params_str: str) -> None:
    global options
    print(params_str)
    params: WebParams = json.loads(params_str)

    tricks = tricks_from_names(params["tricks"])

    # romWriter = RomWriter.fromBlankIps()  # TODO
    options = GameOptions(tricks,
                          bool(params["area_rando"]),
                          params["fill"],
                          bool(params["small_spaceport"]),
                          bool(params["escape_shortcuts"]),
                          getattr(CypherItems, params["cypher"]),
                          bool(params["daphne_gate"]),
                          getattr(ItemMarkersOption, params["item_markers"]),
                          int(params["objective_rando"]),
                          bool(params["skip_crash_space_port"]))
    print(options)


def roll3() -> bool:
    global game
    assert options
    game = generate(options)
    return not (game.hint_data is None)


def roll4() -> None:
    # see if hint_data is None to know if it failed
    if rom_writer and game and game.hint_data:
        rom_name = write_rom(game, rom_writer)
        js.modified_rom_data = rom_writer.getBase64RomData().decode()
        js.rom_name = rom_name

        js.spoiler_text = get_spoiler(game)
    else:
        js.modified_rom_data = ""


populate_tricks()
populate_presets()


def get_logic_str(trick_names: list[str]) -> str:
    tricks: frozenset[Trick] = frozenset([getattr(Tricks, trick_name) for trick_name in trick_names])
    return custom_logic_str_from_tricks(tricks)


js.python_get_logic_str = get_logic_str
js.python_roll1_function = roll1
js.python_roll2_function = roll2
js.python_roll3_function = roll3
js.python_roll4_function = roll4
