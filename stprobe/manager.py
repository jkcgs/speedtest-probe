import threading
import time
from datetime import datetime

import requests
import speedtest

from . import settings
from .logger import logger


class SpeedtestMgr:
    def __init__(self):
        self.st = speedtest.Speedtest()
        self.do_run = True
        self.pause = False

        self._sleep = settings.get('scan-interval')
        self._thread = None
        self.__status = "none"
        self.__client_info = None
        self.__all_servers = None

        # Load servers list
        self.st.get_servers(settings.get('servers'))

    def task(self, socketio):
        while self.do_run:
            if self.pause:
                time.sleep(1)
                continue

            start = datetime.now()

            logger.debug('Starting speedtest...')
            self.set_status("started", socketio)
            socketio.emit('speedtest_started', {'timestamp': str(start)})

            logger.debug('Testing download speed...')
            self.set_status("downloading", socketio)
            self.st.download()

            logger.debug('Testing upload speed...')
            self.set_status("uploading", socketio)
            self.st.upload()

            logger.debug('Speedtest finished.')
            self.set_status("finished", socketio)
            socketio.emit('speedtest_finished', self.st.results.dict())

            # Run at the next scheduled time
            diff = self._sleep - (datetime.now() - start).total_seconds()
            logger.debug('Waiting for {:.3f} seconds for the next measurement.'.format(diff))
            time.sleep(max(diff, 0))

    def start(self, socketio):
        if self._thread is not None:
            logger.warn('SpeedtestMgr$start already invoked.')
            return

        logger.debug('Starting speedtest thread...')
        self._thread = threading.Thread(target=self.task, args=(socketio,))
        self._thread.start()
        logger.debug('Speedtest thread started.')

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
        if self.__all_servers is None:
            self.st.get_servers()
            self.__all_servers = [v[0] for k, v in self.st.servers.items()]
            self.__all_servers.sort(key=lambda x: x['d'])

        return self.__all_servers

    def set_test_servers(self, server_list):
        if not isinstance(server_list, list) and not isinstance(server_list, int):
            raise RuntimeError('server_list must be a list of servers ids or an int')

        if isinstance(server_list, int):
            server_list = [server_list]

        for server_id in server_list:
            found = False
            for k, server in self.__all_servers:
                if server_id == server['id']:
                    found = True
                    break
            if not found:
                raise RuntimeError('Server id {} not found'.format(server_id))

        self.st.get_servers(server_list)

    def set_status(self, status, socketio=None):
        self.__status = status

        if socketio is not None:
            socketio.emit('speedtest_update', status)
