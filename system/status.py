# -*- coding: utf-8 -*-

import utils.singleton as singleton
import hardware
import system.self_update as self_update


class Status(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._online = False
        self._playing = False
        self._downloading = False
        self._self_update_once = True

    @property
    def online(self):
        return self._online

    @online.setter
    def online(self, state):
        self._online = state
        hardware.platfrom.set_network_led(state)
        if state and self._self_update_once:
            self_update.SelfUpdate().verify()
            self._self_update_once = False

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, state):
        self._playing = state
        hardware.platfrom.set_player_led(state)

    @property
    def downloading(self):
        return self._downloading

    @downloading.setter
    def downloading(self, state):
        self._downloading = state
        hardware.platfrom.set_network_blink_led(state)
