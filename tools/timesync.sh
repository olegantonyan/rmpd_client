#!/bin/bash

/sbin/hwclock -r || /bin/ping -c1 google.com && /usr/sbin/ntpdate-debian

exit 0