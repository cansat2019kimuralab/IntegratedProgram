import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import time
import cv2
import numpy as np
import difflib
import pigpio
import binascii
import traceback
import BMX055
import goal_detection
import Motor
import GPS
import Other

def Togoal(photopath, H_min, H_max, S_thd):
	area, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	#print("GAP is",GAP)
	#print("area is",area)
	if area == -1 and GAP == 0:
		Motor.motor(0, 0, 0.3)
		return [0, ,area, GAP, photoname]
	
	elif area == 0 and GAP == -1:
		Motor.motor(0, 25, 0.2, 1)
		BMX055.bmx055_read()
		#Motor.motor(0, 0, 0.3)
		#time.sleep(1)
		return [-1, area, GAP, photoname]

	else:
		speed = SpeedSwitch(area)
		t, switch = CurvingSwitch(GAP)
		if switch == 1:
			mPL = speed
			mPR = speed
		elif switch == 2:
			mPL = -speed
			mPR = speed
		elif switch == 3:
			mPL = speed
			mPR = -speed
		else:
			print("Error")
		Motor.motor(mPL, mPR, t, 1)
		Motor.motor(0, 0, 0.3)
		time.sleep(1)
		Motor.motor(20, 20, 0.2, 1)
		Motor.motor(0, 0, 0.3)
		time.sleep(1)
		#switch 1:goal center 2:goal left 3:goal right
		return [switch, area, GAP, photoname]

def SpeedSwitch(area):
	if area < 5000 :
		return 50
	elif area < 10000:
		return 40
	else:
		return 30 

def CurvingSwitch(GAP):
	if abs(GAP) < 40:
		t = 0.8
		return [t, 1]
	elif abs(GAP) < 70:
		t = 0.06

	else:
		t = 0.1

	if GAP > 0:
		return [t, 3]

	else:
		return [t, 2]
		
if __name__ == "__main__":
	try:
		GPS.openGPS()
		BMX.bmx055_setup()
		count = 0
		ahh = 0
		H_min = 200
		H_max = 10
		S_thd = 120
		goal = Togoal("photo/photo", H_min, H_max, S_thd)
		while goal[0] != 0:
			gpsData = GPS.readGPS()
			goal = Togoal("photo/photo", H_min, H_max, S_thd)
			print("goal flug is",goal)
			Other.saveLog("GoalLog.txt", time.time(), gpsData[1], gpsData[2], goal)
			"""
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
			"""
		GPS.closeGPS()

	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
		GPS.closeGPS()
	except:
		GPS.closeGPS()
		print(traceback.format_exc())
