# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:33:34 2021

@author: Jonathan Rockstroh
"""

import sympy as sp
import symbtools as st
from sympy import I
import numpy as np
import importlib

from GenericModel import GenericModel

# Import parameter_file
# Name of the parameter file without ending -- MODEL DEPENDENT
parameter_file_name = 'MMC_parameters'

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
        # check existance of params file -> if not: System is defined to hasn't 
        # parameters
        self.has_params = True
        try:
            params.get_default_parameters()
        except NameError:
            self.has_params = False
        # Define number of inputs -- MODEL DEPENDENT
        self.u_dim = 4
        # Set fix system dimension if necessary
        x_dim = 8
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
        if pp is None:
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

        vdc, vg, omega, Lz, Mz, R, L = list(self.pp_dict.values())
        Ind_sum = Mz + Lz
        def uu_rhs(t, xx_nv):
            	
            es0, ed0, es, ed, iss, iss0, i, theta = xx_nv
                   
            # Define Input Functions
            Kp = 5
            # define reference trajectory for i
            T_dur = 1.5
            tau = t/T_dur
            i_max = 10
        
            i_ref = 10
            dt_i_ref = 0            
            
            if tau < 1:
                i_ref = 4 + (i_max - 4) *np.sin(0.5*tau *np.pi) *np.sin(0.5*tau *np.pi)
                dt_i_ref = np.pi/T_dur * np.sin(0.5*tau *np.pi) *np.cos(0.5*tau *np.pi)
            if t < 1:
                i_ref = 4
                dt_i_ref = 0  
            
            vy = vg + (R+1j*omega*L) *i + 1*(i_ref - i) + L *dt_i_ref
            vy = complex(vy)
            
            vy0 = -1/6 *np.absolute(vy) *np.real(
                    np.exp(3 *1j*(theta + np.angle(vy))) )
            
            vx = 1j *omega*Ind_sum*iss - Kp*iss # p- controller to get iss
            
                # define reference trajectory of es0
            T_dur = 0.5 #duration of es0 ref_traj
            tau = t/T_dur
            #es0_max = 68
            #es0_ref = sp.Piecewise((0, tau < 0), (es0_max *sp.sin( tau*sp.pi/2)  \
            #                        *sp.sin( tau*sp.pi/2), tau < 1), (es0_max, True) )
            es0_ref = 56
                # derive iss0 ref trajectory
            iss0_ref = 1/vdc *np.real(i *np.conjugate(vy)) + Kp *(es0_ref - es0)
            
            # p-controller for vx0
            vx0 = Kp*(iss0_ref - iss0)       
            return [vy, vy0, vx, vx0]
        
        return uu_rhs

         
    # ----------- SYMBOLIC RHS FUNCTION ---------- # 
    # --------------- MODEL DEPENDENT  
    
    def get_rhs_symbolic(self):
        """
        :return:(scalar or array) symbolic rhs-functions
        """
        if self.dxx_dt_symb is not None:
            return self.dxx_dt_symb
        
        es0, ed0, es, ed, iss, iss0, i, theta = self.xx_symb
        vdc, vg, omega, Lz, Mz, R, L = self.pp_symb 
        # u0 = input force     
        vy0, vy, vx0, vx = self.uu_symb
        
        # Auxiliary variables
        Ind_sum = Lz + Mz
        vydelta = vy - Mz *(I *omega*i + 1/L *(vy - (R + I *omega*L) *i - vg))
        
        # create symbolic rhs functions
        des0_dt = vdc*iss0 - sp.re(i*sp.conjugate(vy) )
        
        ded0_dt = -2 *vy0*iss0 - sp.re(sp.conjugate(iss)*vydelta )
        
        des_dt = vdc*iss - sp.exp(- 3*I*theta) *sp.conjugate(vy) \
                *sp.conjugate(i) - 2 *i*vy0 - I *omega*es
                
        ded_dt = vdc*i - sp.exp(- 3*I*theta) *sp.conjugate(iss) \
                *sp.conjugate(vydelta) - 2*iss*vy0 \
                - 2*iss0*vydelta - I *omega*ed
                
        diss_dt = 1/Ind_sum * (vx -  I*omega*Ind_sum*iss)
        
        diss0_dt = vx0/Ind_sum
        
        di_dt = 1/L * (vy - (R + I *omega*L) *i - vg) 
        
        dtheta_dt = 2*sp.pi/360*omega
        
        # put rhs functions into a vector
        self.dxx_dt_symb = [des0_dt, ded0_dt, des_dt, ded_dt, diss_dt, 
                            diss0_dt, di_dt, dtheta_dt]
        
        return self.dxx_dt_symb
    
    # ----------- NUMERIC RHS FUNCTION ---------- # 
    # -------------- written sepeeratly cause it seems like that lambdify can't
    # -------------- handle complex values in a proper way
     
    def get_rhs_func(self):
        """
        Creates an executable function of the model which uses:
            - the current parameter values
            - the current input function
        
        To evaluate the effect of a changed parameter set a new rhs_func needs 
        to be created with this method.
        
        :return:(function) rhs function for numerical solver like 
                            scipy.solve_ivp
        """
     
        # create rhs function
        def rhs(t, xx_nv):
            """
            :param t:(tuple or list) Time
            :param xx_nv:(self.n-dim vector) numerical state vector
            :return:(self.n-dim vector) first time derivative of state vector
            """
            uu_nv = self.uu_func(t, xx_nv)
            vy, vy0, vx, vx0 = uu_nv
            es0, ed0, es, ed, iss, iss0, i, theta = xx_nv
            vdc, vg, omega, Lz, Mz, R, L = list(self.pp_dict.values())
            Ind_sum = Mz + Lz 
            # = vy-Mz(j*omega*i-dt_i)
            vydelta = vy - Mz *(1j *omega*i + 1/L 
                                *(vy - (R + 1j *omega*L) *i - vg) )
            
            dt_es0 = vdc*iss0 - np.real(i*np.conjugate( vy) )
            dt_ed0 = -2 *vy0*iss0 - np.real(np.conjugate( iss)*vydelta )
            
            dt_es = vdc*iss - np.exp( -3*1j*theta) *np.conjugate( vy) \
                    *np.conjugate( i) - 2 *i*vy0 - 1j *omega*es
                    
            dt_ed = vdc*i - np.exp( -3*1j*theta) *np.conjugate( iss) \
                    *np.conjugate( vydelta)- 2 *iss*vy0 - 2 *iss0*vydelta \
                    - 1j *omega*ed        
                    
            dt_iss = 1/Ind_sum * (vx -  1j*omega*Ind_sum*iss)
            dt_iss0 = vx0/Ind_sum      
            dt_i = 1/L * (vy - (R+1j *omega*L) *i - vg)
            dt_theta = omega
            
            dxx_dt_nv = [dt_es0, dt_ed0, dt_es, dt_ed, dt_iss, 
                         dt_iss0, dt_i, dt_theta
                         ]

            return dxx_dt_nv
            
        return rhs