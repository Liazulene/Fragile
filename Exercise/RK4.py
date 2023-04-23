import numpy as np

import numpy as np

def rk4(f, t0, y0, tf, h):
    """
    使用四阶龙格-库塔法（RK4）求解微分方程

    参数：
    f：函数，形式为 f(t, y)，其中 t 是自变量，y 是因变量
    t0：起始时间
    y0：起始状态（y(t0)）
    tf：终止时间
    h：步长

    返回：
    t：时间向量
    y：状态向量
    """

    # 初始化时间向量和状态向量
    t = np.arange(t0, tf + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0

    # 使用 RK4 方法递推求解微分方程
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(t[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(t[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return t, y


def f(t, Y):
    y, z = Y
    dydt = z
    dzdt = -2 * z - 5 * y
    return np.array([dydt, dzdt])

t, y = rk4(f, 0, np.array([1, 0]), 10, 0.01)

import matplotlib.pyplot as plt

plt.plot(t, y[:, 0], label='y')
plt.plot(t, y[:, 1], label='z')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()
