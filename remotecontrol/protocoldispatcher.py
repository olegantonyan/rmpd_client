# -*- coding: utf-8 -*-

from os import path
from traceback import format_exc
from logging import getLogger
from tzlocal import get_localzone
from datetime import datetime

import remotecontrol.controlwrapper
import utils.singleton
import utils.config
import utils.shell
import remotecontrol.protocol.receiver

log = getLogger(__name__)


class ProtocolDispatcher(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self.__control_wrapper = remotecontrol.controlwrapper.ControlWrapper(utils.config.Config().server_url(),
                                                                             utils.config.Config().login(),
                                                                             utils.config.Config().password(),
                                                                             self.onmessage)
        self.__control_wrapper.send(self.__json_for_startup(), True)

    def onmessage(self, msg, seq):
        try:
            remotecontrol.protocol.receiver.Receiver(self.__control_wrapper, msg, seq).call()
        except Exception as e:
            log.error("error processing message '{m}' -- {e} -- {t}".format(m=str(msg), e=str(e), t=format_exc()))

    def send_now_playing(self, track, percent_pos):
        if track is None and percent_pos is None:
            # TODO if updating now - srn one thing, else another
            self.__control_wrapper.send(self.__json_for_now_playing("none"))
        else:
            track = "{name} ({c}%)".format(name=path.basename(str(track)), c=str(percent_pos))
            self.__control_wrapper.send(self.__json_for_now_playing(track))

    def send_onplay(self, track):
        if track is None:
            log.error("track is none")
        else:
            self.__control_wrapper.send(self.__json_for_onplay(track), True)

    def send_onstop(self, track):
        if track is None:
            log.error("track is none")
        else:
            self.__control_wrapper.send(self.__json_for_onstop(track), True)

    def send_on_playlist_begin(self, files):
        self.__control_wrapper.send(self.__json_for_begin_playlist(files), True)

    def send_onerror(self, message):
        if message is None:
            log.error("message is none")
        else:
            self.__control_wrapper.send(self.__json_for_onerror(message), True)

    def send_ack(self, ok, seq, message):
        self.__control_wrapper.send(self.__json_for_ack(ok, message), True, seq)

    def __json_for_onplay(self, track):
        return {"type": "playback", "localtime": self.__thetime(), "status": "begin", "track": str(track)}

    def __json_for_onstop(self, track):
        return {"type": "playback", "localtime": self.__thetime(), "status": "end", "track": str(track)}

    def __json_for_onerror(self, message):
        return {"type": "playback", "localtime": self.__thetime(), "status": "error", "track": str(message)}

    def __json_for_startup(self):
        return {"type": "power", "localtime": self.__thetime(), "status": "on"}

    def __json_for_now_playing(self, track):
        return {"type": "playback", "status": "now_playing", "localtime": self.__thetime(), "track": str(track)}

    def __json_for_update_playlist(self, files):
        return {"type": "playback", "localtime": self.__thetime(), "status": "update_playlist", "track": files}

    def __json_for_begin_playlist(self, files):
        return {"type": "playback", "localtime": self.__thetime(), "status": "begin_playlist", "track": files}

    def __json_for_ack(self, ok, message):
        return {"type": "ack", "status": "ok" if ok else "fail", "localtime": self.__thetime(), "message": message}

    def __thetime(self):
        return datetime.now(get_localzone()).strftime("%Y-%m-%dT%H:%M:%S%z")
