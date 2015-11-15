#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger
from os import path, remove, listdir
from urllib import parse
from traceback import format_exc
from threading import Thread

import utils.config
import utils.state
import remotecontrol.httpclient
import mediaplayer.playercontroller
import remotecontrol.protocoldispatcher
import system.status

log = getLogger(__name__)


class PlaylistManage(object):
    def __init__(self):
        self.__state = {"updating": False, "deleting": False}
        self.__threads = {"updating": None, "deleting": None}

    def busy(self):
        return self.__state["updating"] or self.__state["deleting"]

    def start_update(self, items, seq):
        self.__state["updating"] = True
        self.__threads["updating"] = UpdateWorker(items, seq, self.__on_playlist_update_finished)
        self.__threads["updating"].start()
        system.status.Status().downloading = True

    def start_delete(self, seq):
        self.__state["deleting"] = True
        self.__threads["deleting"] = DeleteWorker(seq, self.__on_playlist_delete_finished)
        self.__threads["deleting"].start()

    def __on_playlist_update_finished(self, ok, seq, message=""):
        self.__state["updating"] = False
        if ok:
            mediaplayer.playercontroller.PlayerController().start_playlist()
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send_ack(ok, seq, message)
        system.status.Status().downloading = False

    def __on_playlist_delete_finished(self, ok, seq, message=""):
        self.__state["deleting"] = False
        if ok:
            mediaplayer.playercontroller.PlayerController().stop()
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send_ack(ok, seq, message)


def mediafiles_path():
    return utils.config.Config().mediafiles_path()


def full_file_localpath(relativeurl):
    filepath = mediafiles_path()
    fullpath = path.join(filepath, path.basename(relativeurl))
    return fullpath


def list_files_in_playlist(playlist_file):
    result = []
    with open(playlist_file, 'r') as file:
        for line in file:
            result.append(line.rstrip('\r|\n'))
    return result


class UpdateWorker(Thread):
    def __init__(self, media_items, seq, onfinish_callback):
        Thread.__init__(self)
        self.__media_items = media_items
        self.__seq = seq
        self.daemon = True
        self.__onfinish = onfinish_callback

    def run(self):
        try:
            for i in self.__media_items:
                if i is not None:
                    url = self.__full_file_url(i)
                    localpath = full_file_localpath(i)
                    if not path.isfile(localpath) or localpath.endswith("m3u"):
                        log.info("downloading file '%s'", url)
                        self.__download_file(url, localpath)
            utils.state.State().current_track_num = 0
            self.__utilize_nonplaylist_files(self.__media_items, mediafiles_path())
            self.__onfinish(True, self.__seq, "playlist updated successfully")
        except Exception:
            log.error("error updating playlist\n{ex}".format(ex=format_exc()))
            self.__onfinish(False, self.__seq, "playlist update error")

    def __download_file(self, url, localpath):
        remotecontrol.httpclient.download_file(url, localpath)

    def __full_file_url(self, relativeurl):
        return parse.urljoin(utils.config.Config().server_url(), relativeurl)

    def __utilize_nonplaylist_files(self, media_items, media_items_path):
        media_items = [path.basename(i) for i in media_items]
        for file in listdir(media_items_path):
            if file not in media_items and not file.endswith('.log'):
                log.info("removing file not in currnet playlist '{f}'".format(f=file))
                remove(full_file_localpath(file))


class DeleteWorker(Thread):
    def __init__(self, seq, onfinish_callback):
        Thread.__init__(self)
        self.__seq = seq
        self.daemon = True
        self.__onfinish = onfinish_callback

    def run(self):
        try:
            playlist_fullpath = full_file_localpath("playlist.m3u")
            for f in list_files_in_playlist(playlist_fullpath):
                try:
                    remove(full_file_localpath(f))
                except FileNotFoundError:
                    pass
            remove(playlist_fullpath)
            utils.state.State().current_track_num = 0
            self.__onfinish(True, self.__seq, "playlist deleted successfully")
        except Exception:
            log.error("error deleting playlist\n{ex}".format(ex=format_exc()))
            self.__onfinish(False, self.__seq, "playlist delete error")
