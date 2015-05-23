#!/bin/bash

INSTAL_DIR=$(dirname $(readlink -f $0))
CONFIGFILE=$INSTAL_DIR/rmpd.conf
WORKDIR=$INSTAL_DIR
PIDFILE=$INSTAL_DIR/pidfile

function start_rmpd {
    echo "Starting RMPD"
    $INSTAL_DIR/rmpd -d start -c $CONFIGFILE -w $WORKDIR -p $PIDFILE
}

function stop_rmpd {
    echo "Stopping RMPD"
    $INSTAL_DIR/rmpd -d stop -p $PIDFILE
}

case "$1" in
  start)
    start_rmpd
    ;;
  stop)
    stop_rmpd
    ;;
  restart)
    echo "Restarting RMPD"
    stop_rmpd
    sleep 1
    start_rmpd
    ;;
  kill)
    killall -9 rmpd
    killall mplayer
    ;;
  configpath)
    echo $CONFIGFILE
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|configpath}"
    exit 1
    ;;
esac

exit 0