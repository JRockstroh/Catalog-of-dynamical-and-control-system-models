# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
import importlib
from itertools import combinations as comb
import numpy as np

from GenericModel import GenericModel

# Import parameter file
# Name of the parameter file without ending -- MODEL DEPENDENT
parameter_file_name = 'stable_pt_2_parameters'

# try to find ModuleSpecs
param_module = importlib.util.find_spec(parameter_file_name)

# if ModuleSpecs are found, paramters_package can be loaded
if param_module is not None:
    params = importlib.import_module(parameter_file_name) 
    
class Model(GenericModel): 
    ## NOTE:
        # x_dim usw vllt als keywordargs definieren - Vermeidung von effektlosen, optionelen parametern  
    has_params = True    
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
        self.u_dim = 1
        # Set fix system dimension if necessary
        x_dim_for_set_pp = x_dim
        if x_dim is None:
            x_dim = 2
        # Set self.n
        self._set_dimension(x_dim)        
        # Create symbolic input vector
        self._create_symb_uu(self.u_dim)
        # Create symbolic xx and xxuu
        self._create_symb_xx_xxuu()
        # Create parameter dict, subs_list and symbolic parameter vector
        self.set_parameters(pp, x_dim=x_dim_for_set_pp)
        # Create Symbolic parameter vector and subs list
        self._create_symb_pp()
        # Validate parameter values
        #print("PP_DICT_DICT?: ", isinstance(self.pp_dict, dict))
        self._validate_p_values(list(self.pp_dict.values()))
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
            pp_symb = [sp.Symbol('T'+ str(i)) for i in range(0, x_dim)]
            pp_symb = [sp.Symbol('K')] + pp_symb
            self._create_individual_p_dict(pp, pp_symb=pp_symb)
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
        try: [float(i) for i in p_value_list]
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
            u = 10
            c = t > 0
            try: 
                uu = list(c*u)
            except TypeError:
                uu = [c*u]
            uu = [np.sin(0.387298334621*t)]
            return uu
        
        return uu_rhs

         
    # ----------- SYMBOLIC RHS FUNCTION ---------- # 
    # --------------- MODEL DEPENDENT  
    
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """
        if self.dxx_dt_symb is not None:
            return self.dxx_dt_symb
        xx_symb = self.xx_symb  
        u_symb= self.uu_symb[0]
        K_symb = self.pp_symb[0]
        TT_symb = self.pp_symb[1:]
        # create symbolic rhs functions
        # define entry/derivation 1 to n-1
        dxx_dt = [entry for entry in xx_symb]
        dxx_dt = dxx_dt[1:]
        # define entry/derivation n
        sum_vec = []
        # write all summands of the expanded inverse laplace into a vector
        for k in range(self.n + 1):
            next_elem = self._create_factor(TT_symb, k)        
            sum_vec = sum_vec + [next_elem]
        # calculate expanded inverse laplace
        
        inv_laplace = 0
        for i in range(len(sum_vec) - 1):
            inv_laplace = inv_laplace + sum_vec[i]*xx_symb[i]
        
        
        dxn_dt = (K_symb*u_symb - inv_laplace) * 1/sum_vec[-1]
        dxx_dt = dxx_dt + [dxn_dt]
        # put rhs functions into a vector
        self.dxx_dt_symb = dxx_dt
        
        return self.dxx_dt_symb
    
    def _create_factor(self, pp_symb, deriv_nr):
        '''Auxiliary Function to create the symb function of the pt_n element
        returns the factor infront of the state, which represents the 
        deriv_nr-th derivation of y. Take a look at product in the equation 
        for dx_n_dt in the model documentation.
        
        :param pp_symb: list of sympy variables
            symbolic parameter vectorm, which only contains the time coefficients
        :param deriv_nr: int >= 0
            number of the state of the dxn_dt solution for which the leading factor
            shall be calculated
            
        :return summand: sympy function
            returns the summand of
    
        '''
        # assure, that deriv_nr is a proper value
        assert deriv_nr >= 0, "deriv_nr needs to be positive or zero"
    
        assert deriv_nr <= len(pp_symb), "deriv_nr can't be greater than the \
                                            length of the pp_symb list"
        # initialize summand
        factor = 0
        # Solve Special case of deriv_nr = 0
        if deriv_nr == 0:
            factor = 1
        # create factor for deriv_nr > 0
        else:
            # create list of all deriv_nr-element combinations 
            subsummand_vec = list(comb(pp_symb, deriv_nr))
            # save length of the sublists, to improve performance
            sublist_len = len(subsummand_vec[0])
            # iterate over the combinations and create summand = sum of subsummands
            for i in range(len(subsummand_vec)):
                subsummand = 1
                # create one summand of the factor
                for j in range(sublist_len):
                    subsummand = subsummand * subsummand_vec[i][j]
                # add subsummand to factor    
                factor = factor + subsummand
                
        return factor