# -*- coding: utf-8 -*-

import os
import logging

import utils.dbwrapper as dbwrapper
import utils.datetime as datetime
import utils.config as config

log = logging.getLogger(__name__)


class MessageQueue(dbwrapper.DbWrapper):
    def __init__(self):
        db_path = config.Config().message_queue()
        dbwrapper.DbWrapper.__init__(self, db_path or os.path.join(os.getcwd(), 'message_queue.db3'))

    def enqueue(self, data):
        res = self.execute("INSERT OR REPLACE INTO message_queue ([data], [created_at]) VALUES (?, ?)",
                           (data, datetime.utcnow()))
        return res["result"]

    def dequeue(self):
        res = self.execute("SELECT [id], [data] FROM message_queue ORDER BY [created_at] LIMIT 1")

        if len(res["result"]) == 0:
            return None, None
        return int(res["result"][0][0]), str(res["result"][0][1])

    def remove(self, messageid):
        res = self.execute("DELETE FROM message_queue WHERE [id]=?", (str(messageid),))
        return res

    def create_db(self):
        self.execute("""
                     CREATE TABLE IF NOT EXISTS message_queue (
                     [id]         INTEGER PRIMARY KEY NOT NULL,
                     [data]       TEXT NOT NULL,
                     [created_at] TIMESTAMP NOT NULL )
                     """)
