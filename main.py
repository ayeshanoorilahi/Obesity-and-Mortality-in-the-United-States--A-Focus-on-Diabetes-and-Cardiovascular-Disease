# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:16:29 2023

@author: ayesh
"""

import pandas as pd
import common as com
import mortality as mt
import obesity as obs
import chart as ch

input_path = 'Data/Input'
output_path = 'Data/Output'

# get mortality data after clean up and merge
mortality_data = mt.process_mortality_data(input_path)

# get obesity data from bfrss source by calculating percentages for each state
obesity_percent = obs.calculate_obesity_percentage(input_path)

# merge mortality and obesity data
final_data = pd.merge(mortality_data, obesity_percent, how="left", on=["State Code"])

# generate quantiles to assist with color ramps
com.generate_quantiles(final_data)

# save to csv
final_data.to_csv(f'{output_path}/MortalityData.csv', sep='|')


# draw scatter plot between obesity and mortality by the circulatory and diabetes conditions
ch.scatter_plot(output_path, final_data)

# draw regression plot between obesity and mortality by the circulatory and diabetes conditions
ch.reg_plot(output_path, final_data)





































