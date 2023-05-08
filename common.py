# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:59:24 2023

@author: ayesh
"""
import pandas as pd
import numpy as np


def generate_quantiles(df):
    # Divide the total deaths per state column into 3 quantiles and assign values 0, 1, 2
    mortality_condition_quantiles = np.quantile(df['Crude_Death_Rate_Conditions_Overall'], [0.33, 0.66])
    df['Death_Condition_Val'] = pd.cut(df['Crude_Death_Rate_Conditions_Overall'], bins=[-np.inf, mortality_condition_quantiles[0], mortality_condition_quantiles[1], np.inf], labels=[0, 1, 2]).astype(int)

    # Multiply death by conditions with 10
    df['Death_Condition_Val'] =df['Death_Condition_Val'] * 10

    # Divide the diabetes risk column into 3 quantiles and assign values 0, 1, 2
    obesity_quantiles = np.quantile(df['ObesityPercent'], [0.33, 0.66])
    df['Obesity_Val'] = pd.cut(df['ObesityPercent'], bins=[-np.inf, obesity_quantiles[0], obesity_quantiles[1], np.inf], labels=[0, 1, 2]).astype(int)

    # Compute the color_val column as the sum of the heart and diabetes variables
    df['Color_Val'] = df['Death_Condition_Val'] + df['Obesity_Val']
