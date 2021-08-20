# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:55:41 2021

@author: Rocky
"""

import numpy as np
import time


# Parameter Values
p_dict = {'vdc':300,'vg':0,'omega':2*np.pi*5,'Mz':0.94/1000,\
          'Lz':1.2/1000,'R':26,'L':3/1000}
p_list = list(p_dict.items())

vdc = p_dict['vdc']
vg = p_dict['vg']
omega = p_dict['omega']
Mz = p_dict['Mz']
Lz = p_dict['Lz']
R = p_dict['R']
L = p_dict['L']
Ind_sum = Lz + Mz 

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
    es0, ed0, es, ed, iss, iss0, i, theta = xx_nv
    # Define Input Functions
    Kp = 5
        # define reference trajectory for i
    T_dur = 1.5
    tau = t/T_dur
    i_max = 10

    i_ref = 10
    dt_i_ref = 0
    if (tau < 1):
        i_ref = 4 + (i_max - 4) *np.sin( 0.5*tau *np.pi) *np.sin( 0.5*tau *np.pi)
        dt_i_ref = np.pi/T_dur * np.sin( 0.5*tau *np.pi) * np.cos( 0.5*tau *np.pi)
    if (t < 1):
        i_ref = 4
        dt_i_ref = 0  
    
    vy = vg - (R+1j*omega*L) *i + 1*(i_ref - i) + L *dt_i_ref
    vy = complex( vy)
    vy0 = -1/6 *np.absolute( vy) *np.real( np.exp( 3*1j*(theta + np.angle( vy) ) ) )
    vx = 1j *omega*Ind_sum*iss - Kp*iss # p- controller to get iss
    
        # define reference trajectory of es0
    T_dur = 0.5 #duration of es0 ref_traj
    tau = t/T_dur
    es0_max = 68
    #es0_ref = sp.Piecewise((0, tau < 0), (es0_max *sp.sin( tau*sp.pi/2)  \
    #                        *sp.sin( tau*sp.pi/2), tau < 1), (es0_max, True) )
    es0_ref = 56
        # derive iss0 ref trajectory
    iss0_ref = 1/vdc *np.real( i *np.conjugate( vy)) + Kp *(es0_ref - es0)
    
        # p-controller for vx0
    vx0 = Kp*(iss0_ref - iss0)    
    
    # create functions for the input equations
    uu_nv = [vy, vy0, vx, vx0]
    
    return uu_nv

"""RHS-Function of the MMC_model
    Args:
        t (int): time
        x (8darray, complex): state vector
    Returns:
        dx/dt (8dlist): time derivative of state vector at time t
"""  
dur_es0 = 0
dur_ed0 = 0
dur_es = 0
dur_ed = 0
dur_iss = 0
dur_iss0 = 0
dur_i = 0
dur_theta = 0
dur_uu = 0
calls = 0
  
def MMC_model(t,xx_nv):    
    
    global dur_es0 
    global dur_ed0 
    global dur_es 
    global dur_ed 
    global dur_iss 
    global dur_iss0 
    global dur_i 
    global dur_theta
    global dur_uu 
    
    start = time.time()    
    vy, vy0, vx, vx0 = uu(xx_nv,t)
    dur_uu = dur_uu + time.time() - start
#    vy = 4+0j
#    vy0 = 1
#    vx = 2+1j
#    vx0 = 1     
    es0, ed0, es, ed, iss, iss0, i, theta = xx_nv     
    
    vydelta = vy - Mz *(1j *omega*i + 1/L *(vy - (R + 1j *omega*L) *i - vg) ) # = vy-Mz(j*omega*i-dt_i)
    
    start = time.time() 
    dt_es0 = vdc*iss0 - np.real(i*np.conjugate( vy) )
    dur_es0 = dur_es0 + time.time() - start
    
    start = time.time() 
    dt_ed0 = -2 *vy0*iss0 - np.real(np.conjugate( iss)*vydelta )
    dur_ed0 = dur_ed0 + time.time() - start
    
    start = time.time() 
    dt_es = vdc*iss - np.exp( -3*1j*theta) *np.conjugate( vy) *np.conjugate( i) \
            - 2 *i*vy0 - 1j *omega*es
    dur_es = dur_es + time.time() - start
    
    start = time.time() 
    dt_ed = vdc*i - np.exp( -3*1j*theta) *np.conjugate( iss) *np.conjugate( vydelta)\
            - 2 *iss*vy0 - 2 *iss0*vydelta - 1j *omega*ed      
    dur_ed = dur_ed + time.time() - start
    
    start = time.time() 
    dt_iss = 1/Ind_sum * (vx -  1j*omega*Ind_sum*iss)
    dur_iss = dur_iss + time.time() - start
    
    start = time.time() 
    dt_iss0 = vx0/Ind_sum
    dur_iss0 = dur_iss0 + time.time() - start
    
    start = time.time() 
    dt_i = 1/L * (vy - (R+1j *omega*L) *i - vg)
    dur_i = dur_i + time.time() - start
 
    start = time.time() 
    dt_theta = omega
    dur_theta = dur_theta + time.time() - start
    
    dur_list = [dur_es0, dur_ed0, dur_es, dur_ed, dur_iss, dur_iss0, dur_i, dur_theta, dur_uu]
    dur_list = list(np.around(np.array(dur_list),2))
    
    global calls
    calls = calls + 1
    print("Dauer[s] - es0, ed0, es, ed, is, is0, i, theta ,uu: ", dur_list)
    print("Calls: ", calls)
    dxx_dt_nv = [dt_es0, dt_ed0, dt_es, dt_ed, dt_iss, dt_iss0, dt_i, dt_theta]
    #print("Ping:t={}".format(t))
    return dxx_dt_nv


                     
                     
                     
