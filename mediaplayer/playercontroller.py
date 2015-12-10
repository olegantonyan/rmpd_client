# -*- coding: utf-8 -*-

import os
import logging

import mediaplayer.playlist.scheduler
import mediaplayer.player.watcher
import utils.config
import remotecontrol.protocoldispatcher as proto
import utils.files
import mediaplayer.playlist.loader as playlist_loader
import mediaplayer.playlist.playlist as playlist

log = logging.getLogger(__name__)


class PlayerController(object):
    def __init__(self):
        self._player = mediaplayer.player.watcher.Watcher()
        self._scheduler = mediaplayer.playlist.scheduler.Scheduler()
    
    def start_playlist(self):
        mediafiles_fullpath = utils.config.Config().mediafiles_path()
        if not os.path.exists(mediafiles_fullpath):
            os.makedirs(mediafiles_fullpath)
        
        playlist_fullpath = playlist_loader.Loader().filepath()
        if not os.path.exists(playlist_fullpath):
            log.error("playlist file '{f}' does not exists".format(f=playlist_fullpath))
            return

        proto.ProtocolDispatcher().send('playlist_begin',
                                        files=playlist_loader.Loader(playlist_fullpath).list_all_files())
        self._scheduler.set_playlist(playlist.Playlist())
            
    def stop(self):
        self._player.stop()
        
    def quit(self):
        self._player.quit()
            
    def current_track_name(self):
        return self._player.filename()
    
    def current_track_posiotion(self):
        return self._player.percent_pos()
