# -*- coding: utf-8 -*-

import os
import logging

import utils.sqlexecutor
import utils.datetime

log = logging.getLogger(__name__)


def _guard_errors(func):
    def wrap(self, *args):
        try:
            return func(self, *args)
        except utils.sqlexecutor.SqlError:
            log.exception("%s sql error #%s", self._db_path, self._error_count + 1)
            self._error_count += 1
            if self._error_count > 15:
                self._reinit_db()
            raise
    return wrap


class DbWrapper(object):
    def __init__(self, dbpath):
        self._db_path = dbpath
        self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
        self._error_count = 0
        try:
            self.create_db()
        except:
            self._error_count += 1

    def _reinit_db(self):
        log.warning('re-initializing {f}'.format(f=self._db_path))
        self._db = None
        os.rename(self._db_path, self._db_path + "_" + str(utils.datetime.now()))
        self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
        self.create_db()
        self._error_count = 0

    @_guard_errors
    def execute(self, statement, values=()):
        return self._db.execute(statement, values)

    def create_db(self):
        raise NotImplementedError("you must implement 'create_db' method in subclass")

