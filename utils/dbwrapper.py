# -*- coding: utf-8 -*-

import os
import logging

import utils.sqlexecutor
import utils.datetime

log = logging.getLogger(__name__)


def _guard_errors(func):
    def wrap(self, *args):
        try:
            result = func(self, *args)
            self._error_count = 0
            return result
        except utils.sqlexecutor.SqlError:
            self._error_count += 1
            log.exception("%s sql error #%s", self._db_path, self._error_count)
            if self._error_count > self._max_errors:
                self._reinit_db()
            raise
    return wrap


class DbWrapper(object):
    def __init__(self, dbpath):
        self._db_path = dbpath
        self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
        self._error_count = 0
        self._max_errors = 5
        try:
            self.create_db()
        except:
            self._reinit_db()

    def _reinit_db(self):
        try:
            log.warning('re-initializing {f}'.format(f=self._db_path))
            self._db.close()
            os.rename(self._db_path, self._db_path + "_" + str(utils.datetime.now()))
        except:
            pass
        finally:
            self._db = utils.sqlexecutor.SqlExecutor(self._db_path)
            self.create_db()
            self._error_count = 0

    @_guard_errors
    def execute(self, statement, values=()):
        return self._db.execute(statement, values)

    def create_db(self):
        raise NotImplementedError("you must implement 'create_db' method in subclass")

