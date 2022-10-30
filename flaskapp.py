import flask
import Main
from romWriter import RomWriter

app = flask.Flask(__name__)

@app.route('/rollseed')
def roll_seed():
    argv = ['dummyexe']
    argv.extend(flask.request.args.get('argv', default="").split())
    romWriter = RomWriter.fromBlankIps()
    Main.Main(argv, romWriter)
    response = flask.make_response(romWriter.getFinalIps())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={romWriter.getBaseFilename()}.ips'
    return response
