# -*- coding: utf-8 -*-

import logging
import os

import utils.dbwrapper as db

log = logging.getLogger(__name__)


class State(db.DbWrapper):
    def __init__(self):
        db.DbWrapper.__init__(self, os.path.join(os.getcwd(), 'player_state.db3'))

    def create_db(self):
        self.execute("""
                     CREATE TABLE IF NOT EXISTS player_state (
                     [id]         INTEGER PRIMARY KEY NOT NULL,
                     [data]       TEXT NOT NULL,
                     [created_at] TIMESTAMP NOT NULL )
                     """)

