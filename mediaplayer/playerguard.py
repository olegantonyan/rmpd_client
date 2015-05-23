#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from logging import getLogger
from os import path
from threading import Lock

log = getLogger(__name__)

import mediaplayer.wrapperplayer
import mediaplayer.playlist
import utils.singleton  # @UnusedImport
import utils.threads
import system.status

class PlayerGuard(object, metaclass=utils.singleton.Singleton):
    '''
    Guard for media player(s)
    '''

    def __init__(self):
        self.__onchange_lock = Lock()
        self.__player = mediaplayer.wrapperplayer.WrapperPlayer()
        self.__playlist = None
        self.__callbacks = None
        self.__check_status()
        
    def __wait_on_change_decorator(func):  # @NoSelf
        def wrap(self, *args):
            if self.isstopped(): #wait for poll __check_status
                sleep(2.5)
            self.__onchange_lock.acquire()
            result = func(self, *args)
            self.__onchange_lock.release()
            return result
        return wrap
    
    def __check_status(self):
        try:
            is_stopped = self.isstopped()
            if is_stopped and self.__playlist is not None:  
                log.debug("track finished, about to start a next one")
                self.__set_playing_status(False)
                try:
                    self.__callbacks["onstop"](filename=path.basename(self.__playlist.current()))
                except:
                    pass
                
                self.play(self.__playlist.next())
        except:
            log.exception("unhandled exception when checking status")
        finally:
            utils.threads.run_after_timeout(timeout=1.1, target=self.__check_status, daemon=True)
    
    def __set_playing_status(self, status):
        system.status.Status().playing = status
        
    def isstopped(self):
        return self.__player is not None and self.__player.isstopped()
        
    def set_callbacks(self, **kwargs):
        self.__callbacks = kwargs
        
    def play_list(self, playlist):
        log.info("start playlist '%s'", playlist)
        if not self.isstopped():
            self.stop()
        lst = mediaplayer.playlist.Playlist(playlist)
        self.play(lst.current())
        self.__playlist = lst
        #self.__playlist = mediaplayer.playlist.Playlist(playlist)
        #self.play(self.__playlist.current())
        
    def play(self, filename):
        log.info("start track '%s'", filename)
        if path.isfile(filename):
            self.__onchange_lock.acquire()
            self.__player.play(filename)
            retries = 0
            while self.isstopped():
                sleep(0.5)
                retries = retries + 1
                if retries > 10:
                    log.warning("reinitializing mplayer as it has probably crashed")
                    try:
                        self.__callbacks["onerror"](message="reinitializing mplayer as it has probably crashed", filename=path.basename(self.__playlist.pick_prev()))
                    except:
                        pass
                    del self.__player
                    self.__player = mediaplayer.wrapperplayer.WrapperPlayer()
                    self.__player.play(filename)
                    retries = 0
            self.__onchange_lock.release()
            if self.__playlist:
                self.__playlist.save_position()
            self.__set_playing_status(True)
            try:
                self.__callbacks["onplay"](filename=self.filename())
            except Exception:
                pass
        else:
            log.error("file '{f}' does not exists".format(f=filename))
            try:
                self.__callbacks["onerror"](message="file does not exists", filename=path.basename(filename))
            except:
                pass
        
    def pause(self):
        log.info("paused/resumed")
        self.__player.pause()
        
    def stop(self):
        log.info("stopped")
        self.__player.stop()
        try:
            self.__callbacks["onstop"](filename=path.basename(self.__playlist.current()))
        except Exception:
            pass
        self.__playlist = None
    
    @__wait_on_change_decorator    
    def time_pos(self):
        return self.__player.time_pos()
    
    @__wait_on_change_decorator
    def percent_pos(self):
        return self.__player.percent_pos()
    
    @__wait_on_change_decorator
    def filename(self):
        return self.__player.filename()
    
    @__wait_on_change_decorator
    def length(self):
        return self.__player.length()
        
    def quit(self):
        self.__player.quit()
        del self.__player
        
    
