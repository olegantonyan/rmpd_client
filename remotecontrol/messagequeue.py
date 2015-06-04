#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from logging import getLogger
from os import remove

log = getLogger(__name__)

import utils.sqlexecutor

class MessageQueue(object):
    def __init__(self, dbpath):
        self.__db_path = dbpath
        self.__db = utils.sqlexecutor.SqlExecutor(self.__db_path)
        self.__error_count = 0
        try:
            self.__create_db()
        except:
            self.__error_count = self.__error_count + 1

    def __reinit_db(self):
        log.warning('re-initializing message queue')
        self.__db = None
        remove(self.__db_path)
        self.__db = utils.sqlexecutor.SqlExecutor(self.__db_path)
        self.__create_db()
        self.__error_count = 0

    def __watch_exceptions(func):
        def wrap(self, *args):
            try:
                return func(self, *args)
            except utils.sqlexecutor.SqlError as e:
                log.exception("message queu sql error #%s", self.__error_count + 1)
                self.__error_count = self.__error_count + 1
                raise
        return wrap

    def __guard_db(func):
        def wrap(self, *args):
            if self.__error_count > 15:
                self.__reinit_db()
            return func(self, *args)
        return wrap

    @__guard_db
    @__watch_exceptions
    def enqueue(self, data):
        res = self.__db.execute("INSERT OR REPLACE INTO message_queue ([data], [created_at]) VALUES (?, ?)", (data, datetime.now()) )
        return res["result"]

    @__guard_db
    @__watch_exceptions
    def dequeue(self):
        res = self.__db.execute("SELECT [id], [data] FROM message_queue ORDER BY [created_at] LIMIT 1")

        if len(res["result"]) == 0:
            return None, None
        return (int(res["result"][0][0]), str(res["result"][0][1]))

    @__guard_db
    @__watch_exceptions
    def remove(self, messageid):
        res = self.__db.execute("DELETE FROM message_queue WHERE [id]=?", (str(messageid),) )
        return res

    def __create_db(self):
        self.__db.execute("""
                          CREATE TABLE IF NOT EXISTS message_queue (
                          [id]         INTEGER PRIMARY KEY NOT NULL,
                          [data]       TEXT NOT NULL,
                          [created_at] TIMESTAMP NOT NULL )
                          """)
