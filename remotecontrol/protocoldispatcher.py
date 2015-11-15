# -*- coding: utf-8 -*-

from os import path
from traceback import format_exc
from logging import getLogger
from tzlocal import get_localzone
from datetime import datetime

import remotecontrol.controlwrapper
import remotecontrol.playlistmanage
import utils.singleton
import utils.config
import utils.shell
import remotecontrol.protocol.receiver

log = getLogger(__name__)


class ProtocolDispatcher(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self.__playlist_manage = remotecontrol.playlistmanage.PlaylistManage()
        self.__control_wrapper = remotecontrol.controlwrapper.ControlWrapper(utils.config.Config().server_url(),
                                                                             utils.config.Config().login(),
                                                                             utils.config.Config().password(),
                                                                             self.onmessage)
        self.__control_wrapper.send(self.__json_for_startup(), True)

    def onmessage(self, msg, seq):
        try:
            if msg["type"] == "playlist":
                self.__process_playlist(msg, seq)
            if msg["type"] == "ssh_tunnel":
                remotecontrol.protocol.receiver.Receiver(self.__control_wrapper, msg, seq).call()
                #self.__process_ssh_tunnel(msg, seq)
            # remotecontrol.protocol.receiver.Receiver(self.__control_wrapper, msg, seq).call()
        except Exception as e:
            log.error("error processing message '{m}' -- {e} -- {t}".format(m=str(msg), e=str(e), t=format_exc()))

    def send_now_playing(self, track, percent_pos):
        if track is None and percent_pos is None:
            if self.__playlist_manage.busy():
                self.__control_wrapper.send(self.__json_for_now_playing("updating_now"))
            else:
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

    def __process_playlist(self, jsondata, seq):
        if jsondata["status"] == "update":
            items = jsondata["items"]
            self.__control_wrapper.send(self.__json_for_update_playlist([path.basename(i) for i in items]), True)
            self.__playlist_manage.start_update(items, seq)
        elif jsondata["status"] == "delete":
            self.__control_wrapper.send(self.__json_for_update_playlist([]), True)
            self.__playlist_manage.start_delete(seq)
        else:
            raise RuntimeError("unknown playlist status")

    def __process_ssh_tunnel(self, jsondata, seq):
        if jsondata["status"] == "open":
            cli = "ssh -R {ext_port}:localhost:{int_port} {user}@{server} -p {server_port} -f sleep {dur}"\
                .format(ext_port=jsondata["external_port"], int_port=jsondata["internal_port"], user=jsondata["username"],
                        server=jsondata["server"], server_port=jsondata["server_port"], dur=jsondata["duration"])
            m = "opening ssh tunnel: '{cli}'".format(cli=cli)
            log.info(m)
            self.send_ack(True, seq, m)
            r, o, e = utils.shell.execute(cli)
            log.info("ssh tunnel result: {r}, stdout: {o}, stderr: {e}".format(r=r, o=o, e=e))

    def __thetime(self):
        return datetime.now(get_localzone()).strftime("%Y-%m-%dT%H:%M:%S%z")
