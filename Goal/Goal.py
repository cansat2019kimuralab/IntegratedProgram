import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import time
import cv2
import numpy as np
import difflib
import pigpio
import binascii
import goal_detection
import Motor

def Togoal(photopath, H_min, H_max, S_thd):
	L, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	if L == 0 and GAP == 0:
		Motor.motor(0, 0, 0.3)
		return 0
	
	elif L == -1 and GAP == -1:
		Motor.motor(-50, 50, 0.3)
		Motor.motor(0, 0, 0.3)
		return -1

	else:
		speed = SpeedSwitch(L)
		mPL, mPR, switch = CurvingSwitch(GAP, speed)
		Motor.motor(mPL, mPR, 1)
		Motor.motor(0, 0, 0.3)
		return switch

def SpeedSwitch(L):
	if L > 10:
		return 70
	elif L > 5:
		return 50
	else:
		return 30 

def CurvingSwitch(GAP, speed):
	if GAP == 0:
		return [speed, speed, 3]
	elif abs(GAP) < 40:
		RATE = 1
		rate = 0.8
	elif abs(GAP) < 80:
		RATE = 1
		rate = 0.7
	elif abs(GAP) < 120:
		RATE = 1
		rate = 0.6
	else:
		RATE = 1
		rate = 0.5
	if GAP > 0:
		mPLeft = speed * RATE
		mPRight = speed * rate

	else:
		mPLeft = speed * rate
		mPRight = speed * RATE
		return [mPLeft, mPRight, 2]

	return [mPLeft, mPRight, 1]

if __name__ == "__main__":
	try:
		count = 0
		ahh = 0
		H_min = 200
		H_max = 10
		S_thd = 120
		goal = Togoal("photo", H_min, H_max, S_thd)
		while goal != 0:
			while count < 10:
				print(goal)
				goal = Togoal("photo", H_min, H_max, S_thd)
				if goal ==-1:
					count = count + 1
			if count == 10:
				H_min = H_min - 5
				H_max = H_max + 5
				count = 0
				ahh = ahh + 1
			if ahh == 5:
				print("runningGPS again")
				break

	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
