# pyscript entry point

import json
from typing import Any, Literal, Optional, TypedDict

# pyscript library
import js  # type: ignore

from game import CypherItems, Game, GameOptions
from logic_presets import casual, expert, medium
from romWriter import RomWriter
from trick import Trick
from trick_data import Tricks, trick_name_lookup
from Main import generate, get_spoiler, write_rom

Element: Any  # pyscript built-in


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
    tricks_element = Element("tricks")  # noqa: F821
    tricks_element.element.innerHTML = "<tbody>" + ("".join(table_rows)) + "</tbody>"


def make_presets() -> list[tuple[str, list[str]]]:
    tr = [
        ("casual", [trick_name_lookup[t] for t in casual]),
        ("medium", [trick_name_lookup[t] for t in medium]),
        ("expert", [trick_name_lookup[t] for t in expert]),
    ]
    return tr


def populate_presets() -> None:
    preset_data = make_presets()
    js.populate_presets(preset_data)  # type: ignore


class WebParams(TypedDict):
    area_rando: bool
    small_spaceport: bool
    escape_shortcuts: bool
    fill: Literal["D", "B", "MM"]
    cypher: str
    tricks: list[str]
    daphne_gate: bool


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
        base64_data: str = js.rom_data  # type: ignore
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

    tricks: frozenset[Trick] = frozenset([getattr(Tricks, trick_name) for trick_name in params["tricks"]])

    # romWriter = RomWriter.fromBlankIps()  # TODO
    options = GameOptions(tricks,
                          bool(params["area_rando"]),
                          params["fill"],
                          bool(params["small_spaceport"]),
                          bool(params["escape_shortcuts"]),
                          getattr(CypherItems, params["cypher"]),
                          bool(params["daphne_gate"]))
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
