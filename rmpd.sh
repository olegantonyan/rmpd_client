#!/bin/bash

INSTAL_DIR=$(dirname $(readlink -f $0))
CONFIGFILE=$INSTAL_DIR/rmpd.conf
WORKDIR=$INSTAL_DIR
PIDFILE=$INSTAL_DIR/pidfile
PYTHON=python3

function start_rmpd {
    echo "Starting RMPD"
    $INSTAL_DIR/tools/clean_tmp.sh
    $INSTAL_DIR/tools/delete_large_logs.sh
    $PYTHON $INSTAL_DIR/main.py -d start -c $CONFIGFILE -w $WORKDIR -p $PIDFILE
}

function stop_rmpd {
    echo "Stopping RMPD"
    $PYTHON $INSTAL_DIR/main.py -d stop -p $PIDFILE
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
    killall -9 $PYTHON
    killall mplayer
    ;;
  configpath)
    echo $CONFIGFILE
    ;;
  *)
    echo "Usage: rmpd.sh {start|stop|restart|configpath}"
    exit 1
    ;;
esac

exit 0

