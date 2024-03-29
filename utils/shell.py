# -*- coding: utf-8 -*-

import subprocess
import os


def execute(cli, cwd=os.getcwd()):
    popen_cli = filter(lambda x: True if len(x) > 0 else False, cli.split(" "))
    process = subprocess.Popen(popen_cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = process.communicate()
    return process.returncode, out.decode('utf-8') if out else '', err.decode('utf-8') if err else ''


def execute_shell(cli, cwd=os.getcwd()):
    process = subprocess.Popen(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True)
    out, err = process.communicate()
    return process.returncode, out.decode('utf-8') if out else '', err.decode('utf-8') if err else ''


def execute_child_pid(cli, cwd=os.getcwd()):
    popen_cli = filter(lambda x: True if len(x) > 0 else False, cli.split(" "))
    process = subprocess.Popen(popen_cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = process.communicate()
    return process.returncode, out.decode('utf-8') if out else '', err.decode('utf-8') if err else '', process.pid