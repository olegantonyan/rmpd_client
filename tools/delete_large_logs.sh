#!/usr/bin/env bash

MAX_SIZE=1M

CONFIGFILE=$(dirname $(readlink -f $0))/../rmpd.conf
LOGFILE=$(awk -F "=" '/logfile/ {print $2}' $CONFIGFILE)
LOGDIR=$(dirname $LOGFILE)

write_log()
{
    echo "[`date`] $1" >> $LOGDIR/delete_large_logs.log
    echo $1
}

write_log "Checking for files larger than $MAX_SIZE in $LOGDIR"

files=$(find $LOGDIR -type f -size +$MAX_SIZE)

for f in $files
do
    write_log "Removing $f"
    rm $f
done

exit 0