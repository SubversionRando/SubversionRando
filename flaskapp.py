import sys
from typing import TypedDict
import flask

import Main
from game import CypherItems, GameOptions
import logic_presets
from romWriter import RomWriter
from trick import Trick
from trick_data import Tricks, trick_name_lookup

app = flask.Flask(__name__)


def make_tricks_response() -> list[tuple[str, str]]:
    tr: list[tuple[str, str]] = []
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick):
            tr.append((trick_name, trick.desc))
    return tr


tricks_response = make_tricks_response()


def make_presets_response() -> list[tuple[str, list[str]]]:
    tr = [
        ("casual", [trick_name_lookup[t] for t in logic_presets.casual]),
        ("medium", [trick_name_lookup[t] for t in logic_presets.medium]),
        ("expert", [trick_name_lookup[t] for t in logic_presets.expert]),
    ]
    return tr


presets_response = make_presets_response()


class WebParams(TypedDict):
    area_rando: bool
    small_spaceport: bool
    escape_shortcuts: bool
    mmb: bool
    cypher: str
    tricks: list[str]


@app.route('/rollseed', methods=['POST'])
def roll_seed() -> flask.Response:
    print(flask.request.get_data(), file=sys.stderr)
    params: WebParams = flask.json.loads(flask.request.get_data())  # type: ignore

    tricks: frozenset[Trick] = frozenset([getattr(Tricks, trick_name) for trick_name in params["tricks"]])

    romWriter = RomWriter.fromBlankIps()
    options = GameOptions(tricks,
                          bool(params["area_rando"]),
                          "B" if params["mmb"] else "D",
                          bool(params["small_spaceport"]),
                          bool(params["escape_shortcuts"]),
                          getattr(CypherItems, params["cypher"]))
    game = Main.generate(options)
    Main.write_rom(game, romWriter)
    response = flask.make_response(romWriter.getFinalIps())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={romWriter.getBaseFilename()}.ips'
    return response


@app.route('/tricks')
def tricks() -> flask.Response:
    return flask.jsonify(tricks_response)  # type: ignore


@app.route('/presets')
def presets() -> flask.Response:
    return flask.jsonify(presets_response)  # type: ignore


@app.route('/<path:path>')
def statics(path: str) -> flask.Response:
    return flask.send_from_directory('web/static', path)


@app.route('/')
def home() -> flask.Response:
    return flask.send_from_directory('web/static', "index.html")
