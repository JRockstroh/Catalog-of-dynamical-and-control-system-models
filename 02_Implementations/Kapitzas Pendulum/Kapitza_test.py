# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:46:19 2021

@author: Rocky
"""

import numpy as np
from matplotlib import pyplot
from scipy.integrate import solve_ivp
from matplotlib import rc
import Kapitzas_Pendulum_class as kpc

# Defining Input functions

model = kpc.Model()        
rhs_func = model.get_rhs_func()


xx0 = [200/360*2*np.pi,0]



t_end = 1
tt = times = np.linspace(0,t_end,10000) # vector of times for simulation
sol = solve_ivp(rhs_func, (0, t_end), xx0, t_eval=tt)


uu = model.uu_func(sol.t, xx0)[0] *0.005 +180


# create figure + 2x2 axes array
fig1, axs = pyplot.subplots(nrows=2, ncols=1, figsize=(12.8,9.6))

# print in axes top left
axs[0].plot(sol.t, np.real(sol.y[0]*360/(2*np.pi)), label = 'Phi')
#axs[0].plot(sol.t, np.real(sol1.y[0]*360/(2*np.pi)), label = 'Phi_old')
axs[0].plot(sol.t, list(uu), label ='z(t)')
#axs[0].set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
#axs[0].set_yticklabels([r'-$\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'])
axs[0].set_ylabel('Winkel[rad]') # y-label Nr 1
axs[0].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[0].grid()
axs[0].legend()

# print in axes top right 
axs[1].plot(sol.t, np.real(sol.y[1] ), label = 'Phi_dot')
axs[1].set_ylabel('Winkelgeschwindigkeit[rad/s]') # y-label Nr 1
axs[1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1].grid()
axs[1].legend()


# adjust subplot positioning and show the figure
#fig1.suptitle('Simulationen des geschlossenen Kreises, Sprunganregung', fontsize=16)
fig1.subplots_adjust(hspace=0.5)
fig1.show()
