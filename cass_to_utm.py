import pandas as pd
import numpy as np
import utm



# conformal conversion function
# This function converts cassini coordinates to conformal coordinates by changing the easting values
def convert_to_conformal(cassini_df:pd.DataFrame):
    sys_params = pd.read_csv("./data/parameters.csv")
    e = cassini_df['cass_eastings']
    a = float(sys_params.iloc[2,1])
    b = float(sys_params.iloc[3,1])
    conformal_easting = e + ((e**3)/(6*a*b)) + ((e**5)/(24*(a**2)*(b**2)))
    return conformal_easting


def northing_comp(df, params):
    y = df['cass_northings']
    x = df['conformal_easting']
    b0 = params['b0']
    b1 = params['b1']
    b2 = params['b2']
    b3 = params['b3']
    b4 = params['b4']
    b5 = params['b5']

    northing = b0+b1*x+b2*y+b3*x**2+b4*x*y+b5*y**2
    return np.round(northing,4)

def easting_comp(df,params):
    y = df['cass_northings']
    x = df['conformal_easting']
    a0 = params['a0']
    a1 = params['a1']
    a2 = params['a2']
    a3 = params['a3']
    a4 = params['a4']
    a5 = params['a5']

    easting = a0+a1*x+a2*y+a3*x**2+a4*x*y+a5*y**2
    return np.round(easting,4)

def convert_to_latlon(df_utm):
    latlon = pd.DataFrame(utm.to_latlon(df_utm["easting"],df_utm["northing"], 37,"M"))
    latlon = latlon.transpose()
    latlon.columns = ["latitude", "longitude"]
    return latlon



    
    
    


