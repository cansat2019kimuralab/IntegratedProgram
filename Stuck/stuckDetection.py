import sys
sys.path.append("/home/pi/git/kimuralab/IntegratedProgram/Running")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/BMX055")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/GPS")
sys.path.append("/home/pi/git/kimuralab/SensorModuleTest/Motor")
sys.path.append("/home/pi/git/kimuralab/Other")

import math
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
stuckStatus = 0

stuckFlug = 0

def BMXstuckDetection(mP, bmxThd, measureCount, countThd, mode=0):
	global aveinit, stuckCount
	returnVal = 0
	if mode == 0:
		for i in range(5):
			bmxinit = BMX055.bmx055_read()
			print(i, "init:", bmxinit[0:6])
			aveinit = aveinit + bmxinit[5]
		aveinit = aveinit / 5
		#print('aveinit', aveinit)
		Motor.motor(-mP, mP, 0.5)

	for i in range(measureCount):
		bmxnow = BMX055.bmx055_read()
		print(i, "now:", bmxnow[5])
		if math.fabs(bmxnow[5] - aveinit) < bmxThd:
			stuckCount = stuckCount + 1
			#print('stuckCount', stuckCount)
			if stuckCount > countThd:
				print("stuck DA YO NE ?")
				#Motor.motor(0, 0, 2)
				returnVal =  1
				break
		else:
			stuckCount = 0

	if mode == 0:
		Motor.motor(0, 0, 2)

	return returnVal

def stuckDetection(nLat = 0, nLon = 0):
	global oLat
	global oLon
	global stuckNum
	global stuckStatus
	distance = 0.0
	angle1, angle2 = 0.0, 0.0
	rollCount = 0

	for i in range(10):
		bmx055data = BMX055.bmx055_read()
		if(math.fabs(bmx055data[0]) >= 6):
			rollCount = rollCount + 1
		time.sleep(0.05)

	if(rollCount >= 8):
		#if rover has rolled over
		if(not stuckStatus == 1):
			stuckNum = 0
		stuckStatus = 1
		stuckNum = stuckNum + 1
	elif(not nLon == 0.0):
		distance, angle1, angle2 = RunningGPS.calGoal(nLat, nLon, oLat, oLon, 0.0)
		if(distance <= 5):
			#if rover doesn't move
			if not stuckStatus == 2:
				stuckNum = 0
			stuckStatus = 2
			stuckNum = stuckNum + 1
		else:
			stuckStatus = 0
			stuckNum = 0
		oLat = nLat
		oLon = nLon
	else:
		stuckStatus = 0
		stuckNum = 0
	print(stuckStatus, stuckNum, distance)
	return stuckStatus, stuckNum

if __name__ == "__main__":
	try:
		GPS.openGPS()
		while 1:
			stuckDetection()
			time.sleep(1)
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

		'''
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
		'''
		GPS.closeGPS()
	except KeyboardInterrupt:
		Motor.motor(0, 0, 1)
		GPS.closeGPS()
	except:
		print(traceback.format_exc())
		Motor.motor(0, 0, 1)
		GPS.closeGPS()
