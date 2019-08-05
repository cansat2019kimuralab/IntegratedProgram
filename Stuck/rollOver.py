# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/Other')

import pigpio
import time
import traceback

import BMX055
import Motor
import Stuck

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()
		flug = 0
		count = 0
		while flug <= 5:
			# --- Restart --- #
			if(count == 0):
				Motor.motor(0, 0, 2)
				Motor.motor(40, 40, 2)
				Motor.motor(35, 35, 1)
				Motor.motor(28, 28, 1)
				count = 40
			Motor.motor(28, 28, 0.1)

			# --- Roll Over Check --- #
			if(Stuck.stuckDetection() == 1):
				flug = flug + 1	#Not Roll Over
			else:
				flug = 0		#Roll Over
			count = count - 1
		Motor.motor(0, 0, 2)
	except:
		Motor.motor(0, 0, 2)
		Motor.motor_stop()
		print(traceback.format_exc())
