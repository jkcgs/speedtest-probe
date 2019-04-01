import json

from bson.json_util import dumps
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

from stprobe import settings, database
from stprobe.manager import SpeedtestMgr
from stprobe.logger import logger

# Application initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.get('session-secret')
socketio = SocketIO(app, logger=logger)

# Speedtest manager initialization - this starts speed measures.
mgr = SpeedtestMgr()
mgr.start(socketio)


# ROUTES DEFINITION

@app.route('/')
def main():
    return send_from_directory('html', 'main.html')


@app.route('/servers')
def server_list():
    return jsonify(mgr.servers)


@app.route('/results')
def results():
    return app.response_class(
        dumps(database.get_results()) + '\n',
        mimetype=app.config['JSONIFY_MIMETYPE']
    )


@socketio.on('connect')
def test_connect():
    logger.info('Client connected')
    emit('client_connect', {
        'status': mgr.status,
        'client_info': mgr.client_info
    })

    current = mgr.last_result
    if current is not None and current['download'] > 0 and current['upload'] > 0:
        emit('current_results', json.loads(dumps(current)))


if __name__ == '__main__':
    socketio.run(app, log_output=True)
    mgr.do_run = False
