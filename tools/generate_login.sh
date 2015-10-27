#!/bin/sh

#date | md5sum | cut -c1-7
< /dev/urandom tr -dc a-z0-9 | head -c${1:-7};echo;
