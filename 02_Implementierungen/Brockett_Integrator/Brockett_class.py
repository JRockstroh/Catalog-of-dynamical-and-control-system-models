# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
import importlib

from GenericModel import GenericModel

# Import parameter file
# Name of the parameter file without ending -- MODEL DEPENDENT
parameter_file_name = ''

# try to find ModuleSpecs
param_module = importlib.util.find_spec(parameter_file_name)

# if ModuleSpecs are found, paramters_package can be loaded
if param_module is not None:
    params = importlib.import_module(parameter_file_name)

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
        super().__init__()
        
        # Define number of inputs -- MODEL DEPENDENT
        self.u_dim = 2
        # Set fix system dimension if necessary
        x_dim = 3
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
        :param x_dim:(positive int)
        """
        # Case: System doesn't have parameters
        if not self.has_params:
            return     
         
        # Case: Use Default Parameters
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
        
    # - BEGIN: MODEL DEPENDENT PART -
        # Case: parameter number = f(x_dim) , x_dim != default dim
        # --> define symbolic parameters for n extendible System
        # and use individual parameter values in pp
        if pp is not None and x_dim is not None:
            # Create symbolic parameters - skip, if pp is dict/mapping
            pp_symb = None
            self._create_individual_p_dict(pp, pp_symb)
            return
    # - END: MODEL DEPENDENT PART -
        
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
        def uu_rhs(t, xx_nv):
            u1 = 0
            u2 = 0
            if t > 0:
                u1 = 4-t#4-xx[0]
                u2 = (t-5)#2-xx[1]  
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
        x1, x2, x3 = self.xx_symb
        # u0 = input force     
        u1, u2 = self.uu_symb
        # create symbolic rhs functions
        dx1_dt = u1
        dx2_dt = u2
        dx3_dt = x2*u1 - x1*u2 
        
        # put rhs functions into a vector
        self.dxx_dt_symb = [dx1_dt, dx2_dt, dx3_dt]
        
        return self.dxx_dt_symb
    