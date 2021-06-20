# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:06:37 2021

@author: Rocky
"""

import numpy as np
import Lorenz_Attractor_class as lac
from matplotlib import pyplot
from scipy.integrate import solve_ivp

# Defining Input functions
lorenz_att = lac.Model()

rhs_xx_pp_symb = lorenz_att.get_rhs_symbolic()


latt_rhs = lorenz_att.get_rhs_func()

# Initial State values       
xx0 = [0.1, 0.1, 0.1]


t_end = 30
tt = times = np.linspace(0, t_end, 10000) # vector of times for simulation
sol = solve_ivp(latt_rhs, (0,t_end), xx0, t_eval=tt)

pyplot.plot(sol.y[0],sol.y[1],label='', lw=1)

pyplot.title('x-y Phaseplane')
pyplot.xlabel('x',fontsize= 15)
pyplot.ylabel('y',fontsize= 15)
pyplot.legend()
pyplot.grid()
pyplot.show()