#!/usr/bin/env bash

if [ -z "$1" ]; then
   echo "You have to specify distribution path as a first argument"
   exit 1
fi
DIST=$1

if [ -z "$2" ]; then
   echo "You have to specify host's IP address as a second argument"
   exit 1
fi
HOST=$2

if [ -z "$3" ]; then
   echo "You have to specify password as a third argument"
   exit 1
fi
PASSWORD=$3

if [ -z "$4" ]; then
    PORT=22
else
    PORT=$4
fi

sshpass -p $PASSWORD scp -P $PORT $1 rmpd@$2:/tmp && sshpass -p $PASSWORD ssh rmpd@$2 -p $PORT "sudo mount -o remount,rw / && cd /tmp && sudo tar -xvf $(basename $DIST) -C /home/rmpd/ && sync"

exit $?