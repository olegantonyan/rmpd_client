#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform

import version

def linux_disto():
    return platform.linux_distribution()

def user_agent():
    return "rmpd {v} ({s}, {m}, {p}, {cpu}, python {py}, {di} {div})".format(v=version.VERSION,
                                                          s=platform.system(),
                                                          m=platform.machine(),
                                                          p=platform.platform(),
                                                          cpu=platform.processor(),
                                                          py=platform.python_version(),
                                                          di=linux_disto()[0],
                                                          div=linux_disto()[1])
    