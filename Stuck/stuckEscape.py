import sys
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/BMX055")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/GPS")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/Motor")
sys.path.append("/home/pi/git/kimuralab/Other")

import pigpio
import time
import traceback

import BMX055
import GPS
import Motor
import Other


def fuckingRun(mP, thd):
	suminit = 0
	count = 0
	for i in range(5):
		bmxinit = BMX055.bmx055_read()
		print(i, "init:", bmxinit[0:6])
		suminit = suminit + bmxinit[5]
	aveinit = suminit / 5
	print('aveinit', aveinit)
	Motor.motor(-mP, mP, 1)
	for i in range(20):
		bmxnow = BMX055.bmx055_read()
		print(i, "now:", bmxnow[0:6])
		if bmxnow[5] - aveinit < thd:
			count = count + 1
			print('count', count)
			if count > 5:
				print("stack")
				Motor.motor(0, 0, 2)
				return 1
		else:
			count = 0
	time.sleep(1)
	Motor.motor(0, 0, 2)
	return 0

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()
		stuckFlug = fuckingRun(50, 100)
		if stuckFlug == 1:
			Motor.motor(20, 20, 1)
			Motor.motor(-20, -20, 1)
			Motor.motor(20, -20, 1)
			Motor.motor(-20, 20, 1)
			Motor.motor(0, 0, 2)
	except KeyboardInterrupt:
		Motor.motor_stop()
		print("Emergency!")
		#GPS.closeGPS()
	except:
		Motor.motor_stop()
		#GPS.closeGPS()
		print(traceback.format_exc())
