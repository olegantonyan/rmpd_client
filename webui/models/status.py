# -*- coding: utf-8 -*-

import mediaplayer.playercontroller
import system.status
import utils.config
import version


class Status(object):
    @staticmethod
    def current_track_name():
        if system.status.Status().playing:
            return mediaplayer.playercontroller.PlayerController().current_track_name()
        return "nothing"

    @staticmethod
    def online():
        return system.status.Status().online

    @staticmethod
    def login():
        return utils.config.Config().login()

    @staticmethod
    def version():
        return version.VERSION
