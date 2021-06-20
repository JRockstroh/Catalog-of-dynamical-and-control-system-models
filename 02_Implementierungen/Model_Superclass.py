# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:55:35 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
from collections.abc import Mapping
import warnings
import abc

class Model_Superclass:
    t_symb = sp.Symbol('t')
    
    def __init__(self, x_dim=None, u_func=None, pp=None):
        """
        :param x_dim:(int, positive) dimension of the state vector 
                                - has no effect for non-extendible systems
        :param u_func:(callable) input function, args: time, state vector
                        return: list of numerical input values 
                        - has no effect for autonomous systems    
        :param pp:(vector or dict-type with floats>0) parameter values
        :return:
        """
        # Initialize all Parameters of the Model-Object with None    
        # System Dimension
        self.n = None
        # Symbolic State Vector
        self.xx_symb = None
        # Symbolic Input Vector
        self.uu_symb = None
        # Symbolic combined vector
        self._xxuu_symb = None
        # Symbolic rhs-vector (first derivative)
        self.dxx_dt_symb = None
        # Symbolic parameter vector
        self.pp_symb = None
        # Parameter dictionary with symbol:value entries 
        self.pp_dict = None
        # Parameter Substitution List for sp.subs methods
        self.pp_subs_list = None
        # Input function
        self.uu_func = None
        

    # ----------- SET NEW INPUT FUNCTION ---------- # 
    # --------------- Only for non-autonomous Systems
# ??? u_func validation sinnvoll?    
    def set_input_func(self, u_func):
        """
        :u_func:(object, callable), individual input function
        """
        # check if u_func is a callable object 
        assert callable(u_func), ":param u_func: isn't a callable object." 
        # assign given function to object variable        
        self.uu_func = u_func


    # ----------- SET DEFAULT INPUT FUNCTION ---------- # 
    # --------------- Only for non-autonomous Systems
    # --------------- MODEL DEPENDENT
    
    @abc.abstractmethod    
    def uu_default_func(self):
        """
        :param t:(scalar or vector) Time
        :param xx_nv: (vector or array of vectors) state vector with 
                                                    numerical values at time t      
        :return:(function with 2 args - t, xx_nv) default input function 
        """ 
     
        
    # ----------- SET STATE VECTOR DIMENSION ---------- # 
    
    def _set_dimension(self, x_dim, pp = None):
        """
        :param dim:(int > 0), Order of the system
        """
        # check if system is n-extendable
        if self.n is not None:
            warnings.warn("Function \"set_dimension\" had no effect. \
                          System is not n-extendable.")            
            return
        # check if :param dim: is valid -- ADJUSTION NEEDED IN SPECIAL CASES
        assert(x_dim > 0 and isinstance(x_dim, int)), \
                "Param: x_dim isn't valid."
        self.n = x_dim

    
    # ----------- CREATE INDIVIDUAL P DICT  ---------- #
    
    def _create_individual_p_dict(self, pp, pp_symb=None):
        """
        :param pp:(list or dict) 
        """
# ??? Sinnvoll Instance-Abfrage auf Mapping zu setzen, wenn danach dict-spezifische Funktionen (keys(), items()) aufgerufen werden?     
        # Check if pp is a dictionary type object        
        if isinstance(pp, Mapping):
            p_values = list(pp.values())
            # Check if parameter values are valid 
            self._validate_p_values(p_values)          
            # Take Keys in the dict as parameter symbols
            self.pp_symb = list(pp.keys())
            assert isinstance(self.pp_symb, sp.Symbol), \
                                "param pp: keys aren't of type sp.Symbol"
            self.pp_dict = pp
        else:  # pp is a vector of parameter values
            # Check if parameters are valid     
            self._validate_p_values(pp)
            # Define symbolic parameter vector
            self.pp_symb = pp_symb
            parameter_number = len(pp_symb)
            self.pp_dict = {self.pp_symb[i]:pp[i] for i 
                            in range(parameter_number)}


    # ----------- SYMBOLIC RHS FUNCTION ---------- # 
    # --------------- MODEL DEPENDENT  
    
    @abc.abstractmethod    
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """        


    # ----------- VALIDATE PARAMETER VALUES ---------- #
    
    @abc.abstractmethod
    def validate_p_values(self, p_value_list):
        """ throws exception if values in list aren't valid """
        
    # ----------- NUMERIC RHS FUNCTION ---------- # 
    # -------------- MODEL INDEPENDENT - no adjustion needed
     
    def get_rhs_func(self):
        """
        :return:(function) rhs function for numerical solver
        """
        # transform symbolic function to numerical function
        dxx_dt_func = sp.Matrix(self.get_rhs_symbolic())
        # Substitute Parameters with numerical Values
        dxx_dt_func = dxx_dt_func.subs(self.pp_subs_list)
        # dxx_dt_func = st.expr_to_func(self._xxuu_symb, list(dxx_dt_func), 
        #                               modules = 'numpy')
        dxx_dt_func = sp.lambdify(self._xxuu_symb, list(dxx_dt_func), 
                                    modules = 'numpy')        
        # create rhs function
        def rhs(t, xx_nv):
            """
            :param t:(scalar) Time
            :param xx_nv:(self.n-dim vector) numerical state vector
            :return:(self.n-dim vector) first time derivative of state vector
            """
            uu_nv = self.uu_func(t, xx_nv)
           
            # convert uu_nv to list
# ??? könnte auch einfach davon ausgehen, dass uu_func() eine Liste mit u_werten zurück gibt            
            try:
                uu_nv = list(uu_nv)
            except TypeError:       
            # uu_nv is not iteratable --> assume its scalar 
            # and converts it to 1-element-list
                uu_nv = [float(uu_nv)]
            # uu_nv = list(uu_nv)  
            # combine numerical state and input vector
            xxuu_nv = list(xx_nv) + uu_nv
            ### xxuu_nv = list(xx_nv) + list(uu_nv)           
            # evaluate function
            dxx_dt_nv = dxx_dt_func(*xxuu_nv)

            return dxx_dt_nv
            
        return rhs
    
    
    # ----------- CREATE SYMBOLIC INPUT VECTOR ---------- #
    
    def _create_symb_uu(self, u_dim):
        self.uu_symb = [sp.Symbol('u'+ str(i)) for i in range(0, self.u_dim)]

    
    # ----------- CREATE SYMBOLIC STATE AND COMBINED VECTOR ---------- #
    
    def _create_symb_xx_xxuu(self):
        # create new symbolic state vector
        self.xx_symb = [sp.Symbol('x'+ str(i)) for i in range(0, self.n)]
        self._xxuu_symb = self.xx_symb + self.uu_symb   
        
        
    # ----------- CREATE SYMBOLIC PARAMETER VECTOR ---------- #
    
    def _create_symb_pp(self):
        self.pp_symb = list(self.pp_dict.keys())
    
    
    # ----------- CREATE PARAMETER SUBSTITUTION LIST ---------- #
    
    def _create_subs_list(self):
        self.pp_subs_list = list(self.pp_dict.items())