import json
import threading
import time
from datetime import datetime

import requests
import speedtest
from bson.json_util import dumps

from . import settings
from . import database
from .logger import logger


class SpeedtestMgr:
    def __init__(self):
        self.st = speedtest.Speedtest()
        self.do_run = True
        self.pause = False
        self.last_result = None

        self._sleep = settings.get('scan-interval') * 60
        self._thread = None
        self.__status = "none"
        self.__client_info = None
        self.__all_servers = None

    def task(self, socketio):
        while self.do_run:
            if self.pause:
                time.sleep(1)
                continue

            batch_results = []
            start = datetime.utcnow()
            for server_id in settings.get('servers'):
                sv = self.st.get_servers([server_id])
                sv = sv[list(sv.keys())[0]][0]

                logger.debug('Starting speedtest with server: %s (%s - %s) %s',
                             sv['sponsor'], sv['name'], sv['country'], sv['host'])
                self.update_status(socketio, "started", {'timestamp': str(start)})

                # Cancel point
                if not self.do_run:
                    break

                logger.debug('Testing download speed...')
                self.update_status(socketio, "downloading")
                download = self.st.download()
                logger.debug('Download test finished with %s bits', download)

                # Cancel point
                if not self.do_run:
                    break

                logger.debug('Testing upload speed...')
                self.update_status(socketio, "uploading")
                upload = self.st.upload()
                logger.debug('Upload test finished with %s bits', upload)

                # Cancel point
                if not self.do_run:
                    break

                results = self.st.results.dict()
                results['server'] = sv
                results['batch_timestamp'] = start.isoformat()
                batch_results.append(results)
                self.last_result = results
                database.insert_result(results)

                logger.debug('Speedtest finished: %s', results)
                self.update_status(socketio, "finished", json.loads(dumps(results)))

            # Cancel point
            if not self.do_run:
                break

            # Run at the next scheduled time
            diff = max(self._sleep - (datetime.utcnow() - start).total_seconds(), 15)
            self.update_status(socketio, "batch_finished", {
                'sleep_time': diff, 'results': json.loads(dumps(batch_results))
            })

            logger.debug('Waiting for {:.3f} seconds for the next measurement.'.format(diff))
            time.sleep(diff)

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

    def update_status(self, socketio, status, data=None):
        self.__status = status

        payload = {'status': status, 'data': data}
        socketio.emit('speedtest_update', payload)
