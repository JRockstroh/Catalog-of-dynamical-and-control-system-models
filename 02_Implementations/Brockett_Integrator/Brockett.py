# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:54:15 2021

@author: Rocky
"""

import sympy as sp

# Define symbols
x1, x2, x3 = sp.symbols('x1, x2, x3', real = True)
u1, u2 = sp.symbols('u1, u2', real = True)

# symbolic state, input and combined vector
xx = [x1,  x2, x3]
uu = [u1, u2]
xxuu = xx + uu

# symbolic model equations
dx1_dt = u1
dx2_dt = u2
dx3_dt = x2*u1 - x1*u2 

dxx_dt = sp.Matrix([dx1_dt, dx2_dt, dx3_dt] )

# create function for model equations
dxx_dt_func = sp.lambdify(xxuu, list(dxx_dt), modules = 'numpy')

# define Input functions

"""Input Functions for the brockett_model
    Args:
        xx (3darray): state vector
        t (int): time
        p (ndarray, int): parameter
    Returns:
        uu (2darray): input vector
    
"""
def uu(xx,t,p=None):
    u1, u2 = 0,0
    if t > 0:
        u1 = 4-t#4-xx[0]
        u2 = (t-5)#2-xx[1]  
    return [u1,u2] 

    
"""RHS-Function of the brockett_model
    Args:
        t (int): time
        x (3darray, int): state vector
    Returns:
        dx/dt (3darray): time derivative of state vector at time t
"""

def brockett_model(t,xx_nv):
      
    uu_nv = uu(xx,t)
    
    xxuu_nv = list(xx_nv) + list(uu_nv)
    
    # calculate dx/dt at time t
    dxx_dt_nv = dxx_dt_func(*xxuu_nv)

    return dxx_dt_nv
