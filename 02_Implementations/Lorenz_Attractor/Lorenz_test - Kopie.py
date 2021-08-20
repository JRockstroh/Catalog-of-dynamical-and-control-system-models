# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:06:37 2021

@author: Rocky
"""

import numpy as np
import Lorenz_attractor as la
import Lorenz_Attractor_class as lac
from matplotlib import pyplot
from scipy.integrate import solve_ivp
import time
import timeit

start = time.time()

# Defining Input functions
lorenz_att = lac.Model()

rhs_xx_pp_symb = lorenz_att.get_rhs_symbolic()
print(lorenz_att._xxuu_symb)

latt_rhs = lorenz_att.get_rhs_func()

# Initial State values       
xx0 = [0.1, 0.1, 0.1]


t_end = 30
tt = times = np.linspace(0, t_end, 10000) # vector of times for simulation
#sol = solve_ivp(la.lorenz_model, (0,t_end), xx0, t_eval=tt)
sol = solve_ivp(latt_rhs, (0,t_end), xx0, t_eval=tt)

print("Dauer[s]: ", time.time() - start) 

n = 100000
start = time.time()
i = 0
while i < n:
    la.lorenz_model(6, xx0)
    i = i+1
dur = time.time() - start   
print("Dauer Func: ", dur)

start = time.time()
i = 0
while i < n:
    latt_rhs(6, xx0)
    i = i+1
dur = time.time() - start   
print("Dauer Class: ", dur)

func_rhs = la.get_lamb_rhs()
start = time.time()
i = 0
while i < n:
    func_rhs(*xx0)
    i = i+1
dur = time.time() - start   
print("Dauer Func_lamb: ", dur)

class_rhs = latt_rhs
start = time.time()
i = 0
while i < n:
    class_rhs(*xx0)
    i = i+1
dur = time.time() - start   
print("Dauer Class_lamb: ", dur)

pyplot.plot(sol.y[0],sol.y[1],label='', lw=1)

pyplot.title('x-y Phaseplane')
pyplot.xlabel('x',fontsize= 15)
pyplot.ylabel('y',fontsize= 15)
pyplot.legend()
pyplot.grid()
pyplot.show()