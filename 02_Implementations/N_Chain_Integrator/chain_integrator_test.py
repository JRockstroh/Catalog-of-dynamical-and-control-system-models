# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:37:16 2021

@author: Jonathan Rockstroh
"""

import numpy as np
import chain_integrator as ci
import chain_integrator_class as cic
from matplotlib import pyplot
from scipy.integrate import solve_ivp
import time


start = time.time()

# Initial State values       
xx0 = [0, 0, 0, 0, 0]

chain_int = cic.Model(x_dim=len(xx0))


print("xxuu_symb: ", chain_int._xxuu_symb)
rhs_symb = chain_int.get_rhs_symbolic()
print('rhs_symb', rhs_symb)
rhs_num = chain_int.get_rhs_func()

t_end = 30
tt = times = np.linspace(0, t_end, 1000) # vector of times for simulation
#sol = solve_ivp(rhs_num, (0,t_end), xx0, t_eval=tt)
sol = solve_ivp(ci.chain_integrator_model, (0,t_end), xx0, t_eval=tt)

print("Dauer[s]: ", time.time() - start)  

pyplot.plot(sol.t, sol.y[0],label='x1', lw=1)
pyplot.plot(sol.t, sol.y[1],label='x2', lw=1)
pyplot.plot(sol.t, sol.y[2],label='x3', lw=1)
pyplot.plot(sol.t, sol.y[3],label='x4', lw=1)
pyplot.plot(sol.t, sol.y[4],label='x5', lw=1)
pyplot.plot(sol.t, chain_int.uu_func(sol.t, sol.y), label ='u', lw =1)


pyplot.title('State progress')
pyplot.xlabel('Time[s]',fontsize= 15)
pyplot.ylabel('y',fontsize= 15)
pyplot.legend()
pyplot.grid()
pyplot.show()