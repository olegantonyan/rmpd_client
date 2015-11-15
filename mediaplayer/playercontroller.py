# -*- coding: utf-8 -*-

import os
import logging

import mediaplayer.playerguard
import utils.config
import remotecontrol.protocoldispatcher
import utils.files

log = logging.getLogger(__name__)


class PlayerController(object):
    def __init__(self):
        self.__player = mediaplayer.playerguard.PlayerGuard()
        self.__player.set_callbacks(onplay=self.__onplay_callback,
                                    onstop=self.__onstop_callback,
                                    onerror=self.__onerror_callback)
        self.__onplay_callback = None
        
    def __onplay_callback(self, **kwargs):
        log.debug("callback on play: " + kwargs["filename"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('track_begin', **kwargs)
    
    def __onstop_callback(self, **kwargs):
        log.debug("callback on stop: " + kwargs["filename"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('track_end', **kwargs)
        
    def __onerror_callback(self, **kwargs):
        log.debug("callback on error: " + kwargs["filename"] + " : " + kwargs["message"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send('playback_error', **kwargs)
    
    def start_playlist(self):
        mediafiles_fullpath = utils.config.Config().mediafiles_path()
        if not os.path.exists(mediafiles_fullpath):
            os.makedirs(mediafiles_fullpath)
        
        playlist_fullpath = os.path.join(utils.config.Config().mediafiles_path(), "playlist.m3u")
        if os.path.exists(playlist_fullpath):
            remotecontrol.protocoldispatcher.ProtocolDispatcher().send('playlist_begin',
                                                                       files=utils.files.list_files_in_playlist(playlist_fullpath))
            self.__player.play_list(playlist_fullpath)
            
    def stop(self):
        self.__player.stop()
        
    def quit(self):
        self.__player.quit()
            
    def current_track_name(self):
        return self.__player.filename()
    
    def current_track_posiotion(self):
        return self.__player.percent_pos()
