import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
import numpy as np
import math
import matplotlib.pyplot as plt
import Calibration
import BMX055
import Motor
import time
from scipy.stats import norm
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse


if __name__ == '__main__':
	try:
		file = 'cal_test_1.txt'
		BMX055.bmx055_setup()
		count = 0
		while count <= 200:
			Motor.motor(30, -30)
			bmx055data = BMX055.bmx055_read()
			with open(file, 'a') as f:
				for i in range(6, 8):
					print(str(bmx055data[i]) + "\t", end="")
					f.write(str(bmx055data[i]) + "\t")
				print()
				f.write("\n")
			count = count + 1

		Motor.motor(0, 0, 1)
		cal_data = Calibration.calibration(file)
		for i in range(4):
			print(cal_data[i])

		while 1:
			bmx055data = BMX055.bmx055_read()
			dir = math.atan2(bmx055data[6], bmx055data[7])*180/math.pi
			print(dir, end="")
			dir = math.atan2((bmx055data[6]-cal_data[0])/cal_data[2], (bmx055data[7]-cal_data[1])/cal_data[3])*180/math.pi
			print("\t" + str(dir))
	except KeyboardInterrupt:
		Motor.motor_stop()
	except Exception as e:
		Motor.motor_stop()
		print(e.message)
