import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import difflib
import pigpio
import serial
import binascii
import BMX055
import Capture
import ParaDetection
import IM920
import GPS
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

def Cal_rho(lon_a,lat_a,lon_b,lat_b):
	ra=6378.140  # equatorial radius (km)
	rb=6356.755  # polar radius (km)
	F=(ra-rb)/ra # flattening of the earth
	rad_lat_a=np.radians(lat_a)
	rad_lon_a=np.radians(lon_a)
	rad_lat_b=np.radians(lat_b)
	rad_lon_b=np.radians(lon_b)
	pa=np.arctan(rb/ra*np.tan(rad_lat_a))
	pb=np.arctan(rb/ra*np.tan(rad_lat_b))
	xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
	c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
	c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
	dr=F/8*(c1-c2)
	rho=ra*(xx+dr)
	return rho

def ParaAvoidance():
	n = 0
	try:
		GPS.openGPS()
		time.sleep(3)

		print("START: GPS init")
		GPS_init = GPS.readGPS()
		GPS_now = GPS_init
		print("SUCCESS: GPS init")
	
		dist = 0
		try:
			while dist <= 0.020 :
				print("START: capture")
				Capture.Capture(n)
				print("SUCCESS: capture")

				print("START: Judge parachute exist")
				img = cv2.imread('photo/photo' + str(n) + '.jpg')
				flug = ParaDetection.ParaDetection(img)
				if flug == 0:
					Motor.motor(-50,50,2)
					Motor.motor(0,0,2)
					try:
						print("START: GPS now")
						GPS_now = GPS.readGPS()
						print("SUCCESS: GPS now")
					except:
						print("FAIL: GPS now")
						GPS.closeGPS()
					dist = Cal_rho(GPS_now[2], GPS_now[1], GPS_init[2], GPS_init[1])
					print("GPS_now is", GPS_now[2], GPS_now[1],"GPS_init is" , GPS_init[2], GPS_init[1])
					print("Distance from prachute is", dist)
	
				else:
					Motor.motor(30,30,1)
					Motor.motor(0,0,2)

		except KeyboardInterrupt:
			Motor.motor_stop()

	except:
		GPS.closeGPS()
		print("fail GPS init")

if __name__ == '__main__':
	print("START: Judge covered by Parachute")
	ParaJudge()
	print("START: Parachute avoidance")
	ParaAvoidance()
