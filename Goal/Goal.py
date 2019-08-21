import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import RunningGPS
import time
import numpy as np
import traceback
import Calibration
import goal_detection
import Motor

goalArea = 0		#variable for goal area
goalGAP = -1		#variable for goal gap
goalthd = 7000		#variable for goal area thd
H_min = 220			#Hue minimam
H_max = 5			#Hue maximam
S_thd = 180			#Saturation threshold


photopath = 		"/home/pi/photo/photo"

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()
		while 1:
			#-----------------get information-----------------#
			Motor.motor(15, 15, 1.0)
			Motor.motor(0, 0, 1.0)
			goalFlug, goalArea, goalGAP, photoName = goal_detection.GoalDetection(photopath, H_min, H_max, S_thd, goalthd)
			print("flug", goalFlug, "area", goalArea, "GAP", goalGAP, "photoname", photoName)
			#-------------------motor debug-------------------#
			L = float(input("input left value "))
			R = float(input("input Right value "))
			T = float(input("input Time value "))
			Motor.motor(L, R, T)
			Motor.motor(0, 0, 2)
			Motor.motor_stop()

	except KeyboardInterrupt:
		print("Emergency!")
		Motor.motor_stop()
	except:
		Motor.motor_stop()
		print(traceback.format_exc())
