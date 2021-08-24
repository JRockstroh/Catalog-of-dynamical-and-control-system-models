# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:48:01 2021

@author: Rocky
"""

import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot 
from mpl_toolkits.mplot3d import Axes3D
import Roessler_class as rs
import time



model = rs.Model()
rhs_func = model.get_rhs_func()


xx0 = [2,3,4]
t_end = 300
tt = np.linspace(0,t_end,6000)

start = time.time()
sol = solve_ivp(rhs_func, (0, t_end), xx0, t_eval=tt)

print("Duration: ", time.time()-start)

y = sol.y.tolist()

fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(y[0],y[1],y[2],label='Phasenportrait',lw=1,c='k')
#pyplot.title('Zustandsverläufe')
ax.set_xlabel('x',fontsize= 15)
ax.set_ylabel('y',fontsize= 15)
ax.set_zlabel('z',fontsize= 15)
ax.legend()
ax.grid()
pyplot.show()