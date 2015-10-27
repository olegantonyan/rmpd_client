#!/bin/sh

if [ -z "$1" ]; then
    LENGTH=30
else
    LENGTH=$1
fi

tr -cd '[:alnum:]' < /dev/urandom | fold -w$LENGTH | head -n1
