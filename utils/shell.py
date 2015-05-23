#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from os import getcwd

def execute(cli, cwd=getcwd()):
    popen_cli = filter(lambda x : True if len(x) > 0 else False, cli.split(" "))
    process = Popen(popen_cli, stdout=PIPE, stderr=PIPE, cwd=cwd)
    out, err = process.communicate()
    return (process.returncode, out, err)