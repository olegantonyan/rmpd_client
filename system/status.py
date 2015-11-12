#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.singleton  # @UnusedImport
import hardware


class Status(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self.__online = False
        self.__playing = False
        self.__downloading = False

    @property
    def online(self):
        return self.__online

    @online.setter
    def online(self, state):
        self.__online = state
        hardware.platfrom.set_network_led(state)

    @property
    def playing(self):
        return self.__playing

    @playing.setter
    def playing(self, state):
        self.__playing = state
        hardware.platfrom.set_player_led(state)

    @property
    def downloading(self):
        return self.__downloading

    @downloading.setter
    def downloading(self, state):
        self.__downloading = state
        hardware.platfrom.set_network_blink_led(state)
    
