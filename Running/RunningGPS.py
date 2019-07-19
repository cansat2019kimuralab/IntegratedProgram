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
disGoal = 0.0						#Distance from Goal [m]
angGoal = 0.0						#Angle toword Goal [deg]
angOffset = -83.0					#Angle Offset towrd North [deg]
gLat, gLon = 35.918181, 139.907992	#Coordinates of That time
nLat, nLon = 0.0, 0.0		  		#Coordinates of That time
nAng = 0.0							#Direction of That time [deg]
relAng = 0.0						#Relative Direction between Goal and Rober That time [deg]
mP = 0								#Motor Power
gpsInterval							#GPS Log Interval Time

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

		fileCal = "cal_t"
		fileCal = Other.fileName(fileCal, "txt")

		Calibration.readCalData(fileCal)
		ellipseScale = Calibration.Calibration(fileCal)

		gpsInterval = 0
		while 1:
			gpsInterval = gpsInterval + 1
			if(gpsInterval = 300):
				while(gpsdfata[1] = 0.0 and gpsData[3] = 0.0):
						gpsData = GPS.readGPS()
						nLat = gpsData[1]
						
				gpsInterval = 0

			bmx055Data = BMX055.bmx055_read()
			nAng = Calibration.readDir(ellipseScale) - angOffset
			nAng = nAng if nAng <= 180.0 else nAng - 360.0
			nAng = nAng if nAng >= -180.0 else nAng + 360.0
			if(gpsData[1] != 0.0 and gpsData[2] != 0.0):
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


			mP = int(relAng * 1.0)
			mP = 30 if mP > 30 else mP
			mP = -30 if mP < -30 else mP
			#Motor.motor(mP, -mP, 0.001, 1)

			print(gpsData[1], gpsData[2], disGoal, angGoal, nAng, relAng, mP)
			time.sleep(1)
		close()
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
	except Exception as e:
		close()
		print(e.message)
