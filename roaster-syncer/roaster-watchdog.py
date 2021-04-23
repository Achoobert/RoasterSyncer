#!/usr/bin/python3

# raspberrypi_roaster will update a file .rpi_roaster every minute

# if the file isn't updated for 5 minutes then this watchdog
# will kill any existing raspberyypi_roaster process
# and restart it

import os
import psutil
import time
import subprocess

def statusfile_too_old():
    if not os.path.exists(".rpi_roaster"):
        return True
    current_time = time.time()
    mtime = os.path.getmtime(".rpi_roaster")

    if current_time - mtime > 300:
        return True
    else:
        return False

def kill_all_rp_roaster():
    for proc in psutil.process_iter():
        # print("checking", proc.cmdline())
        # check whether the process name matches
        if "raspberrypi_roaster.py" in proc.cmdline() or "./raspberrypi_roaster.py" in proc.cmdline():
            proc.kill()

def restart_rp_roaster():
    subprocess.Popen(["python3", "./raspberrypi_roaster.py"])


def check_statusfile():
    if statusfile_too_old():
        kill_all_rp_roaster()
        restart_rp_roaster()