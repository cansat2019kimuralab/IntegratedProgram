import sys
sys.append.path("/home/pi/git/kimuralab/SensorModuleTest/BMX055")
sys.append.path("/home/pi/git/kimuralab/SensorModuleTest/Motor")
sys.append.path("/home/pi/git/kimuralab/Other")

import time
import traceback

import BMX055
import Motor
import Other

if __name__ == "__main__":
    BMX055.bmx055_setup()
    t_start = time.time()
    while(time.time() - t_start <= 3):
        lp, lr = Motor.motor(50, 50)
        Other.saveLog("bmx055data.txt", lp, lr, BMX055.bmx055_read())
    
    t_start = time.time()
    while(time.time() - t_start <= 3):
        lp, lr = Motor.motor(0, 0)
        Other.saveLog("bmx055data.txt", lp, lr, BMX055.bmx055_read())
    
            
