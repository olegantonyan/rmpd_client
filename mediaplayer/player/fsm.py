# -*- coding: utf-8 -*-

import fysom


class Fsm(object):
    def __init__(self):
        self._fsm = fysom.Fysom({'initial': 'stopped',
                                 'events': [
                                    {'name': 'stop', 'src': 'playing', 'dst': 'stopped'},
                                    {'name': 'play', 'src': 'stopped', 'dst': 'playing'}
                                 ],
                                 'callbacks': {
                                    'onplay': self._onplay,
                                    'onplaying': self._onplaying
                                 }})

    def play(self, filepath):
        self._fsm.trigger('play', filepath=filepath)

    def stop(self):
        self._fsm.trigger('stop')

    def _onplay(self, e):
        # run onplaycallback write logs etc
        print("**********" + e.filepath)
        print(e)
        return False

    def _onplaying(self, e):
        # run actual play on player
        print("###########" + e.filepath)
        print(e)


