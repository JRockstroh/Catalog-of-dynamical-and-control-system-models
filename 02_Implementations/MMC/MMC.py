# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:55:41 2021

@author: Rocky
"""

import sympy as sp
from sympy import I
import numpy as np
from scipy.integrate import solve_ivp

# Define all real Variables as Symbols

es0,ed0,theta,omega = sp.symbols('es0,ed0,theta,omega',real=True)
vdc,vy0,vx0,iss0 = sp.symbols('vdc,vy0,vx0,iss0',real=True)
Lz,Mz,R,L,Ind_sum,vydelta = sp.symbols('Lz,Mz,R,L,Ind_sum,vydelta',real=True)
t_sp = sp.symbols('t_sp',real=True)

# Define all complex Variables as Symbols
es,ed,vy,vx,vg,i,iss = sp.symbols('es,ed,vy,vx,vg,i,iss')
esr,esi = sp.symbols('esr,esi',real=True)
#es = esr+I*esi
edr,edi = sp.symbols('edr,edi',real=True)
#ed = edr+I*edi
vyr,vyi = sp.symbols('vyr,vyi',real=True)
#vy = vyr+I*vyi
vxr,vxi = sp.symbols('vxr,vxi',real=True)
#vx = vxr + I*vyi
vgr,vgi = sp.symbols('vgr,vgi',real=True)
#vg = vgr + I*vgi
ir,ii = sp.symbols('ir,ii',real=True)
#i = ir + I*ii
issr,issi = sp.symbols('issr,issi',real=True)
#iss = issr+I*issi

# Parameter Values
p_dict = {vdc:300,vg:0,omega:2*np.pi*5,Mz:0.94/1000,\
          Lz:1.2/1000,R:26,L:3/1000}
p_list = list(p_dict.items())

# symbolic state, input and combined vector
xx = [es0, ed0, es, ed, iss, iss0, i, theta]
uu = [vy, vy0, vx, vx0]
xxuu = xx + uu

# auxiliary variable
Ind_sum = Lz + Mz 
vydelta = vy - Mz *(I *omega*i + 1/L *(vy - (R + I *omega*L) *i - vg) ) # = vy-Mz(j*omega*i-dt_i)


# Symbolic Model Equations
dt_es0 = vdc*iss0 - sp.re(i*sp.conjugate( vy) )
dt_ed0 = -2 *vy0*iss0 - sp.re(sp.conjugate( iss)*vydelta )
dt_es = vdc*iss - sp.exp( -3*I*theta) *sp.conjugate( vy) *sp.conjugate( i) \
        - 2 *i*vy0 - I *omega*es
dt_ed = vdc*i - sp.exp( -3*I*theta) *sp.conjugate( iss) *sp.conjugate( vydelta)\
        - 2 *iss*vy0 - 2 *iss0*vydelta - I *omega*ed
dt_iss = 1/Ind_sum * (vx -  I*omega*Ind_sum*iss)
dt_iss0 = vx0/Ind_sum
dt_i = 1/L * (vy - (R + I *omega*L) *i - vg) 
dt_theta = omega

print(sp.latex(dt_es))

dxx_dt = sp.Matrix([dt_es0, dt_ed0, dt_es, dt_ed, dt_iss, dt_iss0, dt_i, dt_theta] )

# Insert parameter values
dxx_dt = dxx_dt.subs(p_list )

# create function for Model Equations
dxx_dt_func = sp.lambdify(xxuu, list( dxx_dt), modules = 'numpy')


# Define Input Functions
Kp = 5
    # define reference trajectory for i
T_dur = 2
tau = t_sp/T_dur
i_max = 10
i_ref = sp.Piecewise((4, t_sp < 1), (i_max *sp.sin( tau*sp.pi/2)  \
                        *sp.sin( tau*sp.pi/2), tau < 1), (i_max, True) )

vy = vg - (R+I *omega*L) *i + 1*(i_ref - i) + L*i_ref.diff(t_sp)
vy0 = -1/6 *sp.Abs( vy) *sp.re( sp.exp( 3*I*(theta + sp.arg( vy) ) ) )
vx = I *omega*Ind_sum*iss - Kp*iss # p- controller to get iss

    # define reference trajectory of es0
T_dur = 0.5 #duration of es0 ref_traj
tau = t_sp/T_dur
es0_max = 68
#es0_ref = sp.Piecewise((0, tau < 0), (es0_max *sp.sin( tau*sp.pi/2)  \
#                        *sp.sin( tau*sp.pi/2), tau < 1), (es0_max, True) )
es0_ref = 56
    # derive iss0 ref trajectory
iss0_ref = 1/vdc *sp.re( i *sp.conjugate( vy)) + Kp *(es0_ref - es0)

    # p-controller for vx0
vx0 = Kp*(iss0_ref - iss0)

uu_sp = sp.Matrix([vy, vy0, vx, vx0] )

# insert parameter values
uu_sp = uu_sp.subs(p_list )

# create functions for the input equations
xxt = xx + [t_sp]
uu_func = sp.lambdify(xxt, list(uu_sp), modules = 'numpy')


# SCHEMA: vx0_func = sp.lambdify(xx, vx0, modules='numpy')
# AUSWERTUNG: vx_func(*xx)
"""Input Functions for the MMC
    Args:
        xx (8darray): state vector
        t (int): time
        p (ndarray, int): parameter
    Returns:
        uu (4dlist): input vector
    
"""
def uu(xx_nv,t,p=None):
    es0_nv, ed0_nv, es_nv, ed_nv, iss_nv, iss0_nv, i_nv, theta_nv = xx_nv
    xxt_nv = list(xx_nv) + [t]

    uu_nv = uu_func(*xxt_nv)
    
    return uu_nv

"""RHS-Function of the MMC_model
    Args:
        t (int): time
        x (8darray, complex): state vector
    Returns:
        dx/dt (8dlist): time derivative of state vector at time t
"""  
def MMC_model(t,xx_nv):    
    
    vy_nv,vy0_nv,vx_nv,vx0_nv = uu_nv = uu(xx_nv,t) 
#    vy_nv,vy0_nv,vx_nv,vx0_nv = uu_nv = [4+0j, 3, 2+0.5j, 2] 
    
    xxuu_nv = list(xx_nv) + list(uu_nv)    
    
    dxx_dt_nv = dxx_dt_func(*xxuu_nv)

    #print("Ping:t={}".format(t))
    return dxx_dt_nv



