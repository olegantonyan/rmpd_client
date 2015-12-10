# -*- coding: utf-8 -*-

import logging
import os

import utils.dbwrapper as db

log = logging.getLogger(__name__)


class State(db.DbWrapper):
    def __init__(self):
        db.DbWrapper.__init__(self, os.path.join(os.getcwd(), 'player_state.db3'))

    def increment_playbacks_count(self, media_item_advertising_id):
        res = self.execute("""
                           SELECT [playbacks_count] FROM player_state
                           WHERE [media_item_advertising_id]=? AND [date]=date()
                           """, (media_item_advertising_id,))
        if len(res['result']) == 0:
            self.execute("""
                         INSERT INTO player_state (media_item_advertising_id, date, created_at, updated_at, playbacks_count)
                         VALUES (?, date(), datetime(), datetime(), 1)
                         """, (media_item_advertising_id,))
        else:
            self.execute("""
                         UPDATE player_state SET [playbacks_count] = [playbacks_count] + 1, [updated_at]=datetime()
                         WHERE [media_item_advertising_id]=? AND [date]=date()
                         """, (media_item_advertising_id,))

    def fetch_playbacks_count(self, media_item_advertising_id):
        res = self.execute("SELECT [playbacks_count] FROM player_state WHERE [media_item_advertising_id]=?",
                           (str(media_item_advertising_id),))
        if len(res["result"]) == 0:
            return 0
        return res['result'][0][0]

    def create_db(self):
        self.execute("""
                     CREATE TABLE IF NOT EXISTS player_state (
                     [id]                           INTEGER PRIMARY KEY NOT NULL,
                     [media_item_advertising_id]    INTEGER NOT NULL,
                     [date]                         DATE NOT NULL,
                     [playbacks_count]              INTEGER NOT NULL,
                     [created_at]                   TIMESTAMP NOT NULL,
                     [updated_at]                   TIMESTAMP NOT NULL)
                     """)
        self.execute("""
                     CREATE INDEX IF NOT EXISTS media_item_advertising_id_idx ON player_state(media_item_advertising_id)
                     """)


