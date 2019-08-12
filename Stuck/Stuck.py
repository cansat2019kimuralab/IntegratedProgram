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

def stuckDetection(nLat, nLon):
	global oLat
	global oLon
	global stuckNum
	distance = 0.0
	angle1, angle2 = 0.0, 0.0
	stuckStatus = 0

	if(not nLon == 0.0):
		distance, angle1, angle2 = RunningGPS.calGoal(nLat, nLon, oLat, oLon, 0.0)
		if(distance <= 5):
			stuckStatus = 1
			stuckNum = stuckNum + 1
		else:
			stuckStatus = 0
			stuckNum = 0
		oLat = nLat
		oLon = nLon
		#print(distance)
	return stuckStatus, stuckNum

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
