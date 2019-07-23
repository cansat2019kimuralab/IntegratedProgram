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

def checkGPSstatus(gps):
	if(gpsData[1] != -1.0 and gpsData[2] != 0.0):
		return 0
	else:
		return 1

def calNAng(calibrationScale, angleOffset):
	bmx055Data = BMX055.bmx055_read()
	nowAng = Calibration.readDir(calibrationScale, bmx055Data) - angleOffset
	nowAng = nowAng if nowAng <= 180.0 else nowAng - 360.0
	nowAng = nowAng if nowAng >= -180.0 else nowAng + 360.0
	return nowAng

def calGoal(nowLat, nowLon, goalLat, goalLon, nowAng):
	distanceGoal, angleGoal = GPS.Cal_RhoAng(nowLat, nowLon, goalLat, goalLon)
	relativeAng = angleGoal - nowAng
	relativeAng = relativelAng if relativeAng <= 180 else relativeAng - 360
	relativeAng = relativeAng if relativeAng >= -180 else relativeAng + 360
	return [distanceGoal, angleGoal, relativeAng]

def runMotorSpeed(relativeAng):
	mPSin = int(relativeAng * (-1.0))
	mPLeft = int(50 * (180-relativeAng)/180) + mPSpin
	mPRight = int(50 * (180-relativeAng)/180) - mPSpin
	mPLeft = 50 if mPLeft > 50 else mPLeft
	mPLeft = -50 if mPLeft < -50 else mPLeft
	mPRight = 50 if mPRight > 50 else mPRight
	mPRight = -50 if mPRight < -50 else mPRight
	return [mPL, mPR, mPS]

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
		while(not checkGPSstatus(gpsData)):
			gpsData = GPS.readGPS()
			time.sleep(1)

		print("Runnning Start")
		while(disGoal >= 5):
			if(checkGPSstatus(gpsData)):
				nLat = gpsData[1]
				nLon = gpsData[2]

			#Calculate angle
			nAng = calNAng(ellipseScale, angOffset)

			#Calculate disGoal and relAng
			disGoal, angGoal, relAng = calGoal(nLat, nLon, gLat, gLon, nAng)

			#Calculate Motor Power
			mPL, mPR, mPS = runMotorSpeed(relAng)

			Motor.motor(mPL, mPR, 0.001, 1)

			print(nLat, nLon, disGoal, angGoal, nAng, relAng, mPL, mPR, mPS)
			Other.saveLog(runningLog, time.time(), nLat, nLon, disGoal, angGoal, nAng, relAng, mPL, mPR, mPS)
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
