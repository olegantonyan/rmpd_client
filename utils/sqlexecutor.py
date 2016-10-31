# -*- coding: utf-8 -*-

import sqlite3
import threading
import queue
import traceback


class SqlError(RuntimeError):
    pass


class SqlExecutor(object):
    def __init__(self, dbpath):
        self._db_path = dbpath
        self._rx = queue.Queue()
        self._tx = queue.Queue()
        self._thread = threading.Thread(target=self._serve)
        self._thread.setDaemon(True)
        self._stop_flag = False
        self._exec_timeout = 30
        self._thread.start()

    def _serve(self):
        self._conn = sqlite3.connect(self._db_path)
        cursor = self._conn.cursor()
        while not self._stop_flag:
            try:
                statement, values = self._rx.get()
                cursor.execute(statement, values)
                result = cursor.fetchall()
                self._conn.commit()
                self._tx.put({"result": result, "ok": True, "error_message": ""})
            except:
                self._tx.put({"result": [], "ok": False, "error_message": traceback.format_exc()})
        try:
            self._conn.close()
        except:
            pass

    def execute(self, statement, values=()):
        self._rx.put((statement, values))
        try:
            res = self._tx.get(block=True, timeout=self._exec_timeout)
        except queue.Empty:
            raise SqlError("sql execution timed out ({s} seconds)".format(s=self._exec_timeout))
        if not res['ok']:
            raise SqlError("error while executing sql '{s}' with values '{v}'\n{m}".format(s=statement,
                                                                                           v=str(values),
                                                                                           m=res['error_message']))
        return res

    def close(self):
        self._stop_flag = True
        try:
            self.execute("SELECT TIME()")  # force execution to fetch from queue
        except:
            pass

    def __del__(self):
        self.close()
