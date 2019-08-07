import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import time
import numpy as np
import traceback
import BMX055
import goal_detection
import Motor
import GPS
import Other

mP = 0.00	#motor power for PID
e = 0.00	#error for PID
bomb = 0	#flug for rotation
H_min = 200	#Hue minimam
H_max = 10	#Hue maximam
S_thd = 120	#Saturation threshold
Kp = 0.8	#Gain proportional
Ki = 0.7	#Gain integer
Kd = 0.3	#Gain differential
mp_min = 10	#motor power for Low level
mp_max = 30	#motor power fot High level
mp_adj = 2		#adjust motor power

def Togoal(photopath, H_min, H_max, S_thd, mp_min, mp_max, mp_adj):
	global e, mP, bomb
	Motor.motor(0,0,0.3)
	Motor.motor(30,30,0.1)
	Motor.motor(0,0,0.3)
	time.sleep(0.5)
	area, GAP, photoname = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd)
	print("GAP",GAP)
	print("bomb",bomb)
	print("area",area)
	if area == -1 and GAP == 0:
		Motor.motor(30, 30 + mp_adj, 0.3)
		Motor.motor(0, 0, 3)
		return [0, area, GAP, photoname]

	elif area == 0 and GAP == -1:
		if bomb == 1:
			Motor.motor(mp_max, mp_min + mp_adj, 0.5, 2)
			bomb = 1
		else:
			Motor.motor(mp_min, mp_max + mp_adj, 0.5, 2)
			bomb = 0

		return [-1, area, GAP, photoname]

	else:
		if area < 10000 and area > 0 and GAP < 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mp_max, mp_max + MP + mp_adj, 0.5)
			bomb = 1
		elif area < 10000 and area > 0 and GAP >= 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mp_max + MP, mp_max + mp_adj, 0.5)
			bomb = 0
		elif area >= 10000 and GAP < 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mp_min, mp_max + MP + mp_adj, 0.3)
			bomb = 1

		elif area >= 10000 and GAP >= 0:
			MP = curvingSwitch(GAP,10)
			Motor.motor(mp_max + MP, mp_min + mp_adj, 0.3)
			bomb = 0

		else:
			print("error")
			return [-1, area, GAP, photoname]
		print('MP',MP)

		return [1, area, GAP, photoname]

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
	elif abs(GAP) > 0:
		return 0



if __name__ == "__main__":
	try:
		GPS.openGPS()
		BMX055.bmx055_setup()
		goal = Togoal("photo/photo", H_min, H_max, S_thd, mp_min, mp_max, mp_adj)
		while goal[0] != 0:
			gpsData = GPS.readGPS()
			goalFlug, goalArea, goalGAP, photoName  = Togoal("photo/photo", H_min, H_max, S_thd, mp_min, mp_max, mp_adj)
			print("goal flug is",goal)
			Other.saveLog("GoalLog.txt", time.time(), gpsData[1], gpsData[2], goalFlug, goalArea, goalGAP, photoName )
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
