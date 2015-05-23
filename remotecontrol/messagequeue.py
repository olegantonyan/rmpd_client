#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import utils.sqlexecutor

class MessageQueue(object):
    def __init__(self, dbpath):
        self.__db = utils.sqlexecutor.SqlExecutor(dbpath)
        self.__db.execute("""
                          CREATE TABLE IF NOT EXISTS message_queue (
                          [id]         INTEGER PRIMARY KEY NOT NULL,
                          [data]       TEXT NOT NULL,
                          [created_at] TIMESTAMP NOT NULL )
                          """)
    
    def enqueue(self, data):
        res = self.__db.execute("INSERT OR REPLACE INTO message_queue ([data], [created_at]) VALUES (?, ?)", (data, datetime.now()) )
        return res["result"]
    
    def dequeue(self):
        res = self.__db.execute("SELECT [id], [data] FROM message_queue ORDER BY [created_at] LIMIT 1")
        
        if len(res["result"]) == 0:
            return None, None
        return (int(res["result"][0][0]), str(res["result"][0][1]))
    
    def remove(self, messageid):
        res = self.__db.execute("DELETE FROM message_queue WHERE [id]=?", (str(messageid),) )
        return res



