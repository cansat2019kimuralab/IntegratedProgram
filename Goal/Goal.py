import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import time
import numpy as np
import traceback
import BMX055
import goal_detection
import Motor
import GPS
import Other

mP = 0.00
e = 0.00
a = 0

def Togoal(photopath, H_min, H_max, S_thd, spinGoal, vStraightGoal):
	global e, mP, a
	area, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	if area == -1 and GAP == 0:
		Motor.motor(0, 0, 0.3)
		return [0, area, GAP, photoname]
	
	elif area == 0 and GAP == -1:
		mp = accPID(spinGoal, 5, 0.7, 0.3, 0.5, 60.0, 20.0)
		Motor.motor(mp, 20)
		#Motor.motor(0, 0, 0.3)
		a = 0
		return [-1, area, GAP, photoname]

	else:
		if a == 0:
			Motor.motor(0, 0, 0.1)
			a = 1
		if GAP > 0:
			mp = velPID(-10.0, GAP, 0.7, 0.3, 0.5, 60, 0)
			Motor.motor(30, mp)

		else:
			mp = velPID(-10.0, GAP, 0.7, 0.3, 0.5, 60, 0)
			Motor.motor(mp, 30)
		return [1, area, GAP, photoname]

def accPID(Goal, bm, Kp, Ki, Kd, max, min):
	bmx055data = BMX055.bmx055_read()
	global e, mP
	e1 = e
	e2 = e1
	e = bmx055data[bm] - Goal
	mP = mP + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
	mP = mP if mP <= max else max
	if mP < 0:
		mP = min
	return mP

def velPID(Goal, vel, Kp, Ki, Kd, max, min):
	global e, mP
	e1 = e
	e2 = e1
	e = vel - Goal
	mP = mP + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
	mP = mP if mP <= max else max
	if mP < 0:
		mP = min
	return mP


def culvel(fC, bm, t):
	filterCoefficient = fC
	lowpassValue = 0.0
	highpassValue = 0.0
	timeSpan = t
	oldAccel = 0.0
	vel = 0.0

	bmx055data = BMX055.bmx055_read()
	#lowpass
	lowpassValue = lowpassValue * filterCoefficient + bmx055data[bm] * (1 - filterCoefficient)
	#highpass
	highpassValue = bmx055data[bm] - lowpassValue
	#velcity
	vel = ((highpassValue + oldAccel) * timeSpan) / 2 + vel
	oldAccel = highpassValue
	return vel

def SpeedSwitch(area):
	speed = -area / 1000 + 50
	return speed 

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
		BMX055.bmx055_setup()
		count = 0
		ahh = 0
		H_min = 200
		H_max = 10
		S_thd = 120
		spinGoal = -50.00
		vStraightGoal = 10.00
		goal = Togoal("photo/photo", H_min, H_max, S_thd, spinGoal ,vStraightGoal)
		while goal[0] != 0:
			gpsData = GPS.readGPS()
			goal = Togoal("photo/photo", H_min, H_max, S_thd, spinGoal, vStraightGoal)
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
		Motor.motor_stop()
		print(traceback.format_exc())
