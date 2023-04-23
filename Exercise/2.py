import numpy as np
import matplotlib.pyplot as plt

g = 9.81  # 重力加速度
N = 1000  # 区间数量
h = 4 / N  # 区间宽度

# 定义微分方程
def f(t, y):
    y1 = y[1]
    y2 = -g
    return (y1, y2)


# 初始条件
t0 = 0
Y0 = [30, 0]

# 使用四阶龙格-库塔法求解微分方程
def rk4(f, t0, Y0, t1, h):
    t = np.arange(t0, t1 + h, h)
    Y = np.zeros((len(t), len(Y0)))
    Y[0] = Y0
    for i in range(len(t) - 1):
        k1_y, k1_v = f(t[i], Y[i])
        k2_y, k2_v = f(t[i] + h/2, [Y[i][0] + h/2*k1_y, Y[i][1] + h/2*k1_v])
        k3_y, k3_v = f(t[i] + h/2, [Y[i][0] + h/2*k2_y, Y[i][1] + h/2*k2_v])
        k4_y, k4_v = f(t[i] + h, [Y[i][0] + h*k3_y, Y[i][1] + h*k3_v])

    return t, Y

# 求解微分方程
t, Y = rk4(f, t0, Y0, 4, h)

# 绘制解的图形
plt.plot(t, Y[:, 0])
plt.xlabel('时间 t (s)')
plt.ylabel('高度 y (m)')
plt.show()
