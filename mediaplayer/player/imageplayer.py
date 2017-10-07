# -*- coding: utf-8 -*-

import time
import os

import system.wallpaper as wallpaper
import xmain
import utils.threads as threads


class ImagePlayer(object):
    def __init__(self):
        self._stop_flag = False
        self._seek_position = 0
        self._max_duration = 0
        self._started = False
        self._filename = None
        self._timer_thread = threads.run_in_thread(self._timer_loop)

    def __del__(self):
        self._stop_flag = True

    def isstopped(self):
        return not self._started

    def play(self, filename, start_position=0, show_duration=0):
        self._max_duration = show_duration
        self._seek_position = start_position
        self._started = True
        self._filename = filename
        xmain.send({'type': 'show_image', 'path': filename})

    def stop(self):
        self._finished()
        xmain.send({'type': 'show_image', 'path': None})

    def seek(self, value):
        self._seek_position = value

    def time_pos(self):
        return self._seek_position

    def percent_pos(self):
        tm = self.time_pos()
        ln = self.length()
        if tm == 0 or ln == 0 or not self._started:
            return 0
        return round(tm * 100 / ln)

    def filename(self):
        return os.path.basename(str(self._filename))

    def length(self):
        return self._max_duration

    def _finished(self):
        self._started = False
        self._seek_position = 0
        self._max_duration = 0
        threads.run_after_timeout(5, self._deadband_timeout)

    def _timer_loop(self):
        while not self._stop_flag:
            time.sleep(1)
            if self._started:
                self._seek_position += 1
                if self._seek_position >= self._max_duration:
                    self._finished()

    def _deadband_timeout(self):
        if not self._started:
            wallpaper.Wallpaper().load()
