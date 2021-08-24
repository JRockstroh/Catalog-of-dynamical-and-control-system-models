# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:19:23 2021

@author: Rocky
"""

import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot
import Stable_PT_n_Class 

xx0_1 = np.zeros(1)
xx0_2 = np.zeros(2)
xx0_3 = np.zeros(3)
xx0_4 = np.zeros(4)
xx0_5 = np.zeros(5)

pp1 = [3, 2]
pp3 = [3, 5, 0.5, 1]
pp4 = [3, 5, 0.5, 1, 2]
pp5 = [3, 5, 0.5, 1, 2, 0.02]

t_end = 30
tt = np.linspace(0, t_end, 1000)



model1 = Stable_PT_n_Class.Model(x_dim=1, pp=pp1)
model2 = Stable_PT_n_Class.Model()
model3 = Stable_PT_n_Class.Model(x_dim=3, pp=pp3)
model4 = Stable_PT_n_Class.Model(x_dim=4, pp=pp4)
model5 = Stable_PT_n_Class.Model(x_dim=5, pp=pp5)
print(model5.get_rhs_symbolic())
sol1 = solve_ivp(model1.get_rhs_func(), (0, t_end), xx0_1, t_eval=tt)
sol2 = solve_ivp(model2.get_rhs_func(), (0, t_end), xx0_2, t_eval=tt)
sol3 = solve_ivp(model3.get_rhs_func(), (0, t_end), xx0_3, t_eval=tt)
sol4 = solve_ivp(model4.get_rhs_func(), (0, t_end), xx0_4, t_eval=tt)
sol5 = solve_ivp(model5.get_rhs_func(), (0, t_end), xx0_5, t_eval=tt)

# create figure + 2x2 axes array
fig1, axs = pyplot.subplots(nrows=2, ncols=2, figsize=(12.8,9.6))
# print in axes top left
axs[0, 0].plot(sol1.t, sol1.y[0], label = 'PT1')
axs[0, 0].plot(sol2.t, sol2.y[0], label = 'PT2')
axs[0, 0].set_ylabel('Amplitude') # y-label Nr 1
axs[0, 0].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[0, 0].grid()
axs[0, 0].legend()

# print in axes top right 
axs[1, 0].plot(sol3.t, sol3.y[0], label = 'PT3')
axs[1, 0].plot(tt, *model3.uu_func(tt, xx0_3), label = 'u')
axs[1, 0].set_ylabel('Amplitude') # y-label Nr 1
axs[1, 0].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1, 0].grid()
axs[1, 0].legend()

# print in axes bottom left
axs[0, 1].plot(sol4.t, sol4.y[0], label = 'PT4')
axs[0, 1].set_ylabel('Amplitude') # y-label Nr 1
axs[0, 1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[0, 1].grid()
axs[0, 1].legend()

# print in axes bottom right
axs[1, 1].plot(sol5.t, sol5.y[0] , label = 'PT5')
axs[1, 1].set_ylabel('Amplitude') # y-label Nr 1
axs[1, 1].set_xlabel('Zeit[t]') # x-Label für Figure linke Seite
axs[1, 1].grid()
axs[1, 1].legend()

# adjust subplot positioning and show the figure
#fig1.suptitle('Simulationen des geschlossenen Kreises, Sprunganregung', fontsize=16)
fig1.subplots_adjust(hspace=0.5)
fig1.show()

# pyplot.plot(sol2.t, sol2.y[0], label = 'PT2')
# pyplot.title('State progress')
# pyplot.xlabel('Time[s]',fontsize= 15)
# pyplot.ylabel('y',fontsize= 15)
# pyplot.legend()
# pyplot.grid()
# pyplot.show()