# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 18:20:29 2021

@author: Rocky
"""

import sympy as sp

# Define symbols
x, y, z = sp.symbols('x, y, z', real = True)
r, b, sigma = sp.symbols('r, b, sigma', real = True)

# parameter values
p_dict = {r:35, b:2, sigma:20}
p_list = list(p_dict.items())


# symbolic state, input and combined vector
xx = [x,  y, z]

# symbolic model equations
dx1_dt = - sigma*x + sigma*y
dx2_dt = -x*z + r*x - y
dx3_dt = x*y - b*z

dxx_dt = sp.Matrix([dx1_dt, dx2_dt, dx3_dt] )

# Insert parameter values
dxx_dt = dxx_dt.subs(p_list )

# create function for model equations
dxx_dt_func = sp.lambdify(xx, list(dxx_dt), modules = 'numpy')

    
"""RHS-Function of the brockett_model
    Args:
        t (int): time
        x (3darray, int): state vector
    Returns:
        dx/dt (3darray): time derivative of state vector at time t
"""
def lorenz_model(t,xx_nv):
          
    xx_nv = list(xx_nv) 
    
    # calculate dx/dt at time t
    dxx_dt_nv = dxx_dt_func(*xx_nv)

    return dxx_dt_nv

def get_lamb_rhs():
    return dxx_dt_func