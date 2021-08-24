# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:43:36 2021

@author: Jonathan Rockstroh
"""

import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot
import MMC_NP
import MMC_class 

import pprint
import time

model = MMC_class.Model()

print("Symbolic rhs: ", model.get_rhs_symbolic())

rhs_func = model.get_rhs_func()

start = time.time()

xx0 = [0, 0, 0+0j, 0+0j, 0+0j, 0, 0+0j, 0]
t_end = 4
tt = np.linspace(0, t_end, 10000)
# use separate written model/rhs functions
#sol = solve_ivp(MMC_NP.MMC_model, (0, t_end), xx0, t_eval=tt)
# use model class rhs
sol = solve_ivp(rhs_func, (0, t_end), xx0, t_eval=tt)


print("Dauer[s]: ", time.time() - start)    

y = np.abs(sol.y)

i = 0
uu = [[], [], [], []]

while i < len(sol.t):
    #tmp = MMC.uu(sol.y[:, i], sol.t[i])
    tmp = model.uu_func(sol.t[i], sol.y[:, i])
    n = 0
    while n < len(uu):
        uu[n].append(tmp[n])
        n = n+1
    i = i+1

# uu = model.uu_func(sol.t, sol.y)

# create figure + 2x2 axes array
fig1, axs = pyplot.subplots(nrows=2, ncols=2, figsize=(12.8,9.6))

# print in axes top left
axs[0, 0].plot(sol.t, np.real(sol.y[1] ), label = 'Re' )
axs[0, 0].set_ylabel('ed0') # y-label Nr 1
axs[0, 0].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[0, 0].grid()
axs[0, 0].legend()

# print in axes top right 
axs[1, 0].plot(sol.t, np.real(sol.y[2] ), label = 'Re')
axs[1, 0].plot(sol.t, np.imag(sol.y[2] ), label = 'Im')
axs[1, 0].set_ylabel('es') # y-label Nr 1
axs[1, 0].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1, 0].grid()
axs[1, 0].legend()

# print in axes bottom left
axs[0, 1].plot(sol.t, np.real(sol.y[3] ), label = 'Re')
axs[0, 1].plot(sol.t, np.imag(sol.y[3] ), label = 'Im')
axs[0, 1].set_ylabel('ed') # y-label Nr 1
axs[0, 1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[0, 1].grid()
axs[0, 1].legend()

# print in axes bottom right
axs[1, 1].plot(sol.t, uu[0] , label = 'vy')
axs[1, 1].plot(sol.t, uu[1] , label = 'vy0')
axs[1, 1].set_ylabel('') # y-label Nr 1
axs[1, 1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1, 1].grid()
axs[1, 1].legend()

# adjust subplot positioning and show the figure
#fig1.suptitle('Simulationen des geschlossenen Kreises, Sprunganregung', fontsize=16)
fig1.subplots_adjust(hspace=0.5)
fig1.show()


