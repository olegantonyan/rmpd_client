#!/bin/sh

/sbin/hwclock -r && /bin/ping -c1 google.com && /usr/sbin/ntpdate-debian && /bin/mount -o remount,rw / && /sbin/hwclock -w && /bin/mount -o remount,ro /

exit 0