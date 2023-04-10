import numpy as np

a = np.array([[2, 3, 5], [7, 11, 13]])

b = np.arange(1, np.prod(a.shape) + 1).reshape(a.shape)

print(b)
