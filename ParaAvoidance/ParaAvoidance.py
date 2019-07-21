import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import difflib
import pigpio
import binascii
import Capture
import ParaDetection
import Motor
import TSL2561
import cv2
import numpy as np

def ParaJudge():
	t1 = time.time()
	t2 = t1
	while(t2 - t1 <= 60):
		lux=TSL2561.readLux()
		print("lux1: "+str(lux[0]))

		if lux[0]<100:
			time.sleep(5)
			t2 = time.time()
		else:
			break

def ParaAvoidance():
	n = 0
	#dist = 0
	#print("START: GPS init")
	#GPS_init = GPS.readGPS()

	#while (GPS_init[2] == 0 and GPS_init[3] == 0):
		#print("FAIL: GPS init")
		#time.sleep(1)
		#GPS_init = GPS.readGPS()
	#print("SUCCESS: GPS init")


	print("START: capture")
	Capture.Capture(n)
	print("SUCCESS: capture")

	print("START: Judge parachute existance")
	img = cv2.imread('/home/pi/photo/photo' + str(n) + '.jpg')
	flug = ParaDetection.ParaDetection(img)

	if flug == 1:
		Motor.motor(50,50,3)
		Motor.motor(0, 0, 2)
		#Motor.motor(-30,30,0.5)
		#Motor.motor(0,0,2)
		#print("START: capture again")
		#Capture.Capture(n)
		#print("SUCCESS: capture")

		#print("START: Judge parachute existance")
		#img = cv2.imread('photo/photo' + str(n) + '.jpg')
		#flug = ParaDetection.ParaDetection(img)
		Motor.motor(50, 50, 3)
		Motor.motor(0, 0, 2)
	if flug == 0:
		Motor.motor(-50,-50,3)
		Motor.motor(0 ,0, 2)
		Motor.motor(-50, -50, 3)
		Motor.motor(0, 0, 2)

		#print("START: GPS now")
		#GPS_now = GPS.readGPS()
		#while (GPS_now[2] == 0 and GPS_now[3] == 0):
			#print("FAIL: GPS init")
			#GPS_now = GPS.readGPS()
		#print("SUCCESS: GPS now")
		#dist = GPS.Cal_RhoAng(GPS_now[2], GPS_now[1], GPS_init[2], GPS_init[1])[0]
		#print("GPS_now is", GPS_now[2], GPS_now[1],"GPS_init is" , GPS_init[2], GPS_init[1])
		#print("Distance from prachute is", dist)

	return flug

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
