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
import Motor
import Other


def fuckingRun(mP, accy_thd):
	Motor.motor(mP, mP, 3)
	bmx055Data = BMX055.bmx055_read()
	Motor.motor(0, 0, 2)
	if abs(bmx055Data[1]) < accy_thd:
		Motor.motor(-mP, -mP, 3)
		Motor.motor(mP, -mP, 3)
		Motor.motor(-mP, mP, 3)
		Motor.motor(0, 0, 2)

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()
		fucking(30, 50)
	except KeyboardInterrupt:
		Motor.motor_stop()
		print("Emergency!")
		#GPS.closeGPS()
	except:
		Motor.motor_stop()
		#GPS.closeGPS()
		print(traceback.format_exc())