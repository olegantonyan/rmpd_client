# -*- coding: utf-8 -*-

from os import path, makedirs
from logging import getLogger

import mediaplayer.playerguard
import utils.config
import remotecontrol.protocoldispatcher
import utils.files

log = getLogger(__name__)


class PlayerController(object):
    '''
    High-level playback control
    '''

    def __init__(self):
        self.__player = mediaplayer.playerguard.PlayerGuard()
        self.__player.set_callbacks(onplay=self.__onplay_callback, onstop=self.__onstop_callback, onerror=self.__onerror_callback)
        self.__onplay_callback = None
        
    def __onplay_callback(self, **kwargs):
        log.debug("callback on play: " + kwargs["filename"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send_onplay(kwargs["filename"])
    
    def __onstop_callback(self, **kwargs):
        log.debug("callback on stop: " + kwargs["filename"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send_onstop(kwargs["filename"])
        
    def __onerror_callback(self, **kwargs):
        log.debug("callback on error: " + kwargs["filename"] + " : " + kwargs["message"])
        remotecontrol.protocoldispatcher.ProtocolDispatcher().send_onerror("{f} ({m})".format(m=kwargs["message"], f=kwargs["filename"]))
    
    def start_playlist(self):
        mediafiles_fullpath = utils.config.Config().mediafiles_path()
        if not path.exists(mediafiles_fullpath):
            makedirs(mediafiles_fullpath)
        
        playlist_fullpath = path.join(utils.config.Config().mediafiles_path(), "playlist.m3u")
        if path.exists(playlist_fullpath):
            remotecontrol.protocoldispatcher.ProtocolDispatcher().send_on_playlist_begin(utils.files.list_files_in_playlist(playlist_fullpath))
            self.__player.play_list(playlist_fullpath)
            
    def stop(self):
        self.__player.stop()
        
    def quit(self):
        self.__player.quit()
            
    def current_track_name(self):
        return self.__player.filename()
    
    def current_track_posiotion(self):
        return self.__player.percent_pos()
