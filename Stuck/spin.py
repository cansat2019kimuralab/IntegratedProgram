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

dt = 0.1 #計測間隔
x = np.array([[0.], [0.]]) # 初期速度を代入した「4次元状態」
u = np.array([[0.], [0.]]) # 外部要素

P = np.array([ [100., 0.], [0., 100.]]) # 共分散行列
F = np.array([[1., 0.], [0., 1.]])  # 状態遷移行列
H = np.array([[1., 0.], [0., 1.]])  # 観測行列
R = np.array([[0.1, 0], [0, 0.1]]) #ノイズ
I = np.identity((len(x)))	# 4次元単位行列

def kalman_filter(x, P, vel):
	# 予測
	x = np.dot(F, x) + u
	P = np.dot(np.dot(F, P), F.T)

	# 計測更新
	Z = np.array(vel)
	y = Z.T - np.dot(H, x)
	S = np.dot(np.dot(H, P), H.T) + R
	K = np.dot(np.dot(P, H.T), np.linalg.inv(S))
	x = x + np.dot(K, y)		
	P = np.dot((I - np.dot(K, H)), P)

	x = x.tolist()
	P = P.tolist()
	return x,P
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

def zuru(v):
	if abs(v) < 3:
		v =v_buf
	v_buf = v
	return v

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
		t = 0.0
		while t < 2.0:
			velY = culvel(0.5, 1, t)
			velY = zuru(velY)
			#mp = velPID(vStraightGoal, velY, Kp, Ki, Kd, 60.0, 20.0)
			velX = culvel(0.9, 0, t)
			velX = zuru(velX)
			#mpL = velPID(10.0, velX, Kp, Ki, Kd, 20.0, 0.0)
			v = kalman_filter(x, P, [velX,velY])
			print("vY",velY,"vX",velX)
			Motor.motor(30, 30)
			#Motor.motor(mp + mpL, mp, 0.3)
			t1 =time.time()
			t = t1 - t2
			Other.saveLog("logbmx.txt", t, BMX055.bmx055_read(), velY, velX, v[0], v[1])
		Motor.motor(0, 0, 0.5)

	except  KeyboardInterrupt:
		Motor.motor_stop()
	except:
		Motor.motor_stop()
		print(traceback.format_exc())
