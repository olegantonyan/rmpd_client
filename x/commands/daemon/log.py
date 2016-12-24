# -*- coding: utf-8 -*-

import logging

import x.commands.daemon.base_command as base_command


class Log(base_command.BaseCommand):
    def call(self):
        log = logging.getLogger(self._data['source'])
        level = self._data['level']
        msg = self._data['message']
        if level == 'debug':
            log.debug(msg)
        elif level == 'info':
            log.info(msg)
        elif level == 'warning':
            log.warning(msg)
        elif level == 'error':
            log.error(msg)
