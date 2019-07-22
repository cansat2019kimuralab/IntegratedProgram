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

dir_data = [0.0, 0.0, 0.0]

def readCalData(filepath):
	count = 0
	while count <= 200:
		Motor.motor(30, -30)
		bmx055data = BMX055.bmx055_read()
		with open(filepath, 'a')   as f:
			for i in range(6, 8):
				print(str(bmx055data[i]) + "\t", end="")
				f.write(str(bmx055data[i]) + "\t")
			print()
			f.write("\n")
		count = count + 1
	Motor.motor(0, 0, 1)

def ellipse(B, x):
	return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

def Calibration(path):
	with open(path, "r") as f:
		lines = f.readlines()
		x_csv = []
		y_csv = []
		for line in lines:
			word = line.split()
			x_csv.append(float(word[0]))
			y_csv.append(float(word[1]))

	xx_csv = x_csv
	yy_csv = y_csv

	n = len(x_csv)
	x2 = np.power(x_csv, 2)
	y2 = np.power(y_csv, 2)

	xy = 0.0
	for i in range(len(x_csv)):
		xy = xy + x_csv[i] * y_csv[i]

	E = -(x_csv * (x2 + y2))
	F = -(y_csv * (x2 + y2))
	H = -(x2 + y2)

	x_csv = np.sum(x_csv)
	y_csv = np.sum(y_csv)

	x2 = np.sum(x2)
	y2 = np.sum(y2)

	E = np.sum(E)
	F = np.sum(F)
	H = np.sum(H)
	K = np.array([[x2,xy,x_csv], [xy,y2,y_csv], [x_csv,y_csv,n]])
	L = np.array([E,F,H])
	P = np.dot(np.linalg.inv(K),L)

	x_ave = (-1/2)* P[0]
	y_ave = (-1/2)* P[1]

	x_csv = xx_csv - x_ave
	y_csv = yy_csv - y_ave

	xy_csv = np.array([x_csv, y_csv])

	mdr = odr.Model(ellipse, implicit=True)
	mydata = odr.Data(xy_csv,y=1)
	myodr = odr.ODR(mydata, mdr, beta0=[1.,2.])
	myoutput = myodr.run()

	x_csv = x_csv / 100.* myoutput.beta[1]
	y_csv = y_csv / 100.* myoutput.beta[0]

	cal_data = [x_ave, y_ave, 100.*myoutput.beta[1], 100.*myoutput.beta[0]]

	#plt.scatter(xx_csv, yy_csv, c="blue")
	#plt.scatter(x_csv, y_csv, c="red")
	#plt.grid()
	#plt.axes().set_aspect('equal')
	#plt.show()
	return cal_data

def readDir(calData, bmx055data):
	return math.atan2((bmx055data[6]-calData[0])/calData[2], (bmx055data[7]-calData[1])/calData[3])*180/math.pi


if __name__ == '__main__':
	try:
		BMX055.bmx055_setup()
		time.sleep(1)
		file = Other.fileName("calData", "txt")
		readCalData(file)
		cal_data = Calibration(file)
		for i in range(4):
			print(cal_data[i])
		Other.saveLog(file, cal_data)

		for i in range(3):
			dir_data[i] = readDir(cal_data)
			time.sleep(0.1)

		while 1:
			dir_data[2] = dir_data[1]		#Thrid latest data
			dir_data[1] = dir_data[0]		#Second latest data
			dir_data[0] = readDir(cal_data)	#latest data
			dir = np.median(dir_data)
			print(str(dir) + "\t", end="")
			mP = int(dir * 1.0)
			if(mP > 30):
				mP = 30
			elif(mP < -30):
				mP = -30
			Motor.motor(mP, -mP, 0.001, 1)
			print(mP)
	except KeyboardInterrupt:
		Motor.motor(0, 0, 1)
		Motor.motor_stop()
		print("Keyboard Interrupt")
	except Exception as e:
		Motor.motor_stop()
		print(e.message)
