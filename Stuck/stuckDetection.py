import sys
sys.append.path("/home/pi/git/kimuralab/SensorModuleTest/BMX055")
sys.append.path("/home/pi/git/kimuralab/SensorModuleTest/GPS")
sys.append.path("/home/pi/git/kimuralab/SensorModuleTest/Motor")
sys.append.path("/home/pi/git/kimuralab/Other")

import pigpio
import time
import traceback

import BMX055
import GPS
import Other


if __name__ == "__main__":
    try:
    except KeyboardInterrupt:
    except:
        print(traceback.format_exc())