# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:06:26 2021

@author: Jonathan Rockstroh
"""

import numpy as np
import chain_integrator_class as cic

order = 5
chain_int = cic.Chain_Integrator_Model(order)

u = chain_int.uu_func
   
"""RHS-Function of the brockett_model
    Args:
        t (float, positive): time
        x (ndarray): state vector
    Returns:
        dx/dt (ndarray): time derivative of state vector at time t
"""

def chain_integrator_model(t, xx_nv):
          
    dxx_dt_nv = xx_nv*1        
    dxx_dt_nv[:-1] = xx_nv[1:]    
    dxx_dt_nv[-1] = u(t, xx_nv)

    return dxx_dt_nv