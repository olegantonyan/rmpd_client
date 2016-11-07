# -*- coding: utf-8 -*-

import os
import logging

import mediaplayer.playlist.scheduler as scheduler
import mediaplayer.player.watcher as watcher
import utils.files as files
import remotecontrol.protocoldispatcher as protocoldispatcher
import mediaplayer.playlist.loader as loader
import mediaplayer.playlist.playlist as playlist
import system.rw_fs as rw_fs

log = logging.getLogger(__name__)


class PlayerController(object):
    def __init__(self):
        self._player = watcher.Watcher()
        self._scheduler = scheduler.Scheduler()
    
    def start_playlist(self):
        mediafiles_fullpath = files.mediafiles_path()
        if not os.path.exists(mediafiles_fullpath):
            with rw_fs.Storage(restart_player=False):
                files.mkdir(mediafiles_fullpath)
        
        playlist_fullpath = loader.Loader().filepath()
        if not os.path.exists(playlist_fullpath):
            log.error("playlist file '{f}' does not exists".format(f=playlist_fullpath))
            return

        protocoldispatcher.ProtocolDispatcher().send('playlist_begin',
                                                     files=loader.Loader(playlist_fullpath).list_all_files())
        self._scheduler.set_playlist(playlist.Playlist())
            
    def stop(self):
        self._player.stop()
        
    def quit(self):
        self._player.quit()

    def set_scheduler_callback(self, name, target):
        return self._scheduler.set_callback(name, target)

    def isplaying(self):
        return self._player.isplaying()
            
    def current_track_name(self):
        return self._player.filename()
    
    def current_track_posiotion(self):
        return self._player.percent_pos()
