""" 
gw-watchdog - Gateway watchdog
Copyright (C) 2021 IoTmaxx GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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