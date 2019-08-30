import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/Other')
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import BMX055
import Motor
import Other
from scipy.stats import norm
from scipy import odr
from scipy import optimize
#from matplotlib.patches import Ellipse

if __name__ == "__main__":
    BMX055.bmx055_setup()
    targetVal = 300
    kp = 1.0
    ki = 0.0
    kd = 0.0
    dt = 0.05
    mPL, mPR, mPS = 0, 0, 0

    for i in range 100:
        bmx055data = BMX055.bmx055_read()
        P = (targetVal - bmx055data[5]) / 10
        mPS = mPS + int(Kp * P)
        mPS = 60 if mPS > 60 else mPS
        if mPS >= 0
            mPL, mPR = 0, mPS
        elif mPS < 0
            mPL, mPR = mPS, 0
        Motor.motor(mPL, mPR)
        print(mPL, mPR, mPS)
