# -*- coding: utf-8 -*-

import datetime
import os
import logging

import utils.sqlexecutor

log = logging.getLogger(__name__)


class MessageQueue(object):
    def __init__(self, dbpath):
        self._db_path = dbpath
        self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
        self._error_count = 0
        try:
            self._create_db()
        except:
            self._error_count += 1

    def _reinit_db(self):
        log.warning('re-initializing message queue')
        self._db = None
        os.remove(self._db_path)
        self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
        self._create_db()
        self._error_count = 0

    def _watch_exceptions(func):
        def wrap(self, *args):
            try:
                return func(self, *args)
            except utils.sqlexecutor.SqlError as e:
                log.exception("message queue sql error #%s", self._error_count + 1)
                self._error_count += 1
                raise
        return wrap

    def _guard_db(func):
        def wrap(self, *args):
            if self._error_count > 15:
                self._reinit_db()
            return func(self, *args)
        return wrap

    @_guard_db
    @_watch_exceptions
    def enqueue(self, data):
        res = self._db.execute("INSERT OR REPLACE INTO message_queue ([data], [created_at]) VALUES (?, ?)",
                               (data, datetime.datetime.now()))
        return res["result"]

    @_guard_db
    @_watch_exceptions
    def dequeue(self):
        res = self._db.execute("SELECT [id], [data] FROM message_queue ORDER BY [created_at] LIMIT 1")

        if len(res["result"]) == 0:
            return None, None
        return int(res["result"][0][0]), str(res["result"][0][1])

    @_guard_db
    @_watch_exceptions
    def remove(self, messageid):
        res = self._db.execute("DELETE FROM message_queue WHERE [id]=?", (str(messageid),))
        return res

    def _create_db(self):
        self._db.execute("""
                          CREATE TABLE IF NOT EXISTS message_queue (
                          [id]         INTEGER PRIMARY KEY NOT NULL,
                          [data]       TEXT NOT NULL,
                          [created_at] TIMESTAMP NOT NULL )
                          """)
