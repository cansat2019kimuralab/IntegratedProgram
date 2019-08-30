import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
import numpy as np
import time
import traceback
import math
import BMX055
import Motor

spin = 0
P, I, D = 0, 0, 0
motorPowerL, motorPowerR, motorPowerS = 0, 0, 0
prebmx = 0

def pidSpin(targetSpin, KP, KI, KD, deltT):
		global P, I, D
		global motorPowerL, motorPowerR, motorPowerS
		global prebmx
		bmx055data = BMX055.bmx055_read()
		bmx055data = BMX055.bmx055_read()
		P = (targetSpin - bmx055data[5]) / 20
		I = I + P * deltT
		D = -1 * (bmx055data[5] - prebmx) / (20 * deltT)

		motorPowerS = motorPowerS + int(KP * P) + int(KI * I) + int(KD * D)
		motorPowerS = 60 if motorPowerS > 60 else motorPowerS
		motorPowerS = -60 if motorPowerS < -60 else motorPowerS

		if motorPowerS >= 0:
			motorPowerL, motorPowerR = 10, motorPowerS
		elif motorPowerS < 0:
			motorPowerL, motorPowerR = -motorPowerS, 10
		motorPowerL = 60 if motorPowerL > 60 else motorPowerL
		motorPowerL = -60 if motorPowerL < -60 else motorPowerL
		motorPowerR = 60 if motorPowerR > 60 else motorPowerR
		motorPowerR = -60 if motorPowerR < -60 else motorPowerR

		prebmx = bmx055data[5]
		#Motor.motor(mPL, mPR, dt, 1)
		#print(D, bmx055data[5], mPL, mPR, mPS)
		#spin = spin + bmx055data[5] * dt

		return motorPowerL, motorPowerR, motorPowerS, bmx055data


if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()
		targetVal = 300
		Kp = 1.0
		Ki = 1.1
		Kd = 0.0
		dt = 0.05
		mPL, mPR, mPS = 0, 0, 0
		roll = 0
		Motor.motor(0, 30)
		while(math.fabs(roll) <= 2000):
			mPL, mPR, mPS, bmx055data = pidSpin(targetVal, Kp, Ki, Kd, dt)
			roll = roll + bmx055data[5] * dt
			print(bmx055data[5], roll)
			Motor.motor(mPL, mPR, dt, 1)
		Motor.motor(0, 0, 1)
	except:
		Motor.motor(0, 0, 1)
		print(traceback.format_exc())
