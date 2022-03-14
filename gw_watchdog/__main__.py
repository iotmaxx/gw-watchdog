from gw_watchdog import modem
import datetime

if __name__ == '__main__':
    with open("/data/runtime",'w') as f:
        f.write(f"Run on: {datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'}")
    modem.checkModem()
