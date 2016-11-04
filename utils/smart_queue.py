# -*- coding: utf-8 -*-

import collections
import sqlite3
import os
import json
import logging

import utils.datetime

log = logging.getLogger(__name__)


class SmartQueue(object):
    def __init__(self, maxlen=None, db_params=None):
        self._deque = collections.deque(maxlen=maxlen)

        self._db_params = db_params
        self._db = None
        self._current_id = 0
        if self._db_params is not None:
            stmt = """
                   CREATE TABLE IF NOT EXISTS '{table}' (
                   [id]         INTEGER PRIMARY KEY NOT NULL,
                   [data]       TEXT NOT NULL,
                   [created_at] TIMESTAMP NOT NULL )
                   """.format(table=self._db_params['table'])
            self._db = Db(self._db_params['path'], stmt)
            if os.path.exists(self._db_params['path']):
                self._load()

    def enqueue(self, obj, oid=None, created_at=str(utils.datetime.utcnow())):
        if oid is None:
            oid = self._next_id()
        return self._deque.appendleft({'id': oid, 'created_at': created_at, 'data': obj})

    def peek(self):
        return list(self._deque)[-1]['data']

    def dequeue(self):
        return self._deque.pop()['data']

    def sync(self):
        if self._db is None:
            return
        values = ["({id}, '{data}', '{created_at}')".format(id=i['id'], data=json.dumps(i['data']), created_at=i['created_at']) for i in self._deque]
        if len(values) > 0:
            qry = "INSERT OR REPLACE INTO '{table}' ([id], [data], [created_at]) VALUES ".format(table=self._db_params['table'])
            if not os.path.exists(self._db_params['path']):
                self._db.init_db()
            qry += (', '.join(values) + ';')
            self._db.exec(qry)
        ids_to_remove = [str(i['id']) for i in self._deque]
        self._db.exec("DELETE FROM '{table}' WHERE [id] NOT IN ({ids});".format(table=self._db_params['table'], ids=','.join(ids_to_remove)))

    def _load(self):
        if self._db is None:
            return
        result = self._db.exec("SELECT [id], [data], [created_at] FROM '{table}' ORDER BY [created_at]".format(table=self._db_params['table']))
        if result is False:
            return
        if len(result) == 0:
            return
        for i in result:
            oid = int(i[0])
            data = json.loads(str(i[1]))
            created_at = str(i[2])
            self.enqueue(data, oid, created_at)
        result = self._db.exec("SELECT max(id) FROM '{table}' ORDER BY [created_at]".format(table=self._db_params['table']))
        self._current_id = int(result[0][0])

    def _next_id(self):
        self._current_id += 1
        return self._current_id


class Db(object):
    def __init__(self, path, init_statement):
        self._path = path
        self._init_statement = init_statement
        self._retries_before_reinit = 5

    def exec(self, statement, values=()):
        for i in range(self._retries_before_reinit):
            result = self._exec_single(statement, values)
            if result is not False:
                return result
        self.re_init_db()
        return self._exec_single(statement, values)

    def _exec_single(self, statement, values=()):
        connection = None
        try:
            connection = sqlite3.connect(self._path)
            cursor = connection.cursor()
            cursor.execute(statement, values)
            result = cursor.fetchall()
            connection.commit()
            return result
        except:
            ls = statement
            if len(statement) > 100:
                ls = statement[0:99] + '...'
            log.exception('error executing sql `{s}`'.format(s=ls))
            return False
        finally:
            try:
                connection.close()
            except:
                pass

    def init_db(self):
        log.info('initializing db ' + self._path)
        self._exec_single(self._init_statement)

    def re_init_db(self):
        log.info('re-initializing db ' + self._path)
        os.rename(self._path, self._path + "_" + str(utils.datetime.now()))
        self.init_db()
