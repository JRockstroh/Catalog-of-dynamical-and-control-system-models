# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:46:19 2021

@author: Rocky
"""

import numpy as np
import Brockett
from matplotlib import pyplot
from scipy.integrate import solve_ivp
import Brockett_class as bs

# Defining Input functions

model = bs.Model()

rhs_func = model.get_rhs_func()

xx0 = [0, 0, 0]


t_end = 10
tt = times = np.linspace(0, t_end, 1000) # vector of times for simulation
sol = solve_ivp(rhs_func, (0, t_end), xx0, t_eval=tt)

pyplot.plot(sol.t,sol.y[0],label='x1')
pyplot.plot(sol.t,sol.y[1],label='x2')
pyplot.plot(sol.t,sol.y[2],label='x3')


pyplot.title('Zustandsverläufe')
pyplot.xlabel('Zeit t', fontsize= 15)
#pyplot.ylabel('Zeit t', fontsize= 15)
pyplot.legend()
pyplot.grid()
pyplot.show()