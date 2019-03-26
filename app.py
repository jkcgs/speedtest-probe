from datetime import datetime
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import time
from manager import SpeedtestMgr

app = Flask(__name__)
app.config['SECRET_KEY'] = '$_very_s3cre7!'
socketio = SocketIO(app)


mgr = SpeedtestMgr()


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
    emit('client_connect', mgr.status)
    emit('client_info', mgr.client_info)
    emit('current_results', dict(mgr.st.results.dict()))


def background():
    thread = threading.currentThread()

    while getattr(thread, "do_run", True):
        start = datetime.now()

        # Run speedtest task
        mgr.task(socketio)

        diff = 60 - (datetime.now() - start).total_seconds()
        print('wait for', diff, 'seconds')
        time.sleep(max(diff, 0))


print('Starting thread')
t = threading.Thread(target=background)
t.start()

if __name__ == '__main__':
    socketio.run(app)
    t.do_run = False
