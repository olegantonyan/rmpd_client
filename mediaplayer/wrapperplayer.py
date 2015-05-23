#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

import mediaplayer.mplayer
import mediaplayer.pyomxplayer.pyomxplayer
import hardware
import utils.config

class WrapperPlayer(object):
    def __init__(self):
        self.__mplayer = mediaplayer.mplayer.MPlayer()
        self.__omxplayer = mediaplayer.pyomxplayer.pyomxplayer.OMXPlayer()
        if utils.config.Config().omplayer_executable() is not None:
            self.__omxplayer.exec_path = utils.config.Config().omplayer_executable()
        if utils.config.Config().omplayer_arguments() is not None:
            self.__omxplayer.args = utils.config.Config().omplayer_arguments()
        
    def __del__(self):
        del self.__mplayer
        del self.__omxplayer
        
    def quit(self):
        self.__omxplayer.quit()
        del self.__mplayer
        del self.__omxplayer
    
    def __player(self, filename=None):
        if not filename:
            if hardware.platfrom.__name__ == 'raspberry' and not self.__omxplayer.isstopped():
                return self.__omxplayer
            return self.__mplayer
        elif self.isvideo(filename) and hardware.platfrom.__name__ == 'raspberry':
            return self.__omxplayer
        return self.__mplayer
    
    def isvideo(self, filename):
        ext = path.splitext(filename)[1].replace('.','')
        if ext in ['mkv', 'mp4', 'avi', 'mpeg2', 'mov', 'mpg']:
            return True
        return False
        
    def play(self, filename):
        return self.__player(filename).play(filename)
    
    def pause(self):
        return self.__player().pause()
    
    def stop(self):
        return self.__player().stop()
    
    def isstopped(self):
        return self.__player().isstopped()
    
    def time_pos(self):
        return self.__player().time_pos()
    
    def percent_pos(self):
        return self.__player().percent_pos()
    
    def filename(self):
        return self.__player().filename()
    
    def length(self):
        return self.__player().length()
    
        