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
import logging
import os

def reenumerateUSB(usb='usb1'):
    logging.info('gw_watchdog: re-enumerate {usb}')
    with open(f'/sys/bus/usb/devices/{usb}/authorized', 'w') as f:
        f.write('0')
        f.flush()
        time.sleep(1)
        f.write('1')
        f.flush()

def logUSBInfoAndReboot():
    logging.info('USB devices:\n' + subprocess.run("lsusb", stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])
    os.system('reboot')

def checkModem():
    logging.basicConfig(filename="/data/gw-watchdog.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
    level = 0
    try:
        modemList = json.loads(subprocess.run("mmcli -J -L".split(), stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])['modem-list']
        if len(modemList) == 0:         # no modem available
            logging.info(f'gw_watchdog Level {level}: failed to detect modem')
            print("gw_watchdog: failed to detect modem, re-enumerate 1-1")
            level = 1
            reenumerateUSB('1-1')
        else:
            atiResponse = subprocess.run(['mmcli','-m',modemList[0],'--command=ATI'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            if not 'Quectel' in atiResponse:
                logging.info(f'gw_watchdog Level {level}: failed to communicate with modem')
                print("gw_watchdog: failed to communicate with modem, re-enumerate 1-1")
                level = 1
                reenumerateUSB('1-1')
#            print(atiResponse)
#            print(json.dumps(modemInfo,indent=4))
#            print('modem ok')
    except json.decoder.JSONDecodeError:
        # handler "error: couldn't create manager: Timeout was reached" response
        logging.info(f'gw_watchdog Level {level}: failed to parse mmcli response')
        print("gw_watchdog: failed to parse mmcli response, re-enumerate 1-1")
        level = 1
        reenumerateUSB('1-1')

    if level == 1:
        time.sleep(60)

        try:
            modemList = json.loads(subprocess.run("mmcli -J -L".split(), stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])['modem-list']
            if len(modemList) == 0:         # no modem available
                logging.info(f'gw_watchdog Level {level}: failed to detect modem')
                print("gw_watchdog: failed to detect modem, re-enumerate usb1")
                level = 2
                reenumerateUSB('usb1')
            else:
                atiResponse = subprocess.run(['mmcli','-m',modemList[0],'--command=ATI'], stdout=subprocess.PIPE).stdout.decode('utf-8')
                if not 'Quectel' in atiResponse:
                    logging.info(f'gw_watchdog Level {level}: failed to communicate with modem')
                    print("gw_watchdog: failed to communicate with modem, re-enumerate usb1")
                    level = 2
                    reenumerateUSB('usb1')
        except json.decoder.JSONDecodeError:
            # handler "error: couldn't create manager: Timeout was reached" response
            logging.info(f'gw_watchdog Level {level}: failed to parse mmcli response')
            print("gw_watchdog: failed to parse mmcli response, re-enumerate usb1")
            level = 2
            reenumerateUSB('usb1')
        
    if level == 2:
        time.sleep(60)

        try:
            modemList = json.loads(subprocess.run("mmcli -J -L".split(), stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1])['modem-list']
            if len(modemList) == 0:         # no modem available
                logging.info(f'gw_watchdog Level {level}: failed to detect modem')
                print("gw_watchdog: failed to detect modem, reboot")
                logUSBInfoAndReboot()
            else:
                atiResponse = subprocess.run(['mmcli','-m',modemList[0],'--command=ATI'], stdout=subprocess.PIPE).stdout.decode('utf-8')
                if not 'Quectel' in atiResponse:
                    logging.info(f'gw_watchdog Level {level}: failed to communicate with modem')
                    print("gw_watchdog: failed to communicate with modem, reboot")
                    logUSBInfoAndReboot()
        except json.decoder.JSONDecodeError:
            # handler "error: couldn't create manager: Timeout was reached" response
            logging.info(f'gw_watchdog Level {level}: failed to parse mmcli response')
            print("gw_watchdog: failed to parse mmcli response, reboot")
            logUSBInfoAndReboot()
        

