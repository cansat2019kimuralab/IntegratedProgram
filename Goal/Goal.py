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
# --- variable of time setting --- #
t_start  = 0.0				#time when program started
t_sleep = 60				#time for sleep phase
t_release = 120				#time for release(loopx)
t_land = 300					#time for land(loopy)
t_melt = 5					#time for melting
t_sleep_start = 0			#time for sleep origin
t_release_start = 0			#time for release origin
t_land_start = 0			#time for land origin
t_calib_origin = 0			#time for calibration origin
t_paraDete_start = 0
t_takePhoto_start = 0		#time for taking photo
timeout_calibration = 180	#time for calibration timeout
timeout_parachute = 60
timeout_takePhoto = 10		#time for taking photo timeout

# --- variable for storing sensor data --- #
gpsData = [0.0,0.0,0.0,0.0,0.0]						#variable to store GPS data
bme280Data = [0.0,0.0,0.0,0.0]						#variable to store BME80 data
bmx055data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]	#variable to store BMX055 data

# --- variable for Judgement --- #
lcount = 0		#lux count for release
acount = 0		#press count for release
Pcount = 0		#press count for land
GAcount = 0
gacount=0	#GPSheight count for land
luxjudge = 0	#for release
pressjudge = 0	#for release and land
gpsjudge = 0	#for land
paraExsist = 0 	#variable for Para Detection    0:Not Exsist, 1:Exsist
goalFlug = -1	#variable for GoalDetection		-1:Not Detect, 0:Goal, 1:Detect
goalBuf = -1
goalArea = 0	#variable for goal area
goalGAP = -1	#variable for goal gap
H_min = 200		#Hue minimam
H_max = 10		#Hue maximam
S_thd = 120		#Saturation threshold

# --- variable for Running --- #
fileCal = "" 						#file path for Calibration
ellipseScale = [0.0, 0.0, 0.0, 0.0] #Convert coefficient Ellipse to Circle
disGoal = 100.0						#Distance from Goal [m]
angGoal = 0.0						#Angle toword Goal [deg]
angOffset = -77.0					#Angle Offset towrd North [deg]
gLat, gLon = 35.742532, 140.011542	#Coordinates of That time
nLat, nLon = 0.0, 0.0		  		#Coordinates of That time
nAng = 0.0							#Direction of That time [deg]
relAng = [0.0, 0.0, 0.0]			#Relative Direction between Goal and Rober That time [deg]
rAng = 0.0							#Median of relAng [deg]
mP, mPL, mPR, mPS = 0, 0, 0, 0		#Motor Power
kp = 0.8							#Proportional Gain
maxMP = 60							#Maximum Motor Power
mp_min = 20							#motor power for Low level
mp_max = 50							#motor power fot High level
mp_adj = 2							#adjust motor power

# --- variable of Log path --- #
phaseLog =			"/home/pi/log/phaseLog.txt"
sleepLog = 			"/home/pi/log/sleepLog.txt"
releaseLog = 		"/home/pi/log/releaseLog.txt"
landingLog = 		"/home/pi/log/landingLog.txt"
meltingLog = 		"/home/pi/log/meltingLog.txt"
paraAvoidanceLog = 	"/home/pi/log/paraAvoidanceLog.txt"
runningLog = 		"/home/pi/log/runningLog.txt"
goalDetectionLog =	"/home/pi/log/goalDetectionLog.txt"
captureLog = 		"/home/pi/log/captureLog.txt"
calibrationLog = 	"/home/pi/log/calibrationLog"
errorLog = 			"/home/pi/log/erroLog.txt"

photopath = 		"/home/pi/photo/photo"
photoName =			""
bomb = 0	#flug for rotation
H_min = 200	#Hue minimam
H_max = 10	#Hue maximam
S_thd = 120	#Saturation threshold
mp_min = 10	#motor power for Low level
mp_max = 30	#motor power fot High level
mp_adj = -2		#adjust motor power
mP, mPL, mPR, mPS = 0, 0, 0, 0	
adj_add = 15
angOffset = -77.0

Gkp = 0.2
goalFlug = -1
goalBuf = -1
goalArea = 0
goalGAP = -1
goalnowAng = 1
goalBufAng = 1
ellipseScale = 1
goalRelativeAng = 0

