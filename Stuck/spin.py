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

ea = 0.00
mPa = 0.00
ev = 0.00
mPv = 0.00

def accPID(Goal, bm, Kp, Ki, Kd, max, min):
	bmx055data = BMX055.bmx055_read()
	global ea, mPa
	e1 = ea
	e2 = e1
	ea = bmx055data[bm] - Goal
	mPa = mPa + Kp * (ev-e1) + Ki * ea + Kd * ((ev-e1) - (e1-e2))
	mPa = mPa if mPa <= max else max
	if mPa < 0:
		mPa = min
	return mPa

def velPID(Goal, vel, Kp, Ki, Kd, max, min):
	global ev, mPv
	e1 = ev
	e2 = e1
	ev = vel - Goal
	mPv = mPv + Kp * (ev-e1) + Ki * ev + Kd * ((ev-e1) - (e1-e2))
	mPv = mPv if mPv <= max else max
	if mPv < 0:
		mPv = min
	return mPv


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

if __name__ == "__main__":
	try:
		vStraightGoal = -200.00
		Kp = 0.7
		Ki = 0.3
		Kd = 0.5
		spinZ = 0
		t1 = time.time()
		t2 = t1
		t = 0.1
		while 1:
			velY = culvel(0.9, 1, t)
			#mp = velPID(vStraightGoal, velY, Kp, Ki, Kd, 60.0, 20.0)
			velX = culvel(0.9, 0, t)
			#mpL = velPID(10.0, velX, Kp, Ki, Kd, 20.0, 0.0)
			print("vY",velY,"vX",velX)
			Motor.motor(30, 30, 2)
			#Motor.motor(mp + mpL, mp, 0.3)
			t1 =time.time()
			t = t1 - t2
			Other.saveLog("logbmx.txt", t, BMX055.bmx055_read(), velY, velX)

	except  KeyboardInterrupt:
		Motor.motor_stop()
	except:
		Motor.motor_stop()
		print(traceback.format_exc())
