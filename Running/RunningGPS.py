import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
sys.path.append('/home/pi/git/kimuralab/Other')
import math
import time
import pigpio
import serial
import os
import BMX055
import Calibration
import GPS
import Motor
import Other

fileCal = "" 						#file path for Calibration
ellipseScale = [0.0, 0.0, 0.0, 0.0] #Convert coefficient Ellipse to Circle
disGoal = 100.0						#Distance from Goal [m]
angGoal = 0.0						#Angle toword Goal [deg]
angOffset = -83.0					#Angle Offset towrd North [deg]
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

if __name__ == "__main__":
	try:
		setup()
		time.sleep(1)

		fileCal = Other.fileName(calibrationLog, "txt")
		
		Calibration.readCalData(fileCal)
		ellipseScale = Calibration.Calibration(fileCal)

		gpsInterval = 0

		#Get GPS data
		while(gpsData[1] == -1.0 and gpsData[2] == 0.0):
			gpsData = GPS.readGPS()

		while disGoal >= 5:
			gpsInterval = gpsInterval + 1
			if(gpsInterval == 300):
				while(gpsData[1] == -1.0 and gpsData[2] == 0.0):
						gpsData = GPS.readGPS()
				gpsInterval = 0

			#Calculate angle
			bmx055Data = BMX055.bmx055_read()
			nAng = Calibration.readDir(ellipseScale, bmx055Data) - angOffset
			nAng = nAng if nAng <= 180.0 else nAng - 360.0
			nAng = nAng if nAng >= -180.0 else nAng + 360.0
			
			#Calculate disGoal and relAng
			nLat = gpsData[1]
			nLon = gpsData[2]
			disGoal, angGoal = GPS.Cal_RhoAng(nLat, nLon, gLat, gLon)
			relAng = angGoal - nAng
			relAng = relAng if relAng <= 180 else relAng - 360
			relAng = relAng if relAng >= -180 else relAng + 360
			'''
			with open("log.txt", "a") as f:
				f.write(str(nLat) + "\t" + str(nLon) + "\t" + str(disGoal) + "\t" + str(angGoal) + "\n")
			'''

			#Calculate Motor Power
			mP = int(relAng * 1.0)
			mP = 30 if mP > 30 else mP
			mP = -30 if mP < -30 else mP
			#Motor.motor(mP, -mP, 0.001, 1)

			print(gpsData[1], gpsData[2], disGoal, angGoal, nAng, relAng, mP)
			
			IM920.Send(str(nLat) + ":" + tr(nLon))
			time.sleep(0.1)

		print("Switch to Goal Detection")
		close()
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
	except Exception as e:
		close()
		print(e.message)
