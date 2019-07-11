import random
import math
import matplotlib.pyplot as plt

if __name__ == "__main__":
    xx = []
    yy = []
    with open("randomC.txt", mode="w") as f:
        for i in range(100):
            r = random.uniform(9.999, 10.001)
            theta = random.uniform(0, 2*math.pi)
            x = 20.0 * r * math.cos(theta) + 1.0
            y = 10.0 * r * math.sin(theta) - 2.0
            f.write("%f %f %f" % (x, y, 0.0))
            f.write("\n")
            xx.append(x)
            yy.append(y)

    plt.scatter(xx, yy)
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    plt.show()
