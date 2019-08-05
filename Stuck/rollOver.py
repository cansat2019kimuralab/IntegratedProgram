# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/Other')

import math
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
			bmx055data = BMX055.bmx055_read()
			# --- Restart --- #
			if(count == 0):
				Motor.motor(0, 0, 2)
				Motor.motor(40, 0, 2)
				Motor.motor(35, 0, 1)
				#Motor.motor(28, 0, 1)
				#Motor.motor(0, 46, 2)
				#Motor.motor(0, 38, 2)
				#Motor.motor(0, 34, 1)
				count = 40
			Motor.motor(29, 0, 0.1)
			'''
			if(count <= 25):
				Motor.motor(0, 30, 0.1)
			else:
				Motor.motor(0, 32, 0.1)
			'''
			# --- Roll Over Check --- #
			if(Stuck.stuckDetection() == 0):
				flug = flug + 1	#Not Roll Over
			else:
				flug = 0		#Roll Over
			count = count - 1
			print(count, flug)
		Motor.motor(0, 0, 2)
	except:
		Motor.motor(0, 0, 2)
		Motor.motor_stop()
		print(traceback.format_exc())
