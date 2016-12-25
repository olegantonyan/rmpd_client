#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import queue
import subprocess
import PyQt5.Qt as Qt
import time
import json
import traceback

import x.appwindow as appwindow
import x.dispatcher as dispatcher
import x.wrappers as wrappers
import x.log as log
import utils.threads as threads
import utils.shell as shell


class PipeDuplex(object):
    def __init__(self):
        self._read_q = queue.Queue(maxsize=65536)
        self._write_q = queue.Queue(maxsize=65536)
        self._stop_flag = False
        self._reader_thread = None
        self._writer_thread = None

    def start(self):
        self._reader_thread = threads.run_in_thread(self._reader)
        self._writer_thread = threads.run_in_thread(self._writer)

    def stop(self):
        self._stop_flag = True
        self.write('quit')
        if self._writer_thread is not None:
            self._writer_thread.join()
        if self._reader_thread is not None:
            self._reader_thread.join()

    def read(self):
        return self._read_q.get()

    def write(self, data):
        self._write_q.put(data)

    def _reader(self):
        while not self._stop_flag:
            try:
                data = self._read_pipe()
                self._read_q.put(data)
            except:
                traceback.print_exc()

    def _writer(self):
        while not self._stop_flag:
            try:
                data = self._write_q.get()
                if data == 'quit':
                    break
                self._write_pipe(data)
            except:
                traceback.print_exc()

    def _read_pipe(self):
        raise NotImplementedError('you have to implement this method in a subclass')

    def _write_pipe(self, data):
        raise NotImplementedError('you have to implement this method in a subclass')


class Parent(PipeDuplex):
    def __init__(self):
        shell.execute_shell('sudo chmod 777 /dev/tty*')
        env = os.environ.copy()
        env['XAUTHORITY'] = '/tmp/Xauthority'
        cli = ['startx', sys.executable, os.path.abspath(__file__), '--', '-nocursor', '-logfile', '/dev/null']
        self._proc = subprocess.Popen(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, env=env)
        super().__init__()

    def stop(self):
        super().stop()
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.kill()

    def _read_pipe(self):
        return self._proc.stdout.readline().decode('utf-8').rstrip()

    def _write_pipe(self, data):
        self._proc.stdin.write(bytes(data + '\n', 'utf-8'))
        self._proc.stdin.flush()


class Child(PipeDuplex):
    def _read_pipe(self):
        return sys.stdin.readline().rstrip()

    def _write_pipe(self, data):
        sys.stdout.write(data + '\n')
        sys.stdout.flush()


class BaseWrapper(object):
    def __init__(self):
        self._p = self._make_p()
        self._data_for_dispatcher = {}
        self._stop_flag = False
        self._thread = None

    def set_data_for_dispatcher(self, **kwargs):
        self._data_for_dispatcher = kwargs

    def start(self):
        self._thread = threads.run_in_thread(self._run)

    def stop(self):
        self._stop_flag = True
        self.send({'type': 'quit'})
        if self._thread is not None:
            self._thread.join()

    def send(self, msg):
        self._p.write(self._escape(json.dumps(msg)))

    def _make_p(self):
        raise NotImplementedError('you have to implement this method in a subclass')

    def _dispatcher(self):
        raise NotImplementedError('you have to implement this method in a subclass')

    def _run(self):
        self._p.start()
        while not self._stop_flag:
            try:
                data = self._p.read()
                data = self._unescape(data)
                if len(data) == 0:
                    continue
                data = json.loads(data)
                self._dispatcher().call(data)
            except:
                traceback.print_exc()
                time.sleep(0.1)
        self._p.stop()

    def _escape(self, msg):
        return msg.replace('\n', ':newline:')

    def _unescape(self, msg):
        return msg.replace(':newline:', '\n')


# held by daemon
# run from the daemon to start the X subprocess
class XWrapper(BaseWrapper):
    def _dispatcher(self):
        return dispatcher.Dispatcher('daemon')

    def _make_p(self):
        return Parent()


# held by X
class DaemonWrapper(BaseWrapper):
    def _dispatcher(self):
        return dispatcher.Dispatcher('x', **self._data_for_dispatcher)

    def _make_p(self):
        return Child()


def send(msg):
    if wrappers.Wrappers().x() is not None:
        wrappers.Wrappers().x().send(msg)


def start():
    wrap = XWrapper()
    wrap.start()
    wrappers.Wrappers().set_x(wrap)


def stop():
    if wrappers.Wrappers().x() is not None:
        wrappers.Wrappers().x().stop()
    wrappers.Wrappers().set_x(None)


def restart():
    stop()
    start()


def main():
    app = Qt.QApplication(sys.argv)
    win = appwindow.AppWindow()

    wrap = DaemonWrapper()
    wrap.set_data_for_dispatcher(window=win)
    wrap.start()
    wrappers.Wrappers().set_daemon(wrap)

    log.info(__name__, 'started x')

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
