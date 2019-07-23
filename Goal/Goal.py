import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')
import time
import cv2
import numpy as np
import difflib
import pigpio
import binascii
import goal_detection
import Motor

def Togoal():
    L, GAP, photoname = goal_detection.GoalDetection("photo")
    if L == 0 and GAP == 0 :
        Motor.motor(0,0,0.3)
        return 0
    
    elif L == -1 and GAP == -1 :
        Motor.motor(-50,50,0.3)
        return -1

    else :
        if GAP > 0:
		    #goal right
            Motor.motor(50,20,0.3)

        elif GAP < 0:
		    #gaol left
            Motor.motor(20,50,0.3)

        else :
            #goal center
            Motor.motor(30,30,0.3)
if __name__ == "__main__":
    try:
        goal = Togoal()
        while goal != 0:
            goal = Togoal()
    except KeyboardInterrupt:
        print("Emergency!")
        Motor.motor_stop()
