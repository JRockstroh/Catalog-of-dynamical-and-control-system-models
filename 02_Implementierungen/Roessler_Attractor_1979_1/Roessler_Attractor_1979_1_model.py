# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:06:06 2021

@author: Rocky
"""

import sympy as sp
import numpy as np

x,y,z = sp.symbols('x,y,z')
a,b,c = sp.symbols('a,b,c')

# Dictionary with parameter values
p_dict = {a:0.38, b:0.3, c:4.84 }

# symbolic state vector
xx = [x, y, z]

# Symbolic Model Equations
dx_dt = - y - z
dy_dt = x + a*y
dz_dt = b*x - c*z + x*z

dxx_dt = sp.Matrix([dx_dt, dy_dt, dz_dt])

# Substitute Parameter Values
p_list = list(p_dict.items() )
dxx_dt = dxx_dt.subs(p_list )

# Model equation functions
dxx_dt_func = sp.lambdify(xx, list(dxx_dt), modules='numpy')

def roessler_1979_1(t,xx_nv):
    x_nv,y_nv,z_nv = xx_nv
    
    dxx_dt_nv = dxx_dt_func(*xx_nv)
    
    return dxx_dt_nv

