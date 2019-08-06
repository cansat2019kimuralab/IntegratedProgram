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

mP = 0.00	#motor power for PID
e = 0.00	#error for PID
bomb = 0	#flug for rotation
H_min = 200	#Hue minimam
H_max = 10	#Hue maximam
S_thd = 120	#Saturation threshold
Kp = 0.8	#Gain proportional
Ki = 0.7	#Gain integer
Kd = 0.3	#Gain differential
mpL = 10		#motor power for Low level
mpH = 30	#motor power fot High level
adj = 2		#adjust motor power

def Togoal(photopath, H_min, H_max, S_thd, Kp, Ki, Kd, mpL, mpH):
	global e, mP, bomb, adj
	Motor.motor(0,0,0.3)
	Motor.motor(30,30,0.1)
	Motor.motor(0,0,0.3)
	time.sleep(0.5)
	area, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	print("GAP",GAP)
	print("bomb",bomb)
	print("area",area)
	if area == -1 and GAP == 0:
		Motor.motor(30, 30 + adj, 0.3)
		Motor.motor(0, 0, 3)
		return [0, area, GAP, photoname]

	elif area == 0 and GAP == -1:
		if bomb == 1:
			Motor.motor(mpH, mpL + adj, 0.5, 2)
			bomb = 1
		else:
			Motor.motor(mpL, mpH + adj, 0.5, 2)
			bomb = 0

		return [-1, area, GAP, photoname]

	else:
		if area < 10000 and area > 0 and GAP < 0:
			#MP = velPID(0.0, -GAP, Kp, Ki, Kd, mpH + 10, mpH)
			MP = curvingSwitch(GAP,10)
			Motor.motor(mpH, mpH + MP + adj, 0.5)
			bomb = 1
		elif area < 10000 and area > 0 and GAP >= 0:
			#MP = velPID(0.0, GAP, Kp, Ki, Kd, mpH + 10, mpH)
			MP = curvingSwitch(GAP,10)
			Motor.motor(mpH + MP, mpH, 0.5)
			bomb = 0
		elif area >= 10000 and GAP < 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mpL, mpH + MP + adj, 0.3)
			bomb = 1

		elif area >= 10000 and GAP >= 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mpH + MP, mpL, 0.3)
			bomb = 0

		else:
			print("error")
			return [-1, area, GAP, photoname]
		print('MP',MP)

		return [1, area, GAP, photoname]

def accPID(Goal, bm, Kp, Ki, Kd, max, min):
	bmx055data = BMX055.bmx055_read()
	global e, mP
	e1 = e
	e2 = e1
	e = bmx055data[bm] - Goal
	mP = mP + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
	print("bmx",bmx055data[bm])
	mP = mP if mP <= max else max
	if mP < 0:
		mP = min
	return mP

def velPID(Goal, vel, Kp, Ki, Kd, max, min):
	global e, mP
	e1 = e
	e2 = e1
	e = vel - Goal
	mP = mP + Kp * (e-e1) * 0.5 + Ki * e * 0.5 + Kd * ((e-e1) - (e1-e2) * 0.5 )
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

def curvingSwitch(GAP, add):
	if abs(GAP) > 144:
		return add
	elif abs(GAP) > 128:
		return add*0.9
	elif abs(GAP) > 112:
		return add*0.8
	elif abs(GAP) > 96:
		return add*0.7
	elif abs(GAP) > 80:
		return add*0.6
	elif abs(GAP) > 64:
		return add*0.5
	elif abs(GAP) > 48:
		return add*0.4
	elif abs(GAP) > 32:
		return add*0.3
	elif abs(GAP) > 16:
		return add*0.2
	elif abs(GAP) > 0:
		return 0



if __name__ == "__main__":
	try:
		GPS.openGPS()
		BMX055.bmx055_setup()
		goal = Togoal("photo/photo", H_min, H_max, S_thd, Kp, Ki, Kd, mpL, mpH)
		while goal[0] != 0:
			gpsData = GPS.readGPS()
			goal = Togoal("photo/photo", H_min, H_max, S_thd, Kp, Ki, Kd, mpL, mpH)
			print("goal flug is",goal)
			Other.saveLog("GoalLog.txt", time.time(), gpsData[1], gpsData[2], goal)
			"""
			count = 0
			ahh = 0
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
		Motor.motor_stop()
		GPS.closeGPS()

	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
		GPS.closeGPS()
	except:
		GPS.closeGPS()
		Motor.motor_stop()
		print(traceback.format_exc())
