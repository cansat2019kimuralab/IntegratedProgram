import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
import time
import pigpio
import serial
import os
import BMX055
import Calibration
import GPS
import Motor

fileCal = "" 						#file path for Calibration
ellipseScale = [0.0, 0.0, 0.0, 0.0] #Convert coefficient Ellipse to Circle
disGoal = 0.0						#Distance from Goal [m]
angle = 0.0							#Angle toward Goal [deg]
gLat, gLon = 35.918709, 139.911056	#Coordinates of That time
nLat, nLon = 0.0, 0.0		  		#Coordinates of That time

pi = pigpio.pi()	#object to set pigpio

def setup():
	pi.set_mode(22,pigpio.OUTPUT)
	pi.write(22,0)
	pi.write(17,0)
	time.sleep(1)
	#BMX055.bmx055_setup()
	GPS.openGPS()
	with open('log/runningLog.txt', 'w'):
		pass

def close():
	GPS.closeGPS()
	Motor.motor_stop()

def fileName(f):
	i = 0
	while(os.path.exists(f+str(i) + ".txt")):
		i = i + 1
	f = f + str(i) + ".txt"
	return f

if __name__ == "__main__":
	try:
		setup()
		time.sleep(1)

		#fileCal = "cal_t"
		#fileCal = fileName(fileCal)

		#ellipseScale = Calibration.Calibration(fileCal)

		while 1:
			gpsData = GPS.readGPS()
			#bmx055Data = BMX055.bmx055_read()
			print(str(gpsData[1]) + "\t" + str(gpsData[2])+ "\t", end="")
			if(gpsData[1] != 0.0 and gpsData[2] != 0.0):
				nLat = gpsData[1]
				nLon = gpsData[2]
				disGoal, angle = GPS.Cal_RhoAng(nLon, nLat, gLon, gLat)
				print(disGoal, angle)
			else:
				print("StatusV")
			time.sleep(1)
		close()
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
	except Exception as e:
		close()
		print(e.message)
