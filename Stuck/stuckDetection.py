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

def stuckDetection(nLat, nLon):
    global oLat
    global oLon
    global stuckNum
    distance = 0.0
    angle1, angle2 = 0.0, 0.0
    stuckStatus = 0

    if(oLat == 0 and oLon == 0):
        # --- Initialize nLat and nLon --- #
        oLat = nLat
        oLon = nLon

    if(not nLon == 0.0):
        distance, angle1, angle2 = RunningGPS.calGoal(nLat, nLon, oLat, oLon, 0.0)
        if(distance <= 10):
            stuckStatus = 1
            stuckNum = stuckNum + 1
        else:
            stuckStatus = 0
            stuckNum = 0
        oLat = nLat
        oLon = nLon
    return stuckStatus

if __name__ == "__main__":
    try:
        GPS.openGPS()
        while(not RunningGPS.checkGPSstatus(gpsData)):
            time.sleep(1)
            gpsData = GPS.readGPS()
        time.sleep(10)
        if(not stuckDetection(gpsData[1], gpsData[2])):
            print()
        GPS.closeGPS()
        Motor.motor(0, 0, 1)
    except KeyboardInterrupt:
        GPS.closeGPS()
        Motor.motor(0, 0, 1)
    except:
        print(traceback.format_exc())
        GPS.closeGPS()
        Motor.motor(0, 0, 1)