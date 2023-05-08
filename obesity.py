# -*- coding: utf-8 -*-
"""
Created on Sat May  6 11:19:30 2023

@author: ayesh
"""
import pandas as pd


# cleaning up the bmi data, dropping out the missing bmi data and setting index to "State Code" in filtered.

def cleanup_bmi_data(data):
    filtered = data.dropna(subset="BMI")
    filtered = filtered.set_index("State Code")
    
    return filtered


# function to process the bfrss data
def process_brfss_data(input_path, year, colspecs):
    
    # Using col_conv dictionary to convert columns to be used into string and integers.
    col_conv = {'State Code': str, 'IDate': str, 'BMI': int}    
    
    #reading and cleaning up the data in bmi
    bmi = pd.read_fwf(f"{input_path}/LLCP{year}.ASC_",colspecs, names=['State Code', 'IDate', 'BMI'], converters = col_conv)
    bmi = cleanup_bmi_data(bmi)
    # using groupby to group data on state code   
    groups = bmi.groupby('State Code')
    # applying the 'obesity_percentage' function to each group in the 'bmi' DataFrame.
    result = groups.apply(obesity_percentage)
    #renaming
    result = result.rename('ObesityPercent')
    return result

def calculate_obesity_percentage(input_path):
    # define dictionary for column specs for each year of BRFSS data. 
    # BRFSS data is provided in a fixed length file
    dict_colspecs = {
            2021:[(0, 0+2), (18, 18+8), (1999, 1999+4)], 
            2020:[(0, 0+2), (18, 18+8), (1996, 1996+4)], 
            2019:[(0, 0+2), (18, 18+8), (1997, 1997+4)], 
            2018:[(0, 0+2), (18, 18+8), (1994, 1994+4)]
         }
    # create an empty list
    obesity_data_list = [];
    
    # iterate over dictionary (dict_colspecs) 
    for val in dict_colspecs:
        # call process_brfss_data with dictionary key and value as parameter
        obesity_data = process_brfss_data(input_path, val, dict_colspecs[val])
        # append obesity data to the list
        obesity_data_list.append(obesity_data)
         
    # concat obesity_data_list
    obesity_percent = pd.concat(obesity_data_list)
    # calculate mean of obesity for each state
    obesity_percent = obesity_percent.groupby('State Code').mean()
    
    return obesity_percent


# Calculating the percentage of obesity on the given data frame
def obesity_percentage(df):
    condition = df['BMI'] > 3000
    return sum(condition) / len(df) * 100
