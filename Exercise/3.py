import numpy as np

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return np.cos(x)-x


def bi(a, b, tol=1e-6):
    c_list = []
    b_list = []
    while (b-a)/2 > tol:
        c = (a+b)/2
        c_list.append(c)
        b_list.append(b)
        if f(c) == 0:
            return c, c_list, b_list
        elif f(a)*f(c) < 0:
            b = c
        else:
            a = c
    return (a+b)/2, c_list, b_list


a, b = 0, 2
root, c_list, b_list = bi(a, b)

print(f"The root is: {root:.4f}")

# 创建一个包含两个子图的大图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# 在第一个子图中绘制 c 的折线图
ax1.plot(range(len(c_list)), c_list, linestyle='-', color='blue')
ax1.set_xlabel('Iteration')
ax1.set_ylabel('c')
ax1.set_title('Convergence of c in Bisection Method')

# 在第二个子图中绘制 b 的折线图
ax2.plot(range(len(b_list)), b_list, linestyle='-', color='red')
ax2.set_xlabel('Iteration')
ax2.set_ylabel('b')
ax2.set_title('Convergence of b in Bisection Method')

# 调整子图间的间距
plt.subplots_adjust(wspace=0.3)

plt.show()