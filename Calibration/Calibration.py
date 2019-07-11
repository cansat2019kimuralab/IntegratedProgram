import numpy as np
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from scipy.stats import norm

def ellipse(B, x):
    return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

def calibration(path):
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

    ax = plt.subplot(111, aspect='equal')
    plt.scatter(xx_csv, yy_csv, c="blue")
    plt.scatter(x_csv, y_csv, c="red")
    plt.grid()
    plt.show()
    return cal_data


if __name__ == '__main__':
    file = 'cal_test_1.txt'
    cal_data = calibration(file)
    for i in range(4):
        print(cal_data[i])
