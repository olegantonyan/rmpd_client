#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from sys import stdout, exit
from logging import basicConfig, getLogger, StreamHandler, Formatter, info, DEBUG, INFO, warning, debug, critical
from logging.handlers import RotatingFileHandler
from optparse import OptionParser
from traceback import format_exc
from signal import signal, SIGTERM
from os import chdir, getcwd

import mediaplayer.playercontroller
import remotecontrol.protocoldispatcher
import utils.config
import utils.daemon
import utils.threads
import webui.webui
import hardware
import system.watchdog


def signal_handler(signum, frame):
    mediaplayer.playercontroller.PlayerController().quit()
    hardware.platfrom.set_all_leds_disabled()
    warning("terminated")
    exit(0)


def setup_logger(console_app=False, verbose_log=False):
    basicConfig(filename=utils.config.Config().logfile(),
                format="[%(asctime)s] %(name)s |%(levelname)s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                level=(DEBUG if (verbose_log or utils.config.Config().verbose_logging()) else INFO))

    log_handler = RotatingFileHandler(utils.config.Config().logfile(), mode='a', maxBytes=4*1024*1024,
                                      backupCount=2, encoding=None, delay=0)
    log = getLogger()
    log.addHandler(log_handler)

    if console_app:
        root_logger = getLogger()
        child_logger = StreamHandler(stdout)
        child_logger.setLevel(DEBUG)
        formatter = Formatter("[%(asctime)s] %(name)s |%(levelname)s| %(message)s", "%Y-%m-%d %H:%M:%S")
        child_logger.setFormatter(formatter)
        root_logger.addHandler(child_logger)
        info("started as console application")
    else:
        info("started as daemon")


def bootstrap(configfile, console_app=False, verbose_log=False):
    utils.config.Config(configfile)
    setup_logger(console_app, verbose_log)
    info("using config file: '{c}'".format(c=configfile))
    debug("working directory: '{w}'".format(w=getcwd()))
    signal(SIGTERM, signal_handler)


def app():
    player = mediaplayer.playercontroller.PlayerController()
    player.start_playlist()
    proto = remotecontrol.protocoldispatcher.ProtocolDispatcher()
    utils.threads.run_in_thread(webui.webui.start, ['0.0.0.0', 8080])
    while True:
        track = player.current_track_name()
        pos = player.current_track_posiotion()
        proto.send('now_playing', track=track, percent_position=pos)
        system.watchdog.Watchdog().feed()
        sleep(20)


class DaemonApp(utils.daemon.Daemon):
    def set_working_dir(self, cwd):
        self.__cwd = cwd

    def run(self):
        try:
            chdir(self.__cwd)
            debug("daemon working directory: '{w}'".format(w=getcwd()))
            app()
        except Exception as e:
            critical("fatal: unhandled exception\n{e}\n{t}".format(e=str(e), t=format_exc()))


def main():
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="configfile", help="path to configration file")
    parser.add_option("-w", "--working-dir", dest="workingdir", help="working directory in daemon mode")
    parser.add_option("-p", "--pid-file", dest="pidfile", help="path to pid file (only for daemon mode with -d option)")
    parser.add_option("-t", "--console-app", action="store_true", dest="console_app", help="run program as a console app instead of daemon")
    parser.add_option("-d", "--daemon-contol", dest="daemon_control", help="run program as a console app instead of daemon")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="enable verbose logging")

    (opts, args) = parser.parse_args()

    if opts.console_app:
        bootstrap(opts.configfile if opts.configfile else "rmpd.conf",
                  True,
                  opts.verbose)
        exit(app())
    else:
        if not opts.pidfile:
            parser.error("no pid file specified for daemon mode")
            exit(2)

        daemon = DaemonApp(opts.pidfile)
        if 'start' == opts.daemon_control:
            if not opts.configfile:
                parser.error("no config file specified")
                exit(2)
            if not opts.workingdir:
                parser.error("no working directory specified in daemon mode")
                exit(2)
            chdir(opts.workingdir)  # in main app context
            daemon.set_working_dir(opts.workingdir)
            bootstrap(opts.configfile, False, opts.verbose)
            daemon.start()
        elif 'stop' == opts.daemon_control:
            daemon.stop()
        elif 'status' == opts.daemon_control:
            daemon.status()
        elif not opts.daemon_control:
            parser.error("no daemon control options specified, try start or stop".format(opts.daemon_control))
            exit(2)
        else:
            parser.error("unknown daemon control command '{}'".format(opts.daemon_control))
            exit(2)
        exit(0)

if __name__ == '__main__':
    main()
