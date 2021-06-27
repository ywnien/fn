#!/usr/bin/env python
from contextlib import contextmanager
import json
import os
from subprocess import DEVNULL, PIPE, Popen


with open("json/config.json", "r") as f:
    xconfig = json.load(f)["path"]["xlaunch"]

@contextmanager
def xlaunch(path=xconfig):
    """
    Starts XLaunch by "config.xlaunch"

    The config must check "disable access control".
    
    `xlaunch()` is context manager. return `None`.
    
    args:

      - path - the path of "config.xlaunch"

    usage:
    
        `with xlaunch():`
    """
    try:
        running = _running_check("vcxsrv")

        if running == True:
            pass
        else:
            os.system('powershell.exe "%s"' % path)

        yield None

    finally:
        os.system("powershell.exe 'Stop-Process -name vcxsrv'")

def _running_check(name: str) -> bool:
    command = f"powershell.exe Get-Process -name {name}"
    proc = Popen(command, shell=True, stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode("ascii")

    if output.find(name) == -1:
        return False
    else:
        return True
    

def win_open(file: str):
    """
    Opens file with default program from WSL2.

    args:

        - file - The full path of the file.
    """
    os.system("""powershell.exe '$file = "%s" ; & $file'""" % file)