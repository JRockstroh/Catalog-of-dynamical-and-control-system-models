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

model_name = "DC_DC_Buck_Converter"

# --------- CREATE SYMBOLIC PARAMETERS
pp_symb = [R, L, C, U_DC, r_son, r_L, r_c] = \
                sp.symbols('R, L, C, U_DC, r_son, r_L, r_c', real = True)

# -------- CREATE AUXILIARY SYMBOLIC PARAMETERS 
# (parameters, which shall not numerical represented in the parameter tabular)


# --------- SYMBOLIC PARAMETER FUNCTIONS
# ------------ parameter values can be constant/fixed values OR 
# ------------ set in relation to other parameters (for example: a = 2*b)
# ------------ useful for a clean looking parameter table in the Documentation     
R_sf = 2.345
L_sf = 47 * 10**-6
C_sf = 68 * 10**-6
U_DC_sf = 3.75
r_son_sf = 2.1
r_L_sf = 0.13
r_c_sf = 55 * 10**-3
# List of symbolic parameter functions
pp_sf = [R_sf, L_sf, C_sf, U_DC_sf, r_son_sf, r_L_sf, r_c_sf]

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

col_1 = ["Load Resistance", 
         "Inductivity",
         "Capacity",
         "Input Voltage",
         "switching resistance",
         "Inductor Resistance",
         "Capacitor Resistance"
         ] 
# contains all lists of the columns before the "Symbol" Column
# --- Empty list, if there are no columns before the "Symbol" Column
start_columns_list = [col_1]

# Define Entries of the columns after the Value-Column
# --- Entries need to be latex code
col_4 = [r"$\Omega$", 
         r"H",
         r"F",
         "V",
         r"$\Omega$",
         r"$\Omega$",
         r"$\Omega$"
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
    return pp_dict


# ----------- GET SYMBOLIC PARAMETERS ---------- # 

def get_symbolic_parameters():
    """
    :return:(list) with symbolic parameters
    """
    return pp_symb


if __name__ == "__main__":
    main()