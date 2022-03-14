#!/bin/python

import subprocess
import json
import time

def reenumerateUSB(usb=1):
    with open(f'/sys/bus/usb/devices/usb{usb}/authorized', 'w') as f:
        f.write('0')
        f.flush()
        time.sleep(1)
        f.write('1')
        f.flush()

def checkModem():
    modemList = json.loads(subprocess.run("mmcli -J -L".split(), stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])['modem-list']
    if len(modemList) == 0:         # no modem available
        print("gw_watchdog: failed to detect modem, re-enumerate USB1")
        reenumerateUSB()
#    else:
#        print('modem ok')