# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:20:39 2023

@author: roywaswa

@description: This is a module file about all the matrix functions involved 
in the transformation 
"""

import numpy as np
import pandas as pd

def create_numpy_array(control_df:pd.DataFrame):
    utm_northings = control_df.iloc[:,3]
    utm_eastings = control_df.iloc[:,4]
    i_matrix = pd.concat([utm_eastings, utm_northings], ignore_index=True)
    i_matrix.to_numpy()

    cassini_df = control_df.iloc[:,1:3]
    print(control_df)
    cass_simple = cassini_df[['conformal_easting','cass_northings']]
    cass_simple.columns = ['x','y']
    cass_simple['xx'] = cass_simple['x']**2
    cass_simple['xy'] = cass_simple['x']*cass_simple['y']
    cass_simple['yy'] = cass_simple['y']**2
    cass_simple.to_numpy()

    zeros = np.zeros((7,5))
    cass_simple1 = np.vstack((cass_simple,zeros))

    zeros = np.zeros((7,5))
    cass_simple2 = np.vstack((zeros,cass_simple))

    cass_simple3 = np.hstack((cass_simple1,cass_simple2))

    ones = np.ones((7,1))

    zeros = np.zeros((7,1))
    ones_zeros = np.hstack((ones,zeros))
    zeros_ones = np.hstack((zeros,ones))
    # vertical stack the ones_zeros and zeros_ones arrays
    one_zero = np.vstack((ones_zeros,zeros_ones))

    a_matrix = np.hstack((cass_simple3,one_zero))

    # return a_matrix and i_matrix
    return a_matrix, i_matrix

def calculate_parameters(a_matrix, i_matrix):
    a_matrix_transpose = a_matrix.transpose()
    a_matrix_transpose_a_matrix = np.matmul(a_matrix_transpose,a_matrix)
    a_matrix_transpose_i_matrix = np.matmul(a_matrix_transpose,i_matrix)
    a_t_a_inv = np.linalg.inv(a_matrix_transpose_a_matrix)
    sol_parameters = np.matmul(a_t_a_inv,a_matrix_transpose_i_matrix)
    sol_parameters_dict = {
    'a1':sol_parameters[0],
    'a2':sol_parameters[1],
    'a3':sol_parameters[2],
    'a4':sol_parameters[3],
    'a5':sol_parameters[4],
    'b1':sol_parameters[5],
    'b2':sol_parameters[6],
    'b3':sol_parameters[7],
    'b4':sol_parameters[8],
    'b5':sol_parameters[9],
    'a0':sol_parameters[10],
    'b0':sol_parameters[11]
    }
    return sol_parameters_dict