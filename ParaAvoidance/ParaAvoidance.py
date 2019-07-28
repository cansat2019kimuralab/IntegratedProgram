import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
sys.path.append('/home/pi/git/kimuralab/Detection/ParachuteDetection')
import time
import cv2
import numpy as np
import difflib
import pigpio
import binascii
import Capture
import ParaDetection
import Motor
import TSL2561


def ParaJudge(LuxThd):
	Motor.motor(30,30,0.2)
	Motor.motor(0,0,0.2)
	lux=TSL2561.readLux()
	print("lux1: "+str(lux[0]))

	if lux[0] < LuxThd:
		time.sleep(1)
		return 0

	else:
		return 1

def ParaAvoidance(photopath):
	Motor.motor(30, 30, 0.5)
	Motor.motor(0, 0, 0.2)
	print("START: capture")
	photoname = Capture.Capture(photopath)
	print("SUCCESS: capture")

	print("START: Judge parachute existance")
	img = cv2.imread(photoname)
	flug = ParaDetection.ParaDetection(img)

	if flug == 1:
		Motor.motor(-60, -60, 2)
		Motor.motor(0, 0, 2)

	if flug == 0:
		Motor.motor(60, 50, 2)
		Motor.motor(0 ,0, 2)

	return [flug,photoname]

if __name__ == '__main__':
	print("START: Judge covered by Parachute")
	t2 = time.time()
	t1 = t2
	while t2 - t1 < 60:
		Luxflug = ParaJudge(100)
		if Luxflug == 1:
			break
		t1 =time.time()
	print("START: Parachute avoidance")
	try:
		ParaAvoidance("photo")
	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
	Motor.motor_stop()
