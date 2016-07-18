# -*- coding: utf-8 -*-

import platform
import os

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


def free_space(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    # total = st.f_blocks * st.f_frsize
    # used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return free
