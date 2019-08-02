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

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()

		bmx055data = BMX055.bmx055_read()
		flug = 0
		count = 0
		Motor.motor(40, 40, 2)
		Motor.motor(35, 35, 1)
		Motor.motor(28, 28, 1)
		while flug <= 5: #(math.fabs(bmx055data[0]) > 1.0):
			print(count)
			if(count == 40):
				print("Restart")
				Motor.motor(0, 0, 3)
				Motor.motor(40, 40, 2)
				Motor.motor(35, 35, 1)
				Motor.motor(28, 28, 1)
				count = 0
			Motor.motor(28, 28, 0.1)
			bmx055data = BMX055.bmx055_read()
			if(math.fabs(bmx055data[0]) < 4.0):
				flug = flug + 1
			else:
				flug = 0
			#print(bmx055data)
			count = count + 1
		Motor.motor(0, 0, 2)
		print("b")
	except:
		Motor.motor(0, 0, 2)
		Motor.motor_stop()
		print(traceback.format_exc())
