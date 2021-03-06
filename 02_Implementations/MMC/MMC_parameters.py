# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:51:06 2021

@author: Jonathan Rockstroh
"""
import sys
import os
import numpy as np
import sympy as sp

import tabulate as tab


# Trailing "_nv" stands for "numerical value"

#### -- BEGIN: CODE WHICH MUST BE ADJUSTED FOR EACH MODEL -- ####

model_name = "MMC"

# --------- CREATE SYMBOLIC PARAMETERS
pp_symb = [vdc, vg, omega, Lz, Mz, R, L] \
        = sp.symbols('v_DC, v_g, omega, L_z, M_z, R, L', real=True)

# -------- CREATE AUXILIARY SYMBOLIC PARAMETERS 
# (parameters, which shall not numerical represented in the parameter tabular)

# --------- SYMBOLIC PARAMETER FUNCTIONS
# ------------ parameter values can be constant/fixed values OR 
# ------------ set in relation to other parameters (for example: a = 2*b)
# ------------ useful for a clean looking parameter table in the Documentation     
vdc_sf = 300
vg_sf = 235
omega_sf = 2*sp.pi*5
Lz_sf = 1.5
Mz_sf = 0.94
R_sf = 26
L_sf = 3
# List of symbolic parameter functions
pp_sf = [vdc_sf, vg_sf, omega_sf, Lz_sf, Mz_sf, R_sf, L_sf]

# Set numerical values of auxiliary parameters

# List for Substitution 
# -- Entries are tuples like: (independent symbolic parameter, numerical value)
pp_subs_list = []

# OPTONAL: Dictionary which defines how certain variables shall be written
# in the tabular - key: Symbolic Variable, Value: LaTeX Representation/Code
# useful for example for complex variables: {Z: r"\underline{Z}"}
latex_names = {}

# ---------- CREATE BEGIN OF LATEX TABULAR
# Define tabular Header 

# DON'T CHANGE FOLLOWING ENTRIES: "Symbol", "Value"
tabular_header = ["Parameter Name", "Symbol", "Value", "Unit"]

# Define column text alignments
col_alignment = ["left", "center", "left", "center"]

# Define Entries of all columns before the Symbol-Column
# --- Entries need to be latex code

col_1 = ["DC voltage", 
         "grid voltage",
         "angular speed",
         "arm inductance",
         "mutual inductance",
         "load resistance",
         "load inductance"
         ] 
# contains all lists of the columns before the "Symbol" Column
# --- Empty list, if there are no columns before the "Symbol" Column
start_columns_list = [col_1]

# Define Entries of the columns after the Value-Column
# --- Entries need to be latex code
col_4 = ["V", 
         "V",
         "Hz",
         "mH",
         "mH",
         r"$\Omega$",
         "mH"
         ]
# contains all lists of columns after the FIX ENTRIES
# --- Empty list, if there are no columns after the "Value" column
end_columns_list = [col_4]


#### -- END: CODE WHICH MUST BE ADJUSTED FOR EACH MODEL -- ####

# --------- GET NUMERICAL DEFAULT VALUES OF THE PARAMETERS
# Substitute all remaining symbolic parameters
pp_nv = list(sp.Matrix(pp_sf).subs(pp_subs_list))
pp_dict = {pp_symb[i]:pp_nv[i] for i in range(len(pp_symb))}

def main():
    # ------ CREATE RAMAINING PART OF THE LATEX TABULAR AND WRITE IT TO FILE
    # Define "Symbol" column
    pp_dict_key_list = list(pp_dict.keys())
    p_symbols = [sp.latex(pp_dict_key_list[i], symbol_names=latex_names) 
                 for i in range(len(pp_dict))]
    # set cells in math-mode
    for i in range(len(p_symbols)):
        p_symbols[i] = "$" + p_symbols[i] + "$"
    
    # Define "Value" column
    p_values = [sp.latex(p_sf) for p_sf in pp_sf]
    # set cells in math-mode
    for i in range(len(p_values)):
        p_values[i] = "$" + p_values[i] + "$"
    
    # Create list, which contains the content of the table body
    table_body_list = np.array([*start_columns_list, p_symbols, p_values, 
                                *end_columns_list])
    # Convert list of column entries to list of row entries
    table = table_body_list.transpose()
    
    # Create string which contains the latex-code of the tabular
    tex = tab.tabulate(table, tabular_header, tablefmt = 'latex_raw', 
                       colalign = col_alignment)
    
    # Change Directory to the Folder of the Model. 
    cwd = os.path.dirname(os.path.abspath(__file__))
    parent2_cwd = os.path.dirname(os.path.dirname(cwd))
    path_base = os.path.join(parent2_cwd, "01_Models", model_name) 
    os.chdir(path_base)
    # Write tabular to Parameter File.
    file = open("parameters.tex", 'w')
    file.write(tex)
    file.close()


# ----------- GET DEFAULT PARAMETERS ---------- # 

def get_default_parameters():
    """
    :return:(dict) with parameter_symbol:parameter_value pairs
    """
    Lz_sf_loc = Lz_sf/1000
    Mz_sf_loc = Mz_sf/1000
    L_sf_loc = L_sf/1000
    pp_sf = [vdc_sf, vg_sf, omega_sf, Lz_sf_loc, Mz_sf_loc, R_sf, L_sf_loc]
    pp_nv = list(sp.Matrix(pp_sf).subs(pp_subs_list))
    pp_dict = {pp_symb[i]:pp_nv[i] for i in range(len(pp_symb))}
    return pp_dict


# ----------- GET SYMBOLIC PARAMETERS ---------- # 

def get_symbolic_parameters():
    """
    :return:(list) with symbolic parameters
    """
    return pp_symb


if __name__ == "__main__":
    main()