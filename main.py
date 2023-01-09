
import os
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import numpy as np
import pandas as pd
import adtk
from adtk.data import validate_series
from adtk.detector import AutoregressionAD
from adtk.visualization import plot
from adtk.detector import QuantileAD

from skyler_detector import skyler_custom_detector

def main():
    """
    Use this routine to demonstrate detector solution
    """
    
    csv_path = 'sensor_data.csv'

    # use Arundo's Detector library to validate data. Look for nulls, repeat time stamps.

    df = pd.read_csv(csv_path, index_col="datetime", parse_dates=True)
    df = validate_series(df)

    cyclical_data = df[['system power', 'pump flow']]
    pressure_data = df[['lube tank pressure', 'lube gearbox pressure']]

    n_steps = 75 # include half cycle of pump
    step_size = 158 # approximate cycle of pump in step size length

    # --- power/flow detector --  autoregression on cyclical data yields interesting findings...

    autoregression_ad = AutoregressionAD(n_steps=n_steps, step_size=step_size, c=3.0)
    anomalies = autoregression_ad.fit_detect(cyclical_data)
    plot(cyclical_data, anomaly=anomalies, ts_markersize=1, anomaly_color='red', anomaly_tag="marker", anomaly_markersize=3);

    # everything before green line is nominal, failure occurs at black
    plt.axvline(pd.to_datetime('2019-11-06 13:00:00'), color='g', linestyle='--', lw=2)
    plt.axvline(pd.to_datetime('2019-11-10 16:00:00'), color='black', linestyle='--', lw=2)
    plt.show()

    # --- pressure detector -- confirms anomalous behavior near failure

    autoregression_ad = AutoregressionAD(n_steps=n_steps, step_size=step_size, c=3.0)
    anomalies = autoregression_ad.fit_detect(pressure_data)
    plot(pressure_data, anomaly=anomalies, ts_markersize=1, anomaly_color='red', anomaly_tag="marker", anomaly_markersize=3);

    # everything before green line is nominal, failure occurs at black
    plt.axvline(pd.to_datetime('2019-11-06 13:00:00'), color='g', linestyle='--', lw=2)
    plt.axvline(pd.to_datetime('2019-11-10 16:00:00'), color='black', linestyle='--', lw=2)
    plt.show()

    # --- show temp detector -----

    temp_data = df[['lube gearbox temperature']]

    quantile_ad = QuantileAD(high=0.981, low=0.01) # slightly lowered sensitivity
    anomalies = quantile_ad.fit_detect(temp_data)

    plot(temp_data, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker");

    # everything before green line is nominal, failure occurs at black
    plt.axvline(pd.to_datetime('2019-11-06 13:00:00'), color='g', linestyle='--', lw=2)
    plt.axvline(pd.to_datetime('2019-11-10 16:00:00'), color='black', linestyle='--', lw=2)
    plt.show()

    # show custom detector

    df = skyler_custom_detector(df)

    df['score'].plot()
    # everything before green line is nominal, failure occurs at black
    plt.axvline(pd.to_datetime('2019-11-06 13:00:00'), color='g', linestyle='--', lw=2)
    plt.axvline(pd.to_datetime('2019-11-10 16:00:00'), color='black', linestyle='--', lw=2)
    plt.show()


if __name__ == '__main__':
    main()