import sys
sys.path.append("/home/pi/git/kimuralab/IntegratedProgram/Running")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/BMX055")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/GPS")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/Motor")
sys.path.append("/home/pi/git/kimuralab/Other")

import pigpio
import time
import traceback

import BMX055
import GPS
import Motor
import Other
import RunningGPS

oLat = 0.0
oLon = 0.0
gpsData = [0.0, 0.0, 0.0, 0.0, 0.0]
stuckNum = 0

aveinit = 0
stuckCount = 0
stuckFlug = 0

def BMXstuckDetection(mP, bmxThd, measureCount, countThd):
	global aveinit, stuckCount
	for i in range(5):
		bmxinit = BMX055.bmx055_read()
		print(i, "init:", bmxinit[0:6])
		aveinit = aveinit + bmxinit[5]
	aveinit = aveinit / 5
	#print('aveinit', aveinit)
	Motor.motor(-mP, mP, 0.5)
	for i in range(measureCount):
		bmxnow = BMX055.bmx055_read()
		print(i, "now:", bmxnow[0:6])
		if bmxnow[5] - aveinit < bmxThd:
			stuckCount = stuckCount + 1
			#print('stuckCount', stuckCount)
			if stuckCount > countThd:
				print("stuck DA YO NE ?")
				Motor.motor(0, 0, 2)
				return 1
		else:
			stuckCount = 0
	Motor.motor(0, 0, 2)
	return 0

def stuckDetection(nLat, nLon):
	global oLat
	global oLon
	global stuckNum
	distance = 0.0
	angle1, angle2 = 0.0, 0.0
	stuckStatus = 0

	'''
	if(oLat == 0.0 and oLon == 0.0):
		# --- Initialize nLat and nLon --- #
		oLat = nLat
		oLon = nLon
	'''

	if(not nLon == 0.0):
		distance, angle1, angle2 = RunningGPS.calGoal(nLat, nLon, oLat, oLon, 0.0)
		if(distance <= 5):
			stuckStatus = 1
			stuckNum = stuckNum + 1
		else:
			stuckStatus = 0
			stuckNum = 0
		oLat = nLat
		oLon = nLon
		print(distance)
	return stuckStatus, stuckNum

if __name__ == "__main__":
	try:
		GPS.openGPS()
		"""
		while 1:
			# --- Get GPS Data adn Judge Stuck --- #
			gpsData = GPS.readGPS()
			while(not RunningGPS.checkGPSstatus(gpsData)):
				gpsData = GPS.readGPS()
				time.sleep(1)
			print(gpsData)
			stuckMode = stuckDetection(gpsData[1], gpsData[2])
			print(stuckMode)
			#stuckMode
			#	0 : Not Stuck
			#	1 : Stuck
			Motor.motor(0, 0, 1)

			#Motor.motor(60, 60, 1)
			time.sleep(20)
			Motor.motor(0, 0, 1)

		"""
		Motor.motor(60, 60, 3)
		Motor.motor(0, 0, 2)
		BMX055.bmx055_setup()
		stuckFlug = BMXstuckDetection(70, 100, 100, 20)
		if stuckFlug == 1:
			for i in range(2):
				Motor.motor(-70, -70, 3)
				Motor.motor(0, 0, 2)
				Motor.motor(-70, 70, 3)
				Motor.motor(0, 0, 2)
				Motor.motor(70, 70, 3)
				Motor.motor(0, 0, 2)
				Motor.motor(-70, 70, 3)
				Motor.motor(0, 0, 2)
		Motor.motor(0, 0, 1)
		GPS.closeGPS()
	except KeyboardInterrupt:
		Motor.motor(0, 0, 1)
		GPS.closeGPS()
	except:
		print(traceback.format_exc())
		Motor.motor(0, 0, 1)
		GPS.closeGPS()
