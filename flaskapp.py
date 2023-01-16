import sys
from typing import TypedDict
import flask

import Main
import logic_presets
from romWriter import RomWriter
from trick import Trick
from trick_data import Tricks

app = flask.Flask(__name__)


def make_tricks_response() -> list[tuple[str, str]]:
    tr: list[tuple[str, str]] = []
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick):
            tr.append((trick_name, trick.desc))
    return tr


tricks_response = make_tricks_response()


def make_presets_response() -> list[tuple[str, list[str]]]:
    name_lookup = {
        trick: trick_name
        for trick_name, trick in vars(Tricks).items()
        if isinstance(trick, Trick)
    }
    tr = [
        ("casual", [name_lookup[t] for t in logic_presets.casual]),
        ("medium", [name_lookup[t] for t in logic_presets.medium]),
        ("expert", [name_lookup[t] for t in logic_presets.expert]),
    ]
    return tr


presets_response = make_presets_response()


class WebParams(TypedDict):
    area_rando: bool
    small_spaceport: bool
    tricks: list[str]


@app.route('/rollseed', methods=['POST'])
def roll_seed() -> flask.Response:
    print(flask.request.get_data(), file=sys.stderr)
    params: WebParams = flask.json.loads(flask.request.get_data())  # type: ignore

    tricks: frozenset[Trick] = frozenset([getattr(Tricks, trick_name) for trick_name in params["tricks"]])

    romWriter = RomWriter.fromBlankIps()
    game = Main.generate(tricks, bool(params["area_rando"]), "D", bool(params["small_spaceport"]))
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
