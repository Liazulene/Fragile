import math


def g(x):
    return math.asin(math.cos(x))


# 初始值
x0 = 0

# 迭代次数
N = 10

# 迭代
for i in range(N):
    x1 = g(x0)
    print("x{} = {}".format(i+1, x1))
    x0 = x1
