import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

N = 100
U = np.zeros((N,N),float)
threshold = 1e-13

U[:,0] = 100
Q=0

while True:
    Q += 1
    U_old = U
    for i in range(1,N-2):
        for j in range(1,N-2):
            U[i,j] = 0.25*(U_old[i+1,j]+U_old[i-1,j]+U_old[i,j+1]+U_old[i,j-1])
    diff = np.linalg.norm(np.subtract(U, U_old))
    
    if diff < threshold:
        break

x = range(0,N-1)
y = range(0,N-1)
X,Y = np.meshgrid(x,y)
Z = U[X,Y]

fig = plt.figure(figsize=(10,10))
ax = Axes3D(fig)
ax.set_xlim3d(0, N-1)
ax.set_ylim3d(0, N-1)
ax.set_zlim3d(0, 100)
ax.plot_surface(X,Y,Z,alpha=0.7)
ax.contourf(X,Y,Z,zdir='z',offset=100,cmap='coolwarm')
plt.show()
print(Q)
print(U)
print(diff)