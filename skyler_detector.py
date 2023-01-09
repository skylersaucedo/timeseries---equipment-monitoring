
import pandas as pd
import numpy as np

import adtk
from adtk.data import validate_series
from adtk.detector import AutoregressionAD
from adtk.visualization import plot
from adtk.detector import QuantileAD


def skyler_custom_detector(df):
    
    df = validate_series(df)
    
    # ----------- cyclical_data

    cyclical_data = df[['system power', 'pump flow']]

    n_steps = 75 # include half cycle of pump
    step_size = 158 # approximate cycle of pump

    autoregression_ad_cyclical = AutoregressionAD(n_steps=n_steps, step_size=step_size, c=3.0)
    anomalies_cyc = autoregression_ad_cyclical.fit_detect(cyclical_data)
    
    # ----------- pressure_data

    pressure_data = df[['lube tank pressure', 'lube gearbox pressure']]
    autoregression_ad_press = AutoregressionAD(n_steps=n_steps, step_size=step_size, c=3.0)
    anomalies_press = autoregression_ad_press.fit_detect(pressure_data)

    # ----------- temp_data

    temp_data = df[['lube gearbox temperature']]

    quantile_ad_temp = QuantileAD(high=0.981, low=0.01) # slightly lowered sensitivity
    anomalies_temp = quantile_ad_temp.fit_detect(temp_data)
    
    # --------- combine anoms, these are equally weighted for now...
    
    power_anoms = [1 if x == True else 0 for x in anomalies_cyc['system power'].values]
    flow_anoms = [1 if x == True else 0 for x in anomalies_cyc['pump flow'].values]
    tank_anoms = [1 if x == True else 0 for x in anomalies_press['lube tank pressure'].values]
    gear_anoms = [1 if x == True else 0 for x in anomalies_press['lube gearbox pressure'].values]
    temp_anoms = [1 if x == True else 0 for x in anomalies_temp['lube gearbox temperature'].values]
    
    outlist = []

    for i in range(len(power_anoms)):
        outlist.append([power_anoms[i], flow_anoms[i], tank_anoms[i], gear_anoms[i], temp_anoms[i]])
        
    df_p = pd.DataFrame(outlist, columns = ['power', 'flow', 'tank', 'gear', 'temp'])
    df_p['score'] = df_p.sum(axis=1)
    
    # ---------- add score to final dataframe
        
    df['score'] = df_p['score'].values
    
    return df