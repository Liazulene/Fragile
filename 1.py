import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 5, 1000)  # 在[0,5]内均匀取1000个点
a_list = [2, 3, 4]  # 不同的a值

for a in a_list:
    y = x**(a-1) * np.exp(-x)
    plt.plot(x, y, label=f'a = {a}')

plt.legend()  # 显示图例
plt.xlabel('x')
plt.ylabel('y')
plt.title('x**(a-1)*exp(-x) for different a')
plt.show()
