import numpy as np
import matplotlib.pyplot as plt


def dy_dt(y, t):
    return t*y + t**3


def ex(t):
    return np.exp(0.5*t**2)+0.25*t**4


y0 = 1

dt = 0.01
t = np.arange(0, 1+dt, dt)
y2 = ex(t)

y = np.zeros_like(t)
y[0] = y0

for i in range(1, len(t)):
    y[i] = y[i-1] + dt*dy_dt(y[i-1], t[i-1])

# 绘制解
plt.plot(t, y)
plt.plot(t, y2)
plt.xlabel('t')
plt.ylabel('y')
plt.title("Solution to y'(t) = t*y + t^3, y(0) = 1")
plt.show()
