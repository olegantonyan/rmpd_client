# -*- coding: utf-8 -*-

import socket
import json
import queue
import importlib
import time

import utils.threads as threads
import utils.singleton as singleton
import utils.support as support


class BaseConnector(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._stop_flag = False
        self._host = ('localhost', 54845)
        self._queue = queue.Queue()
        self._conn = None  # override in child
        threads.run_in_thread(self._run_send_queue)

    def stop(self):
        self._stop_flag = True

    def send(self, msg):
        return self._queue.put(self._encode_msg(msg))

    def _onreceive(self, msg):
        try:
            self._dispatch(msg)
        except:
            pass

    def _dispatch(self, msg):
        command_name = msg['type']
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".commands.{proc}.{name}".format(name=command_name,
                                                                          proc=self.__class__.__name__.lower()), __package__)
        command_class = getattr(module, command_class_name)
        command_object = command_class(msg)
        command_object.call()

    def _run_send_queue(self):
        while not self._stop_flag:
            data = self._queue.get()
            while not self._stop_flag:
                try:
                    self._conn.sendall(data)
                    break
                except:
                    time.sleep(0.05)

    def _decode_msg(self, msg):
        return json.loads(msg.decode('utf-8'))

    def _encode_msg(self, msg_dict):
        return bytes(json.dumps(msg_dict), 'utf-8')

    def _close_socket(self, s):
        try:
            s.close()
        except:
            pass


class X(BaseConnector):
    def __init__(self):
        super().__init__()
        threads.run_in_thread(self._run)

    def _run(self):
        sock = None
        while not self._stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(self._host)
                sock.listen(1)
                break
            except:
                time.sleep(0.1)
        while not self._stop_flag:
            try:
                self._conn, _ = sock.accept()
                while not self._stop_flag:
                    try:
                        data = self._conn.recv(65536)
                        self._onreceive(self._decode_msg(data))
                    except:
                        self._close_socket(self._conn)
                        break
            except:
                time.sleep(0.1)
        self._close_socket(sock)


class Daemon(BaseConnector):
    def __init__(self):
        super().__init__()
        self._conn = None
        threads.run_in_thread(self._run)

    def _run(self):
        while not self._stop_flag:
            try:
                self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._conn.connect(self._host)
                while not self._stop_flag:
                    try:
                        data = self._conn.recv(65536)
                        self._onreceive(self._decode_msg(data))
                    except:
                        break
            except:
                time.sleep(0.1)
        self._close_socket(self._conn)


