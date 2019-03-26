from datetime import datetime

import requests
import speedtest


class SpeedtestMgr:
    def __init__(self):
        self.st = speedtest.Speedtest()

        self.__status = "none"
        self.__client_info = None
        self.__servers = None

        # Load servers list
        self.st.get_servers()

    def task(self, socketio):
        start = datetime.now()
        self.set_status("started", socketio)
        socketio.emit('speedtest_started', {'timestamp': str(start)})

        self.set_status("downloading", socketio)
        self.st.download()

        self.set_status("uploading", socketio)
        self.st.upload()

        self.set_status("finished", socketio)
        socketio.emit('speedtest_finished', self.st.results.dict())

    @property
    def status(self):
        return self.__status

    @property
    def client_info(self):
        if self.__client_info is None:
            self.__client_info = requests.get('http://extreme-ip-lookup.com/json/').json()

        return self.__client_info

    @property
    def servers(self):
        if self.__servers is None:
            self.__servers = sorted([v[0] for k, v in self.st.servers.items()], key=lambda x: x['d'])

        return self.__servers

    def set_status(self, status, socketio=None):
        self.__status = status

        if socketio is not None:
            socketio.emit('speedtest_update', status)
