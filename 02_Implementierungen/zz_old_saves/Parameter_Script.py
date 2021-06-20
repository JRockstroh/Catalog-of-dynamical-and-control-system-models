# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 14:13:01 2021

@author: Rocky
"""

import numpy as np
import sympy as sp

####### DEFINE PARAMETERS #######

vdc = 300
vg = 0
omega = 2*np.pi*5
Mz = 0.94/1000
Lz = 1.2
R = 26
L = 3/1000

vdc, vg, R = sp.symbols('vdc, vg, R')
pp_symb = [vdc, vg, R]
pp = [2, 3, 4]
pp_dict = {pp_symb[i]:pp[i] for i in range(3)}
print(list(sp.Matrix(pp_symb)))

def get_default_param():
    return pp_dict