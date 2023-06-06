# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:31:55 2023

@author: roywa
"""
import matrix_func as mf
import cass_to_utm as ctu
import pandas as pd


def cassini_to_utm(cassini_coods:str, control_coods:str, conformal:bool=False):
    cass_coods = pd.read_csv(cassini_coods)
    controls = pd.read_csv(control_coods)
    cassini_controls = controls.iloc[:,1:3]
    if conformal == False:
        cassini_controls['conformal_easting'] = cassini_controls.apply(ctu.convert_to_conformal,axis=1)
        controls['conformal_easting'] = controls.apply(ctu.convert_to_conformal,axis=1)
        cass_coods['conformal_easting'] = cass_coods.apply(ctu.convert_to_conformal,axis=1)
    [a,i] = mf.create_numpy_array(controls)
    tr_params = mf.calculate_parameters(a,i)
    utm_cods_cass = pd.DataFrame({
        'northing':cass_coods.apply(lambda row: ctu.northing_comp(row, tr_params),axis=1),
        'easting':cass_coods.apply(lambda row: ctu.easting_comp(row, tr_params),axis=1),
        })
    stn = cass_coods[["stn"]]
    utm_cods = utm_cods_cass[["northing","easting"]]
    wgs = ctu.convert_to_latlon(utm_cods_cass)
    wgs_final = pd.concat([stn,utm_cods, wgs], axis=1)
    return wgs_final





if __name__ == "__main__":
    finals = cassini_to_utm(
        "C:/Users/roywa/Documents/ATTACHMENT/cass_utm/data/KAGOYA.csv", 
        "C:/Users/roywa/Documents/ATTACHMENT/cass_utm/data/controls.csv")
    finals.to_csv("./data/KAGOYA_trial_wgs.csv", index=False)










