import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

x = np.linspace(0, 5, 100)  # 定义x的取值范围
z_values = [2, 3, 4]  # 定义z的取值

# 计算Gamma函数的值
y_values = []
for z in z_values:
    y_values.append(gamma(z) * x**(z-1) * np.exp(-x))

# 绘制曲线图
plt.plot(x, y_values[0], label=f"z={z_values[0]}")
plt.plot(x, y_values[1], label=f"z={z_values[1]}")
plt.plot(x, y_values[2], label=f"z={z_values[2]}")
plt.legend()
plt.show()
