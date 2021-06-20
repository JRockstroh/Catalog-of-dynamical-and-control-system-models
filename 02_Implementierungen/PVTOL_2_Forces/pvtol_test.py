# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:00:47 2021

@author: Jonathan Rockstroh
"""

import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot
import pvtol_class as pcls

model = pcls.Model()

rhs_func = model.get_rhs_func()

xx0 = np.zeros(6)

t_end = 20

tt = np.linspace(0, t_end, 10000)

sol = solve_ivp(rhs_func, (0, t_end), xx0, t_eval=tt)

uu = model.uu_func(sol.t, sol.y)

# create figure + 2x2 axes array
fig1, axs = pyplot.subplots(nrows=2, ncols=1, figsize=(12.8,9.6))

# print in axes top 
# axs[0].plot(sol.y[0], np.real(sol.y[2] ), label = 'Position' )
# axs[0].set_ylabel('y[m]') # y-label Nr 1
# axs[0].set_xlabel('x[m]') # x-Label für Figure linke Seite
# axs[0].grid()
# axs[0].legend()

axs[0].plot(sol.t, np.real(sol.y[0] ), label = 'x-Position' )
axs[0].plot(sol.t, np.real(sol.y[2] ), label = 'y-Position' )
axs[0].plot(sol.t, np.real(sol.y[4] ), label = 'angle' )
axs[0].set_ylabel('Pos[m]') # y-label Nr 1
axs[0].set_xlabel('Time[s]') # x-Label für Figure linke Seite
axs[0].grid()
axs[0].legend()


# print in axes bottom 
axs[1].plot(sol.t, uu[0] , label = 'Force left')
axs[1].plot(sol.t, uu[1] , label = 'Force right')
axs[1].set_ylabel('') # y-label Nr 1
axs[1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1].grid()
axs[1].legend()

# adjust subplot positioning and show the figure
#fig1.suptitle('', fontsize=16)
fig1.subplots_adjust(hspace=0.5)
fig1.show()