t = 0
timeout_calibration = 180	#time for calibration timeout
areaSamp = 10000
LSamp = 0.3
GAPSamp = 50
xSamp = 0.1

calibrationLog = 	"/home/pi/log/calibrationLog"
goalDetectionLog =	"/home/pi/log/goalDetectionLog.txt"
captureLog = 		"/home/pi/log/captureLog.txt"
photopath = 		"/home/pi/photo/photo"

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

def calR2G(nowArea, nowGAP, SampArea, SampL, SampX, SampGAP):
	nowL = SampL*math.sqrt(SampArea)/math.sqrt(nowArea)
	print("nowL",nowL)
	print("nowGAP",nowGAP)
	nowX = SampX * math.sqrt((1000*nowL)**2 - nowGAP**2) / math.sqrt((1000*SampL)**2 - SampGAP**2) * nowGAP / SampGAP
	print("nowX",nowX)
	angR2G = math.degrees(math.asin(nowX/nowL))
	print("angR2G",angR2G)
	return [nowL, angR2G]

if __name__ == "__main__":
	try:
		GPS.openGPS()
		BMX055.bmx055_setup()
		while goalFlug != 0 or goalBuf != 0:
			gpsdata = GPS.readGPS()
			goalBuf = goalFlug
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
			Motor.motor(15,15,0.3)
			Motor.motor(0,0,0.3)
			#-----------------get information-----------------#
			goalFlug, goalArea, goalGAP, photoName = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
			print("GAP",goalGAP)
			print("bomb",bomb)
			print("area",goalArea)
			print("flug",goalFlug)	
			goalnowAng = RunningGPS.calNAng(ellipseScale, angOffset)
			#--------------------goal---------------------#
			if goalFlug == 0:
				Motor.motor(40, 40 + mp_adj, 1.5)
				Motor.motor(0, 0, 3)
				
			#------------------not detect----------------------#
			elif goalFlug == -1:
				goalBufAng = goalnowAng
				if bomb == 1:
					Motor.motor(mp_max, mp_min + mp_adj, 0.5)
					bomb = 1
				else:
					Motor.motor(mp_min, mp_max + mp_adj, 0.5)	
					bomb = 0
			#---------------detect but no goal-------------#
			else:
				if goalArea < 10000 and goalArea > 0 and goalGAP < 0:
					LR2G, angR2G = calR2G(goalArea, goalGAP, areaSamp, LSamp, xSamp, GAPSamp)
					goalBufAng = RunningGPS.calNAng(ellipseScale, angOffset)
					tbomb = time.time()
					while time.time() - tbomb < 3:
						goalnowAng = RunningGPS.calNAng(ellipseScale, angOffset)
						goalRelativeAng = angR2G + goalBufAng - goalnowAng
						print("goalRelativeAng",goalRelativeAng)
						mPL, mPR, mPS = RunningGPS.runMotorSpeed(-goalRelativeAng, Gkp, mp_max)
						Motor.motor(mPL, mPR, 0.001, 1)
					Motor.motor(0, 0, 0.5)
					bomb = 1
				elif goalArea < 10000 and goalArea > 0 and goalGAP >= 0:
					LR2G, angR2G = calR2G(goalArea, goalGAP, areaSamp, LSamp, xSamp, GAPSamp)
					tbomb = time.time()
					while time.time() - tbomb < 3:
						goalnowAng = RunningGPS.calNAng(ellipseScale, angOffset)
						goalRelativeAng = angR2G + goalBufAng - goalnowAng
						print("goalRelativeAng",goalRelativeAng)
						mPL, mPR, mPS = RunningGPS.runMotorSpeed(goalRelativeAng, Gkp, mp_max)
						Motor.motor(mPL, mPR, 0.001, 1)
					Motor.motor(0, 0, 0.5)
					bomb = 0
				elif goalArea >= 10000 and goalGAP < 0:
					MP = curvingSwitch(goalGAP,10)
					Motor.motor(mp_min, mp_max + MP + mp_adj, 0.3)
					bomb = 1

				elif goalArea >= 10000 and goalGAP >= 0:
					MP = curvingSwitch(goalGAP,10)
					Motor.motor(mp_max + MP, mp_min + mp_adj, 0.3)
					bomb = 0
				else:
					print("error")
				#print('MP',MP)

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
