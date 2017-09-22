#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import logging
import logging.handlers
import optparse
import signal
import os

import mediaplayer.playercontroller as playercontroller
import remotecontrol.protocoldispatcher as protocoldispatcher
import utils.config as config
import utils.threads as threads
import webui.webui as webui
import hardware
import system.watchdog as watchdog
import clockd.clockd as clockd
import system.wallpaper as wallpaper
# import hdmihotplug.hdmihotplug as hdmihotplug
import utils.files as files
import system.rw_fs as rw_fs
import xmain
import networkd.networkd as networkd


def signal_handler(signum, _):
    logging.info("caught signal {s}".format(s=signum))
    xmain.stop()
    playercontroller.PlayerController().quit()
    hardware.platfrom.set_all_leds_disabled()
    logging.warning("terminated")
    sys.exit(0)


def setup_logger(verbose_log=False):
    logfile = config.Config().logfile()
    if hardware.platfrom.__name__ == 'raspberry':
        files.mkdir(os.path.dirname(logfile))

    root_logger = logging.getLogger()
    rotating_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=2097152, backupCount=5)
    root_logger.setLevel(logging.DEBUG if (verbose_log or config.Config().verbose_logging()) else logging.INFO)
    child_logger = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] %(name)s[%(threadName)s/%(thread)d] |%(levelname)s| %(message)s", "%Y-%m-%d %H:%M:%S")
    child_logger.setFormatter(formatter)
    rotating_handler.setFormatter(formatter)
    root_logger.addHandler(rotating_handler)
    root_logger.addHandler(child_logger)
    logging.info("started")


def bootstrap(configfile, verbose_log=False):
    hardware.platfrom.initialize()
    config.Config().set_configfile(configfile)
    setup_logger(verbose_log)
    logging.info("using config file: '{c}'".format(c=configfile))
    logging.info("working directory: '{w}'".format(w=os.getcwd()))
    signal.signal(signal.SIGTERM, signal_handler)


def app():
    with rw_fs.Storage(restart_player=False):
        hardware.platfrom.fix_file_permissions(config.Config().storage_path())

    xmain.start()
    wallpaper.Wallpaper().load()

    if config.Config().enable_clockd():
        threads.run_in_thread(clockd.Clockd().run)

    # threads.run_in_thread(networkd.Networkd().run)

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


def main():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config-file", dest="configfile", help="path to configration file")
    parser.add_option("-w", "--working-dir", dest="workingdir", help="working directory")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="enable verbose logging")

    (opts, args) = parser.parse_args()

    if opts.workingdir:
        os.chdir(opts.workingdir)
    bootstrap(opts.configfile if opts.configfile else "rmpd.conf", opts.verbose)
    try:
        sys.exit(app())
    except KeyboardInterrupt:
        logging.warning('caught KeyboardInterrupt')
        xmain.stop()
        raise


if __name__ == '__main__':
    main()
