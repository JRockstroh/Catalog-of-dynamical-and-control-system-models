# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:06:37 2021

@author: Jonathan Rockstroh
"""

import numpy as np
import Lorenz_Attractor_class_compare as laccomp


from matplotlib import pyplot
from scipy.integrate import solve_ivp
import time

# Defining Model - Modelle haben unterschiedliche 
model = laccomp.Model()


rhs_xx_pp_symb = model.get_rhs_symbolic()

rhs_ST = model.get_rhs_func_ST() # rhs über lambdify erstellt
rhs_lamb = model.get_rhs_func_lamb() # rhs über st.expr_to_func erstellt

# Initial State values       
xx0 = [0.1, 0.1, 0.1]


t_end = 30
tt = times = np.linspace(0, t_end, 10000) # vector of times for simulation

# SIMULATE
# Simulate with ST - Function
start = time.time()
sol_ST = solve_ivp(rhs_ST, (0,t_end), xx0, t_eval=tt)
time_sol_ST = time.time() - start

# Simulate with lamb function
start = time.time()
sol_lamb = solve_ivp(rhs_lamb, (0,t_end), xx0, t_eval=tt)
time_sol_lamb = time.time() - start

# EVALUATE FUNCTIONS 100000 times
amount = 100000
random_time = 5 # rhs braucht t-parameter, Wert is unwichtig
# ST Function 
i = 0
start = time.time()
while i < amount:
    rhs_ST(random_time, xx0)
    i = i + 1
time_amount_ST = time.time() - start

# Lambdify Function
start = time.time()
i = 0
while i < amount:
    rhs_lamb(random_time, xx0)
    i = i + 1
time_amount_lamb = time.time() - start

# Drucke Ergebnisse in Konsole
print("Simulationszeit mit ST[s]: %.3f"% time_sol_ST)
print("Simulationszeit mit Lamb[s]: %.3f"% time_sol_lamb)
print("Simulation: ST braucht %.2f fache Zeit von Lamb." %(time_sol_ST/time_sol_lamb))
print("")
print("Zeit %d Auswertungen ST[s]: %.3f" %(amount, time_amount_ST))
print("Zeit %d Auswertungen Lamb[s] %.3f: " %(amount, time_amount_lamb))
print("%d Auswertungen: ST braucht %.2f fache Zeit von Lamb." %(amount, time_amount_ST/time_amount_lamb))

# Plotte Ergebnisse beider Simulationen in das selbe Fenster
pyplot.plot(sol_ST.y[0],sol_ST.y[1],label='ST', lw=1)
pyplot.plot(sol_lamb.y[0],sol_lamb.y[1],label='Lamb', lw=1)

pyplot.title('x-y Phaseplane')
pyplot.xlabel('x',fontsize= 15)
pyplot.ylabel('y',fontsize= 15)
pyplot.legend()
pyplot.grid()
pyplot.show()