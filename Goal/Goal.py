import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Running')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
import RunningGPS
import time
import math
import numpy as np
import traceback
import BMX055
import Calibration
import goal_detection
import Motor
import GPS
import Other

bomb = 0	#flug for rotation
H_min = 200	#Hue minimam
H_max = 10	#Hue maximam
S_thd = 120	#Saturation threshold
mp_min = 10	#motor power for Low level
mp_max = 40	#motor power fot High level
mp_adj = -2		#adjust motor power
mP, mPL, mPR, mPS = 0, 0, 0, 0	
adj_add = 15
angOffset = -77.0
goalFlug = -1
goalBuf = -1
goalArea = 0
goalGAP = -1
goalnowAng = 1
goalBufAng = 1
ellipseScale = 1
timeout_calibration = 180	#time for calibration timeout
areaSamp = 10000
dSamp = 0.3

calibrationLog = 	"/home/pi/log/calibrationLog"
"""
def Togoal(photopath, H_min, H_max, S_thd, mp_min, mp_max, mp_adj):
	global e, mP, bomb, nAng, ellipseScale
	Motor.motor(0,0,0.3)
	Motor.motor(30,30,0.3)
	Motor.motor(0,0,0.3)
	area, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	print("GAP",GAP)
	print("bomb",bomb)
	print("area",area)	
	nAng = RunningGPS.calAng(ellipseScale, angOffset)
	if area == -1 and GAP == 0:
		Motor.motor(40, 40 + mp_adj, 1.5)
		Motor.motor(0, 0, 3)
		return [0, area, GAP, photoname, nAng]

	elif area == 0 and GAP == -1:
		if bomb == 1:
			Motor.motor(mp_max, mp_min + mp_adj, 0.5)
			bomb = 1
		else:
			Motor.motor(mp_min, mp_max + mp_adj, 0.5)
			bomb = 0

		return [-1, area, GAP, photoname, nAng]

	else:
		if area < 10000 and area > 0 and GAP < 0:
			MP = curvingSwitch(GAP,15)
			Motor.motor(mp_max, mp_max + MP + mp_adj, 0.5)
			bomb = 1
		elif area < 10000 and area > 0 and GAP >= 0:
			MP = curvingSwitch(GAP,15)
			Motor.motor(mp_max + MP, mp_max + mp_adj, 0.5)
			bomb = 0
		elif area >= 10000 and GAP < 0:
			MP = curvingSwitch(GAP,15)
			Motor.motor(mp_min, mp_max + MP + mp_adj, 0.3)
			bomb = 1

		elif area >= 10000 and GAP >= 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mp_max + MP, mp_min + mp_adj, 0.3)
			bomb = 0

		else:
			print("error")
			return [-1, area, GAP, photoname, nAng]
		print('MP',MP)

		return [1, area, GAP, photoname, nAng]
"""
def curvingSwitch(GAP, add):
	if abs(GAP) > 144:
		return add
	elif abs(GAP) > 128:
		return add*0.9
	elif abs(GAP) > 112:
		return add*0.8
	elif abs(GAP) > 96:
		return add*0.7
	elif abs(GAP) > 80:
		return add*0.6
	elif abs(GAP) > 64:
		return add*0.5
	elif abs(GAP) > 48:
		return add*0.4
	elif abs(GAP) > 32:
		return add*0.3
	elif abs(GAP) > 16:
		return add*0.2
	elif abs(GAP) >= 0:
		return 0

def calR2G(nowArea, nowGAP, SampArea, SampL):
	nowL = SampL*math.sqrt(SampArea)/math.sqrt(nowArea)
	angR2G = math.degrees(math.asin(nowGAP/nowL))
	return [nowL, angR2G]

if __name__ == "__main__":
	try:
		GPS.openGPS()
		BMX055.bmx055_setup()
		while goalFlug != 0 or goalBuf != 0:
			gpsdata = GPS.readGPS()
			goalBuf = goalFlug
			goalBufAng = goalnowAng
			#-----------------calibration---------------------#
			if time.time() - t > timeout_calibration:
				fileCal = Other.fileName(calibrationLog, "txt")
				Motor.motor(60, 0, 2)
				Calibration.readCalData(fileCal)
				Motor.motor(0, 0, 1)
				ellipseScale = Calibration.Calibration(fileCal)
				Other.saveLog(fileCal, ellipseScale)
				t = time.time()

			Motor.motor(0,0,0.5)
			Motor.motor(30,30,0.3)
			Motor.motor(0,0,0.3)
			#-----------------get information-----------------#
			goalFlug, goalArea, goalGAP, photoName = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
			print("GAP",GAP)
			print("bomb",bomb)
			print("area",area)	
			goalnowAng = RunningGPS.calAng(ellipseScale, angOffset)
			#--------------------goal---------------------#
			if goalFlug == 0:
				Motor.motor(40, 40 + mp_adj, 1.5)
				Motor.motor(0, 0, 3)
				
			#------------------not detect----------------------#
			elif goalFlug == -1:
				if bomb == 1:
					tbomb = time.time()
					while time.time() - tbomb < 3:
						mPL, mpR, mPS = RunningGPS.runMotorSpeed(30, Gkp, mp_max)
						Motor.motor(mPL, mPR + mp_adj, 0.001, 1)
						tbomb = time.time()
					Motor.motor(0, 0, 0.5)
					bomb = 1
				else:
					mPL, mpR, mPS = RunningGPS.runMotorSpeed(-30, Gkp, mp_max)
					Motor.motor(mPL, mPR + mp_adj, 0.001, 1)
					bomb = 0
			#---------------detect but no goal-------------#
			else:
				if area < 10000 and area > 0 and GAP < 0:
					MP = curvingSwitch(GAP,15)
					Motor.motor(mp_max, mp_max + MP + mp_adj, 0.5)
					bomb = 1
				elif area < 10000 and area > 0 and GAP >= 0:
					MP = curvingSwitch(GAP,15)
					Motor.motor(mp_max + MP, mp_max + mp_adj, 0.5)
					bomb = 0
				elif area >= 10000 and GAP < 0:
					MP = curvingSwitch(GAP,15)
					Motor.motor(mp_min, mp_max + MP + mp_adj, 0.3)
					bomb = 1

				elif area >= 10000 and GAP >= 0:
					MP = curvingSwitch(GAP,10)
					Motor.motor(mp_max + MP, mp_min + mp_adj, 0.3)
					bomb = 0
				else:
					print("error")
				print('MP',MP)

			#goalFlug, goalArea, goalGAP, photoName, goalnowAng = Goal.Togoal(photopath, H_min, H_max, S_thd, mp_min, mp_max, mp_adj)
			#goalBuf = goalFlug
			print("goal is",goalFlug)
			Other.saveLog(goalDetectionLog, time.time() - t_start, gpsData, goalFlug, goalArea, goalGAP, goalnowAng, photoName)
			Other.saveLog(captureLog, time.time() - t_start, photoName)
			"""
			count = 0
			ahh = 0
			while count < 10:
				print(goal)
				goal = Togoal("photo", H_min, H_max, S_thd)
				if goal ==-1:
					count = count + 1
			if count == 10:
				H_min = H_min - 5
				H_max = H_max + 5
				count = 0
				ahh = ahh + 1
			if ahh == 5:
				print("runningGPS again")
				break
			"""
		Motor.motor_stop()
		GPS.closeGPS()

	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
		GPS.closeGPS()
	except:
		GPS.closeGPS()
		Motor.motor_stop()
		print(traceback.format_exc())
