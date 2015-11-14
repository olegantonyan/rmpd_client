#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os


def execute(cli, cwd=os.getcwd()):
    popen_cli = filter(lambda x: True if len(x) > 0 else False, cli.split(" "))
    process = subprocess.Popen(popen_cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = process.communicate()
    return process.returncode, out, err
