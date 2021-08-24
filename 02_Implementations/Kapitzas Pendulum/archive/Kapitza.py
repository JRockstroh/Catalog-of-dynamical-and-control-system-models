# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:54:15 2021

@author: Rocky
"""

import sympy as sp
import numpy as np

# Define symbols
phi, phidt = sp.symbols('phi, phidt', real = True)
g, l, a, omega, gamma, t_sp = sp.symbols('g, l, a, omega, gamma, t_sp', real = True)

# Parameter Values
p_dict = {g:9.81, l:10, a:2, omega:16*np.sqrt(9.81/10), gamma:0.1*np.sqrt(9.81/10)}
p_list = list(p_dict.items())


# symbolic state, input and combined vector
xx = [phi, phidt]


# symbolic model equations
dphi_dt = phidt 
dphidt_dt = -2*gamma*phidt - (g/l - a/l * omega**2 *sp.sin(omega*t_sp)) *sp.sin(phi)

dxx_dt = sp.Matrix([dphi_dt, dphidt_dt] )

# Insert parameter values
dxx_dt = dxx_dt.subs(p_list )

# create function for model equations
xxt = xx + [t_sp]
dxx_dt_func = sp.lambdify(xxt, list(dxx_dt), modules = 'numpy')

# define Input functions
u = a*sp.sin(omega*t_sp)
u = u.subs(p_list)
u_func = sp.lambdify(t_sp, u, modules = 'numpy')

"""Input Functions for the brockett_model
    Args:
        xx (3darray): state vector
        t (int): time
        p (ndarray, int): parameter
    Returns:
        uu (2darray): input vector
    
"""
def uu(xx,t,p=None):
    u = u_func(t)
    return u 

    
"""RHS-Function of the brockett_model
    Args:
        t (int): time
        x (2darray, float): state vector
    Returns:
        dx/dt (3darray): time derivative of state vector at time t
"""

def kapitza_model(t,xx_nv):
    
    xxt_nv = list(xx_nv) + [t]   
    # calculate dx/dt at time t
    dxx_dt_nv = dxx_dt_func(*xxt_nv)

    return dxx_dt_nv
