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

stuck = 0

def stuckDetection():
    stuck = 0
    bmx055data = BMX055.bmx055_read()

    if(math.fabs(bmx055data[0]) > 1.0):
        stuck = 1

    # --- Return Value --- #
    #   1: roll over
    return stuck

def stuckEscape(mode = 0):
    # --- Mode --- #
    #   1 : Roll Over
    if(mode == 1):
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
			if(stuckDetection() == 1):
				flug = flug + 1	#Not Roll Over
			else:
				flug = 0		#Roll Over
			count = count - 1 
        Motor.motor(0, 0, 2)
    else:
        pass   

if __name__ == "__main__":
	try:
        print(stuckDetection())
	except:
		Motor.motor(0, 0, 2)
		Motor.motor_stop()
		print(traceback.format_exc())
