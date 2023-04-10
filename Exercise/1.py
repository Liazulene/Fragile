import numpy as np


def g(p, a):
    if (p > 0) and (p < 1):
        return np.power(-np.log(p), a-1)
    else:
        return 0


vg = np.vectorize(g)
a = 4

p_list = np.linspace(0, 1, 4001)
p_list = np.delete(p_list, 0)
g_list = vg(p_list, a)
l_list = list(range(1, len(p_list)))

# print(g_list)

i = 0.0
for l in l_list:
    i += 0.5*(g_list[l]+g_list[l-1])*(p_list[l]-p_list[l-1])

print(i)
