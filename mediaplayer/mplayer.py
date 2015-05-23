#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mplayer import Player, CmdPrefix

import utils.config

class MPlayer(object):
    '''
    Wrapper class wor MPlayer
    '''
    
    SEEK_MODE_SECONDS_RELATIVE = 0
    SEEK_MODE_PERCENTS_ABSOLUTE = 1
    SEEK_MODE_SECONDS_ABSOLUTE = 2

    def __init__(self):
        Player.cmd_prefix = CmdPrefix.PAUSING_KEEP
        if utils.config.Config().mplayer_executable() is not None:
            Player.exec_path = utils.config.Config().mplayer_executable()
        self.__player = Player()
        self.__player.args = ['-really-quiet', '-msglevel', 'global=6']
   
    def __del__(self):
        self.__player.quit()
        
    def isstopped(self):
        return self.__player is not None and self.filename() is None and self.length() is None
    
    def play_list(self, playlist):
        self.__player.loadlist(playlist)
        
    def play(self, filename):
        self.__player.loadfile(filename)
        self.fullscreen(True)
            
    def pause(self):
        self.__player.pause()
        
    def stop(self):
        self.__player.stop()
        
    def seek(self, value, seek_mode=SEEK_MODE_SECONDS_RELATIVE):
        self.__player.seek(seek_mode, value)
        
    def fullscreen(self, value):
        self.__player.vo_fullscreen(1 if value else 0)
        
    def time_pos(self):
        d =  self.__player.time_pos
        if d is None:
            return self.__player.time_pos
        return d
    
    def percent_pos(self):
        d = self.__player.percent_pos
        if d is None:
            return self.__player.percent_pos
        return d
    
    def path(self):
        d = self.__player.path
        if d is None:
            return self.__player.path
        return self.__player.path
    
    def filename(self):
        d = self.__player.filename
        if d is None:
            return self.__player.filename
        return d
        
    def loop(self, value):
        self.__player.loop = value
        
    def length(self):
        d = self.__player.length
        if d is None:
            return self.__player.length
        return d
        