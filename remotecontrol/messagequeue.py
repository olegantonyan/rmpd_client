# -*- coding: utf-8 -*-

import logging
import os

import utils.dbwrapper as dbwrapper
import utils.datetime as datetime

log = logging.getLogger(__name__)


class MessageQueue(dbwrapper.DbWrapper):
    def __init__(self):
        db_path = os.path.join(os.getcwd(), 'message_queue.db3')
        dbwrapper.DbWrapper.__init__(self, db_path)

    def enqueue(self, data):
        try:
            res = self.execute("INSERT OR REPLACE INTO message_queue ([data], [created_at]) VALUES (?, ?)",
                               (data, datetime.utcnow()))
            return res["result"]
        except:
            return None

    def dequeue(self):
        try:
            res = self.execute("SELECT [id], [data] FROM message_queue ORDER BY [created_at] LIMIT 1")

            if len(res["result"]) == 0:
                return None, None
            return int(res["result"][0][0]), str(res["result"][0][1])
        except:
            return None, None

    def remove(self, messageid):
        try:
            res = self.execute("DELETE FROM message_queue WHERE [id]=?", (str(messageid),))
            return res
        except:
            return None

    def create_db(self):
        self.execute("""
                     CREATE TABLE IF NOT EXISTS message_queue (
                     [id]         INTEGER PRIMARY KEY NOT NULL,
                     [data]       TEXT NOT NULL,
                     [created_at] TIMESTAMP NOT NULL )
                     """)
