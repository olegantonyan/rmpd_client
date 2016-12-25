#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import logging
import optparse
import traceback
import signal
import os

import mediaplayer.playercontroller as playercontroller
import remotecontrol.protocoldispatcher as protocoldispatcher
import utils.config as config
import utils.daemon as daemon
import utils.threads as threads
import webui.webui as webui
import hardware
import system.watchdog as watchdog
import clockd.clockd as clockd
import system.wallpaper as wallpaper
import hdmihotplug.hdmihotplug as hdmihotplug
import utils.files as files
import system.rw_fs as rw_fs
import xmain


def signal_handler(signum, frame):
    logging.info("caught signal {s}".format(s=signum))
    playercontroller.PlayerController().quit()
    hardware.platfrom.set_all_leds_disabled()
    logging.warning("terminated")
    sys.exit(0)


def setup_logger(console_app=False, verbose_log=False):
    logfile = config.Config().logfile()
    logdir = os.path.dirname(logfile)
    if hardware.platfrom.__name__ == 'raspberry':
        files.mkdir(logdir)
    logging.basicConfig(filename=logfile,
                        format="[%(asctime)s] %(name)s |%(levelname)s| %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=(logging.DEBUG if (verbose_log or config.Config().verbose_logging()) else logging.INFO))

    if console_app:
        root_logger = logging.getLogger()
        child_logger = logging.StreamHandler(sys.stdout)
        child_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(name)s[%(threadName)s/%(thread)d] |%(levelname)s| %(message)s", "%Y-%m-%d %H:%M:%S")
        child_logger.setFormatter(formatter)
        root_logger.addHandler(child_logger)
        logging.info("started as console application")
    else:
        logging.info("started as daemon")


def bootstrap(configfile, console_app=False, verbose_log=False):
    config.Config().set_configfile(configfile)
    setup_logger(console_app, verbose_log)
    logging.info("using config file: '{c}'".format(c=configfile))
    logging.debug("working directory: '{w}'".format(w=os.getcwd()))
    signal.signal(signal.SIGTERM, signal_handler)


# def resolution_changed():
#    xmain.restart()
#    wallpaper.Wallpaper().load()


def app():
    hardware.platfrom.fix_file_permissions('/tmp')
    with rw_fs.Storage(restart_player=False):
        hardware.platfrom.fix_file_permissions(config.Config().storage_path())

    xmain.start()
    wallpaper.Wallpaper().load()

    if config.Config().enable_clockd():
        threads.run_in_thread(clockd.Clockd().run)

    # threads.run_in_thread(hdmihotplug.HdmiHotplug(onchange_callback=resolution_changed).run)

    player = playercontroller.PlayerController()
    player.start_playlist()

    proto = protocoldispatcher.ProtocolDispatcher()

    threads.run_in_thread(webui.start, ['0.0.0.0', 8080])
    while True:
        track = player.current_track_name()
        pos = player.current_track_posiotion()
        proto.send('now_playing', track=track, percent_position=pos)
        watchdog.Watchdog().feed()
        time.sleep(20)


class DaemonApp(daemon.Daemon):
    def set_working_dir(self, cwd):
        self.cwd = cwd

    def run(self):
        try:
            if self.cwd is not None:
                os.chdir(self.cwd)
            logging.debug("daemon working directory: '{w}'".format(w=os.getcwd()))
            app()
        except Exception as e:
            logging.critical("fatal: unhandled exception\n{e}\n{t}".format(e=str(e), t=traceback.format_exc()))


def main():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config-file", dest="configfile", help="path to configration file")
    parser.add_option("-w", "--working-dir", dest="workingdir", help="working directory in daemon mode")
    parser.add_option("-p", "--pid-file", dest="pidfile", help="path to pid file (only for daemon mode with -d option)")
    parser.add_option("-t", "--console-app", action="store_true", dest="console_app", help="run program as a console app instead of daemon")
    parser.add_option("-d", "--daemon-contol", dest="daemon_control", help="run program as a console app instead of daemon")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="enable verbose logging")

    (opts, args) = parser.parse_args()

    if opts.console_app:
        if opts.workingdir:
            os.chdir(opts.workingdir)
        bootstrap(opts.configfile if opts.configfile else "rmpd.conf", True, opts.verbose)
        sys.exit(app())
    else:
        if not opts.pidfile:
            parser.error("no pid file specified for daemon mode")
            sys.exit(2)

        daemonapp = DaemonApp(opts.pidfile)
        if 'start' == opts.daemon_control:
            if not opts.configfile:
                parser.error("no config file specified")
                sys.exit(2)
            if not opts.workingdir:
                parser.error("no working directory specified in daemon mode")
                sys.exit(2)
            os.chdir(opts.workingdir)  # in main app context
            daemonapp.set_working_dir(opts.workingdir)
            bootstrap(opts.configfile, False, opts.verbose)
            daemonapp.start()
        elif 'stop' == opts.daemon_control:
            daemonapp.stop()
        elif 'status' == opts.daemon_control:
            daemonapp.status()
        elif not opts.daemon_control:
            parser.error("no daemon control options specified, try start or stop".format(opts.daemon_control))
            sys.exit(2)
        else:
            parser.error("unknown daemon control command '{}'".format(opts.daemon_control))
            sys.exit(2)
        sys.exit(0)

if __name__ == '__main__':
    main()
