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
from gw_watchdog import modem
import datetime

if __name__ == '__main__':
    with open("/data/runtime",'w') as f:
        f.write(f"Run on: {datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'}")
    modem.checkModem()
