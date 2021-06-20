# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
from collections.abc import Mapping
import warnings

import Model_Superclass
import model_parameters as params  # MODEL DEPENDENT, only adjust import file

class Model(Model_Superclass): 
    t_symb = sp.Symbol('t_symb')
    ## NOTE:
        # x_dim usw vllt als keywordargs definieren - Vermeidung von effektlosen, optionelen parametern
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
        # Initialize all Parameters of the Model-Object    
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
        
        # Define number of inputs -- MODEL DEPENDENT
        self.u_dim = 1
        # Set fix system dimension if necessary
        x_dim = 2
        # Set self.n
        self._set_dimension(x_dim)        
        # Create symbolic input vector
        self._create_symb_uu(self.u_dim)
        # Create symbolic xx and xxuu
        self._create_symb_xx_xxuu()
        # Create parameter dict, subs_list and symbolic parameter vector
        self.set_parameters(pp)
        # Create Symbolic parameter vector and subs list
        self._create_symb_pp()
        # Create Substitution list
        self._create_subs_list()
        # choose input function
        self.set_input_func(self.uu_default_func())
        if u_func is not None:
            self.set_input_func(u_func)


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
    
    # ----------- SET_PARAMETERS ---------- #
    # ------------- MODEL DEPENDENT, if Parameter Number = f(x_dim)
 
    def set_parameters(self, pp, x_dim=None):
        """
        :param pp:(vector or dict-type with floats>0) parameter values
        """        
        # Case: Use Defautl Parameters
        if pp is None and x_dim is None:
            self.pp_dict = params.get_default_parameters()
            return
        
        # Case: Use individual parameters, but parameter number + symbols 
        # are equal to the Default Parameters
        if pp is not None and x_dim is None:
            parameter_number = len(params.get_default_parameters())
            assert len(pp) == parameter_number, \
                        ":param pp: hasn't length of " + str(parameter_number)
            pp_symb = params.get_symbolic_parameters()            
            self._create_individual_p_dict(pp, pp_symb)
            return
        
        # Case: parameter number = f(x_dim) , x_dim != default dim
        # --> define symbolic parameters for n extendible System
        # and use individual parameter values in pp
        if pp is not None and x_dim is not None:
            # Create symbolic parameters - skip, if pp is dict/mapping
            pp_symb = None
            self._create_individual_p_dict(pp, pp_symb)
            return
        
        # Case: individual x_dim but no individual parameters given 
        raise Exception("Individual Dimension given, but no individual \
                        parameter vector pp given.")
          

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


    # ----------- VALIDATE PARAMETER VALUES ---------- #
    # -------------- MODEL DEPENDENT 
    
    def _validate_p_values(self, p_value_list):
        """ raises exception if values in list aren't valid 
        :param p_value_list:(float) list of parameter values
        """
        # Check for convertability to float
        try: float(p_value_list)
        except ValueError:
                raise Exception(":param pp: Values are not valid. \
                                (aren't convertible to float)")
                                 
        # Check if values are in required range --- MODEL DEPENDENT                         
        assert not any(flag <= 0 for flag in p_value_list), \
                        ":param pp: does have values <= 0"
                                
   
    # ----------- SET NEW INPUT FUNCTION ---------- # 
    # --------------- Only for non-autonomous Systems
    # --------------- Validation is MODEL DEPENDENT
    
    def set_input_func(self, u_func):
        """
        :u_func:(object, callable), individual input function
        """
        # Check if u_func is valid - MODEL DEPENDENT         
        # check if u_func is a callable object 
        assert callable(u_func), ":param u_func: isn't a callable object." 
        # assign given function to object variable        
        self.uu_func = u_func


    # ----------- SET DEFAULT INPUT FUNCTION ---------- # 
    # --------------- Only for non-autonomous Systems
    # --------------- MODEL DEPENDENT
    
    def uu_default_func(self):
        """
        :param t:(scalar or vector) Time
        :param xx_nv: (vector or array of vectors) state vector with 
                                                    numerical values at time t      
        :return:(function with 2 args - t, xx_nv) default input function 
        """ 
        a, omega = self.pp_symb[2], self.pp_symb[3]
        u_sp = self.pp_dict[a]*sp.sin(self.pp_dict[omega]*self.t_symb-sp.pi/2)
        du_dtt_sp = u_sp.diff(self.t_symb, 2)
        du_dtt_sp = du_dtt_sp.subs(self.pp_subs_list)
        du_dtt_func = st.expr_to_func(self.t_symb , du_dtt_sp)
        
        def uu_rhs(t, xx_nv):
            du_dtt_nv = du_dtt_func(t)
            return [du_dtt_nv]
        
        return uu_rhs


    # ----------- SET STATE VECTOR DIMENSION ---------- # 
    # --------------- MODEL DEPENDENT
    # --------------- For Systems with fix x_dim its only works on first use
    # --------------- Keep in mind that you also may need to correct the parameters, if you change the dimension
    
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

         
    # ----------- SYMBOLIC RHS FUNCTION ---------- # 
    # --------------- MODEL DEPENDENT  
    
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """
        if self.dxx_dt_symb is not None:
            return self.dxx_dt_symb
        x1, x2 = self.xx_symb
        l, g, a, omega, gamma = self.pp_symb 
        # u0 = input force     
        u0 = self.uu_symb[0]
        # create symbolic rhs functions
        dx1_dt = x2
        dx2_dt = -2*gamma*x2 - (g/l + 1/l * u0) *sp.sin(x1)
        
        # put rhs functions into a vector
        self.dxx_dt_symb = [dx1_dt, dx2_dt]
        
        return self.dxx_dt_symb
    
    
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
        dxx_dt_func = st.expr_to_func(self._xxuu_symb, list(dxx_dt_func), 
                                      modules = 'numpy')
        # dxx_dt_func = sp.lambdify(self._xxuu_symb, list(dxx_dt_func), 
        #                           modules = 'numpy')        
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
              
            # combine numerical state and input vector
            xxuu_nv = list(xx_nv) + uu_nv   
            ### xxuu_nv = list(xx_nv) + list(uu_nv)           
            # evaluate function
            dxx_dt_nv = dxx_dt_func(*xxuu_nv)

            return dxx_dt_nv
            
        return rhs
    
    