# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Rocky
"""

import sympy as sp
import numpy as np
import symbtools as st

class Model:
    t_symb = sp.Symbol('t_symb')

    def __init__(self, order = 1, u_func = None):
        """
        :param order:(int > 0), Order of the system, if it is n-extensible
        :param u_func:(object, callable), individual function for the system inputs
        :return:
        """        
        # check order param
        assert(order > 0 and isinstance(order, int)), "Param: <Order> is invalid."
        self.n = order   
       
        # choose input function
        if u_func != None:
             # check if u_func is a callable object 
            assert callable(u_func), "Param: <u_func> is invalid"
            self.uu_func = u_func
        else:
            self.uu_func = self.uu_default_func  
            
        # Define number of inputs
        self.u_order = 1        
        # create symbolic state vector
        self.xx_symb = [sp.Symbol('x'+ str(i)) for i in range(0, self.n)]        
        # create symbolic input 
        self.uu_symb = [sp.Symbol('u'+ str(i)) for i in range(0, self.u_order)]        
        self._xxuu_symb = self.xx_symb + self.uu_symb
        
 
    def set_input_func(self, u_func):
        """
        :u_func:(object, callable), individual function for the system inputs
        :return:
        """       
        # check if u_func is a callable object 
        assert callable(u_func)
        # assign given function to object variable        
        self.uu = u_func

    # Function only exists if System is n-extensible
    def set_order(self, order):
        """
        :param order:(int > 0), Order of the system
        """
        assert(order > 0 and isinstance(order, int))
        self.n = order
   
     
    def uu_default_func(self, t, xx_sp):
        """
        :param t: (scalar or vector) time value 
        :param xx_nv: (vector or array of vectors) state vector with numerical values at time t      
        :return:(function) default input function
        """       
        T0 = 0
        T1 = 5
        y0 = 5
        y1 = 0
        # create symbolic polnomial function
        poly = st.condition_poly((T0, y0, 0, 0), (T1, y1, 0, 0))
        # create symbolic piecewise defined symbolic transition function
        transition = st.piece_wise((0, self.t_symb < 0), (poly, t < T1), (y1, True))
        # transform symbolic to numeric function 
        transition_func = st.expr_to_func(self.t_symb, transition) 
        
        return transition_func
         
        
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """       
        # create symbolic rhs function vector
        dxx_dt_symb = self.xx_symb[1:]
        dxx_dt_symb[-1] = self.uu_symb
        
        return dxx_dt_symb
    
    
    def get_rhs_func(self):
        """
        :return: (function) rhs function for numerical solver
        """
        # transform symbolic function to numerical function
        dxx_dt_func = st.expr_to_func(self._xxuu_symb, self.get_rhs_symbolic())
        # create rhs function
        def rhs(t, xx_nv):           
            uu_nv = self.uu_func(t, xx_nv)       
            # combine numerical state and input vector
            xxuu_nv = list(xx_nv) + list(uu_nv)            
            # evaluate function
            dxx_dt_nv = dxx_dt_func(*xxuu_nv)
            
            return dxx_dt_nv
            
        return rhs
    
    