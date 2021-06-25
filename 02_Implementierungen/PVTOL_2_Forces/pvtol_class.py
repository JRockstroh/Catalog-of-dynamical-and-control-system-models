# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GenericModel import GenericModel

try:
    # MODEL DEPENDENT, only adjust import file name
    import pvtol_parameters as params  
except ModuleNotFoundError:
    print("Didn't found default Parameter File. \
          Assuming that the System doesn't have parameters.")

class Model(GenericModel): 
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
        # Initialize all Parameters of the Model-Object with None
#??? zur besseren lesbarkeit die Variablen Initialisierung drin lassen?        
        super().__init__()
        
        # Define number of inputs -- MODEL DEPENDENT
        self.u_dim = 2
        # Set fix system dimension if necessary
        x_dim = 6
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


    # ----------- SET_PARAMETERS ---------- #
    # ------------- MODEL DEPENDENT, if Parameter Number = f(x_dim)
 
    def set_parameters(self, pp, x_dim=None):
        """
        :param pp:(vector or dict-type with floats>0) parameter values
        """
# ??? Können Parameter bei bestehendem Modell/System verändert werden?        
        # Case: Parameters already got set
        if self.pp_dict is not None:
            return
                
        # Case: Use Defautl Parameters
        if pp is None and x_dim is None:
            try:
                self.pp_dict = params.get_default_parameters()
            except NameError:
                self.pp_dict = {}
                
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
        m = self.pp_dict[self.pp_symb[2]]
        T_raise = 2
        T_left = T_raise + 2 + 2
        T_right = T_left + 4
        T_straight = T_right + 2
        T_land = T_straight + 3
        force = 0.75*9.81*m
        force_lr = 0.7*9.81*m
        g_nv = 0.5*self.pp_dict[self.pp_symb[0]]*m
        # create symbolic polnomial functions for raise and land
        poly1 = st.condition_poly(self.t_symb, (0, 0, 0, 0), 
                                  (T_raise, force, 0, 0))
        
        poly_land = st.condition_poly(self.t_symb, (T_straight, g_nv, 0, 0), 
                                      (T_land, 0, 0, 0))
        
        # create symbolic piecewise defined symbolic transition functions
        transition_u1 = st.piece_wise((0, self.t_symb < 0), 
                                      (poly1, self.t_symb < T_raise), 
                                      (force, self.t_symb < T_raise + 2), 
                                      (g_nv, self.t_symb < T_left),
                                      (force_lr, self.t_symb < T_right),
                                      (g_nv, self.t_symb < T_straight),
                                      (poly_land, self.t_symb < T_land),
                                      (0, True))
        
        transition_u2 = st.piece_wise((0, self.t_symb < 0), 
                                      (poly1, self.t_symb < T_raise), 
                                      (force, self.t_symb < T_raise + 2), 
                                      (force_lr, self.t_symb < T_left),
                                      (g_nv, self.t_symb < T_right),
                                      (force_lr, self.t_symb < T_straight),
                                      (poly_land, self.t_symb < T_land),
                                      (0, True))
        
        # transform symbolic to numeric function 
        transition_u1_func = st.expr_to_func(self.t_symb, transition_u1)
        transition_u2_func = st.expr_to_func(self.t_symb, transition_u2)
        
        def uu_rhs(t, xx_nv):
            u1 = transition_u1_func(t)
            u2 = transition_u2_func(t)
                      
            return [u1, u2]
        
        return uu_rhs

         
    # ----------- SYMBOLIC RHS FUNCTION ---------- # 
    # --------------- MODEL DEPENDENT  
    
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """
        if self.dxx_dt_symb is not None:
            return self.dxx_dt_symb
        x1, x2, x3, x4, x5, x6 = self.xx_symb
        g, l, m, J = self.pp_symb      
        u1, u2 = self.uu_symb
        # create symbolic rhs functions
        dx1_dt = x2
        dx2_dt = -sp.sin(x5)/m * (u1 + u2)
        dx3_dt = x4
        dx4_dt = sp.cos(x5)/m * (u1 + u2) - g
        dx5_dt = x6 *2*sp.pi/360
        dx6_dt = l/J * (u2 - u1) *2*sp.pi/360
        
        # put rhs functions into a vector
        self.dxx_dt_symb = [dx1_dt, dx2_dt, dx3_dt, dx4_dt, dx5_dt, dx6_dt]
        
        return self.dxx_dt_symb
    