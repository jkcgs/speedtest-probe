from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

from stprobe.manager import SpeedtestMgr
from stprobe.logger import logger

# Application initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = '$_very_s3cre7!'
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
    return jsonify(mgr.st.results.dict())


@socketio.on('connect')
def test_connect():
    logger.info('Client connected')
    emit('client_connect', mgr.status)
    emit('client_info', mgr.client_info)

    current = mgr.st.results
    if current.download > 0 and current.upload > 0:
        emit('current_results', dict(current.dict()))


if __name__ == '__main__':
    socketio.run(app)
    mgr.do_run = False
