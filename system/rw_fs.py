# -*- coding: utf-8 -*-

import logging
import time

import utils.shell as shell
import hardware


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

    def _before_remount_to(self, mode):
        pass

    def _after_remount_to(self, mode):
        pass

    def _current_mode(self):
        (r, o, e) = shell.execute_shell('mount | grep "on {fs} type \w\+ (ro,"'.format(fs=self._fs))
        if len(o) > 0:
            return 'ro'
        return 'rw'

    def _remount_fs(self, mode='rw'):
        if hardware.platfrom.__name__ != 'raspberry':
            return True
        for i in range(10):
            log.info("remount {fs} {mode}".format(fs=self._fs, mode=mode))
            shell.execute('sudo sync')
            if mode == 'ro' and self._current_mode() == 'ro':
                log.info('fs is already read-only')
                return True
            if mode == 'rw' and self._current_mode() == 'rw':
                log.info('fs is already read-write')
                return True
            self._before_remount_to(mode)
            (r, o, e) = shell.execute("sudo mount -o remount,{mode} {fs}".format(mode=mode, fs=self._fs))
            self._after_remount_to(mode)
            if r == 0:
                return True
            else:
                log.error('fs remount failed: {e}\n{o}'.format(e=e, o=o))
                time.sleep(1)
                continue
        log.error("couldn't remount {fs} after 10 retries".format(fs=self._fs))
        return False


class Root(RwFs):
    def __init__(self):
        super().__init__('/')


class Storage(RwFs):
    def __init__(self, restart_player=True):
        super().__init__(self.path())
        self._restart_player = restart_player

    def _before_remount_to(self, mode):
        if mode == 'ro' and self._restart_player:
            self._player().stop()
            shell.execute('sudo sync')

    def _after_remount_to(self, mode):
        if mode == 'ro' and self._restart_player:
            self._player().start_playlist()

    def _player(self):
        import mediaplayer.playercontroller as playercontroller
        return playercontroller.PlayerController()

    @staticmethod
    def path():
        import utils.config as config
        return config.Config().storage_path()
