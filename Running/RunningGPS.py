import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
sys.path.append('/home/pi/git/kimuralab/Other')
import math
import numpy as np
import time
import pigpio
import serial
import os
import BMX055
import Calibration
import GPS
import IM920
import Motor
import Other

fileCal = "" 						#file path for Calibration
ellipseScale = [0.0, 0.0, 0.0, 0.0] #Convert coefficient Ellipse to Circle
disGoal = 100.0						#Distance from Goal [m]
angGoal = 0.0						#Angle toword Goal [deg]
angOffset = -77.0					#Angle Offset towrd North [deg]
gLat, gLon = 35.918181, 139.907992	#Coordinates of That time
#gLat, gLon = 35.933724, 139.907316
nLat, nLon = 0.0, 0.0		  		#Coordinates of That time
nAng = 0.0							#Direction of That time [deg]
relAng = 0.0						#Relative Direction between Goal and Rober That time [deg]
mP = 0								#Motor Power
gpsInterval = 0						#GPS Log Interval Time

gpsData = [0.0, -1.0, -1.0, 0.0, 0.0]						#variable to store GPS data
bmx055data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]	#variable to store BMX055data

runningLog = "runningLog.txt"
calibrationLog = "calibrationLog"

pi = pigpio.pi()	#object to set pigpio

def setup():
	pi.set_mode(22,pigpio.OUTPUT)
	pi.write(22,0)
	pi.write(17,0)
	time.sleep(1)
	BMX055.bmx055_setup()
	GPS.openGPS()
	with open('log/runningLog.txt', 'w'):
		pass

def close():
	GPS.closeGPS()
	Motor.motor_stop()

if __name__ == "__main__":
	try:
		setup()
		time.sleep(1)

		fileCal = Other.fileName(calibrationLog, "txt")

		Calibration.readCalData(fileCal)
		ellipseScale = Calibration.Calibration(fileCal)
		Other.saveLog(fileCal, ellipseScale)

		gpsInterval = 0

		#Get GPS data
		print("Getting GPS Data")
		while(gpsData[1] == -1.0 or gpsData[2] == 0.0):
			gpsData = GPS.readGPS()
			print(gpsData)
			time.sleep(1)

		print("Runnning Start")
		while disGoal >= 5:
			'''
			if(gpsInterval == 100):
				latA = [0.0, 0.0, 0.0]
				lonA = [0.0, 0.0, 0.0]
				for i in range(3):
					gpsData = GPS.readGPS()
					while(gpsData[1] == -1.0 or gpsData[2] == 0.0):
						gpsData = GPS.readGPS()
						latA[i] = gpsData[1]
						lonA[i] = gpsData[2]
					nLat = np.median(latA)
					nLon = np.median(lonA)
					gpsInterval = 0
			gpsInterval = gpsInterval + 1
			'''

			if(gpsData[1] != -1.0 and gpsData[2] != 0.0):
				nLat = gpsData[1]
				nLon = gpsData[2]

			#Calculate angle
			bmx055Data = BMX055.bmx055_read()
			nAng = Calibration.readDir(ellipseScale, bmx055Data) - angOffset
			nAng = nAng if nAng <= 180.0 else nAng - 360.0
			nAng = nAng if nAng >= -180.0 else nAng + 360.0

			#Calculate disGoal and relAng
			#nLat = gpsData[1]
			#nLon = gpsData[2]
			disGoal, angGoal = GPS.Cal_RhoAng(nLat, nLon, gLat, gLon)
			relAng = angGoal - nAng
			relAng = relAng if relAng <= 180 else relAng - 360
			relAng = relAng if relAng >= -180 else relAng + 360

			#Calculate Motor Power
			mPS = int(relAng * (-1.0))
			mPL = int(50 * (180-relAng)/180) + mPS
			mPR = int(50 * (180-relAng)/180) - mPS

			mPL = 50 if mPL > 50 else mPL
			mPL = -50 if mPL < -50 else mPL
			mPR = 50 if mPR > 50 else mPR
			mPR = -50 if mPR < -50 else mPR

			Motor.motor(mPL, mPR, 0.001, 1)

			#print(nLat, nLon, disGoal, angGoal, nAng, relAng, mP, gpsInterval)
			print(nLat, nLon, disGoal, angGoal, nAng, relAng, mPL, mPR, mPS)
			#print(gpsData[1], gpsData[2])
			#time.sleep(0.1)
			gpsData = GPS.readGPS()
			time.sleep(0.1)

		Motor.motor(0, 0, 2)
		print("Switch to Goal Detection")
		close()
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
	except Exception as e:
		close()
		print(e.message)
