import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')

import time
import numpy as np
import difflib
import pigpio
import binascii
import traceback

import BMX055
import Motor
import Other


if __name__ == "__main__":
	try:
		spinGoal = -200.00
		mP = 0.00
		e = 0.00
		e1 = 0.00
		e2 = 0.00
		Kp = 0.7
		Ki = 0.3
		Kd = 0.5
		spinZ = 0
		while 1:
			bmx055data = BMX055.bmx055_read()
			spinZ = bmx055data[5]
			e1 = e
			e2 = e1
			e =  spinZ - spinGoal
			mP = mP + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
			print(mP, spinZ)
			if spinGoal < 0:
				mP = mP if mP <= 50 else 50
				if mP < 0:
					mP = 20
			else:
				mP = mP if mP >= -50 else -50
				if mP > 0:
					mP = -20
			#print(spinZ, mP)
			a = Motor.motor(mP, 0)
			#time.sleep(0.001)
			#print(a, mP, spinZ)

	except  KeyboardInterrupt:
		Motor.motor_stop()
	except:
		Motor.motor_stop()
		print(traceback.format_exc())
