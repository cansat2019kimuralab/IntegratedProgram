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

	lux=TSL2561.readLux()
	#print("lux1: "+str(lux[0]))

	if lux[0] < LuxThd:
		time.sleep(1)
		return 0

	else:
		return 1

def ParaAvoidance(photopath):
	Motor.motor(50, 50, 0.5)
	Motor.motor(0, 0, 2)
	#print("START: capture")
	photoname = Capture.Capture(photopath)
	#print("SUCCESS: capture")

	#print("START: Judge parachute existance")
	img = cv2.imread(photoname)
	flug = ParaDetection.ParaDetection(img)

	if flug == 1:
		Motor.motor(50, 50, 3)
		Motor.motor(0, 0, 2)

	if flug == 0:
		Motor.motor(-50, -50, 3)
		Motor.motor(0 ,0, 2)

	return [flug,photoname]

if __name__ == '__main__':
	#GPS.openGPS()
	print("START: Judge covered by Parachute")
	ParaJudge()
	print("START: Parachute avoidance")
	try:
		ParaAvoidance()
	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
		#GPS.closeGPS()
	Motor.motor_stop()
