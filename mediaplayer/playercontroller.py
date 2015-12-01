# -*- coding: utf-8 -*-

import os
import logging

import mediaplayer.playerguard
import utils.config
import remotecontrol.protocoldispatcher as proto
import utils.files
import utils.singleton
import mediaplayer.playlist.loader as pl

log = logging.getLogger(__name__)


class PlayerController(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self._player = mediaplayer.playerguard.PlayerGuard(onplay=self._onplay_callback,
                                                           onstop=self._onstop_callback,
                                                           onerror=self._onerror_callback)
    
    def start_playlist(self):
        mediafiles_fullpath = utils.config.Config().mediafiles_path()
        if not os.path.exists(mediafiles_fullpath):
            os.makedirs(mediafiles_fullpath)
        
        playlist_fullpath = pl.Loader().filepath()
        if not os.path.exists(playlist_fullpath):
            log.error("playlist file '{f}' does not exists".format(f=playlist_fullpath))
            return

        proto.ProtocolDispatcher().send('playlist_begin',
                                        files=pl.Loader(playlist_fullpath).list_all_files())
        self._player.play_list()
            
    def stop(self):
        self._player.stop()
        
    def quit(self):
        self._player.quit()
            
    def current_track_name(self):
        return self._player.filename()
    
    def current_track_posiotion(self):
        return self._player.percent_pos()

    def _onplay_callback(self, **kwargs):
        log.debug("callback on play: " + kwargs["filename"])
        proto.ProtocolDispatcher().send('track_begin', **kwargs)

    def _onstop_callback(self, **kwargs):
        log.debug("callback on stop: " + kwargs["filename"])
        proto.ProtocolDispatcher().send('track_end', **kwargs)

    def _onerror_callback(self, **kwargs):
        log.debug("callback on error: " + kwargs["filename"] + " : " + kwargs["message"])
        proto.ProtocolDispatcher().send('playback_error', **kwargs)
