# -*- coding: utf-8 -*-

import x.global_daemon_wrapper as gdw


def _write(level, source, msg):
    return gdw.get().send({'type': 'log', 'message': msg, 'level': level, 'source': source})


def debug(source, msg):
    return _write('debug', source, msg)


def info(source, msg):
    return _write('info', source, msg)


def warning(source, msg):
    return _write('warning', source, msg)


def error(source, msg):
    return _write('error', source, msg)