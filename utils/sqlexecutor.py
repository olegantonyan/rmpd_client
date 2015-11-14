# -*- coding: utf-8 -*-

import sqlite3
import threading
import queue
import traceback


class SqlError(RuntimeError):
    pass


class SqlExecutor(object):
    def __init__(self, dbpath):
        self.__db_path = dbpath
        self.__rx = queue.Queue()
        self.__tx = queue.Queue()
        self.__thread = threading.Thread(target=self.__serve)
        self.__thread.setDaemon(True)
        self.__stop_flag = False
        self.__thread.start()

    def __serve(self):
        self.__conn = sqlite3.connect(self.__db_path)
        cursor = self.__conn.cursor()
        while not self.__stop_flag:
            try:
                statement, values = self.__rx.get()
                cursor.execute(statement, values)
                result = cursor.fetchall()
                self.__conn.commit()
                self.__tx.put({"result": result, "ok": True, "error_message": ""})
            except:
                self.__tx.put({"result": [], "ok": False, "error_message": traceback.format_exc()})

    def execute(self, statement, values=()):
        self.__rx.put((statement, values))
        res = self.__tx.get()
        if not res["ok"]:
            raise SqlError("error while executing sql '{s}' with values '{v}'\n{m}".format(s=statement, v=str(values), m=res["error_message"]))
        return res

    def __del__(self):
        self.__stop_flag = True
        try:
            self.execute("SELECT TIME()")  # force execution to fetch from queue
        except:
            pass
