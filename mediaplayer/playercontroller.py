# -*- coding: utf-8 -*-

import os
import logging

import mediaplayer.playerguard
import utils.config
import remotecontrol.protocoldispatcher
import utils.files
import utils.singleton
import mediaplayer.playlist

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
        
        playlist_fullpath = mediaplayer.playlist.full_filepath()
        if not os.path.exists(playlist_fullpath):
            log.error("playlist file '{f}' does not exists".format(f=playlist_fullpath))
            return

        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('playlist_begin',
                                                                   files=utils.files.list_files_in_playlist(playlist_fullpath))
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
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('track_begin', **kwargs)

    def _onstop_callback(self, **kwargs):
        log.debug("callback on stop: " + kwargs["filename"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('track_end', **kwargs)

    def _onerror_callback(self, **kwargs):
        log.debug("callback on error: " + kwargs["filename"] + " : " + kwargs["message"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('playback_error', **kwargs)
