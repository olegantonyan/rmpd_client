# -*- coding: utf-8 -*-

import logging

import utils.shell as shell


log = logging.getLogger(__name__)


class RwFs(object):
    def __init__(self, fs):
        self._fs = fs
        self._need_remount_back = True

    def __enter__(self):
        if self._current_mode() == 'rw':
            self._need_remount_back = False
            return True
        return self._remount_fs('rw')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._need_remount_back:
            return True
        self._remount_fs('ro')

    def _current_mode(self):
        (r, o, e) = shell.execute_shell('mount | grep "on {fs} type \w\+ (ro,"'.format(fs=self._fs))
        if len(o) > 0:
            return 'ro'
        return 'rw'

    def _remount_fs(self, mode='rw'):
        log.debug("remount {fs} {mode}".format(fs=self._fs, mode=mode))
        if mode == 'ro' and self._current_mode() == 'ro':
            log.debug('fs is already read-only')
            return True
        if mode == 'rw' and self._current_mode() == 'rw':
            log.debug('fs is already read-write')
            return True
        (r, o, e) = shell.execute("sudo mount -o remount,{mode} {fs}".format(mode=mode, fs=self._fs))
        if r != 0:
            log.error('fs remount failed: {e}\n{o}'.format(e=e, o=o))
        return r == 0


class Root(RwFs):
    def __init__(self):
        super().__init__('/')


class Storage(RwFs):
    def __init__(self):
        super().__init__('/var')
