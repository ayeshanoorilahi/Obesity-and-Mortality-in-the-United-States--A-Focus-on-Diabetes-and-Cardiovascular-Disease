# -*- coding: utf-8 -*-
"""
Created on Sat May  6 11:09:38 2023

@author: ayesh
"""
import pandas as pd
#import common as com


# Using the cleanup function for cleaning up the unnecessary data from the data set

def cleanup_mortality_data(data):
    
# Removing the columns that have na...missing data in state code.
    filtered = data.dropna(subset="State Code")
    
# Setting the index of  DataFrame called "filtered" to the "State Code" column
    filtered = filtered.set_index("State Code")
# Dropping the column Notes from filtered
    filtered = filtered.drop('Notes', axis=1)    
    
# converting the columns of deaths and population into integers using the 'astype' method.  
    filtered = filtered.astype({"Deaths":int, "Population":int})    

    return filtered

def process_mortality_data(input_path):
    # Reading csv file of all_mortality and applying a function called 'cleanup_mortality_data' to the DataFrame all_mortality.
    all_mortality = pd.read_csv(f"{input_path}/Underlying Cause of Death, 2018-2021, Single Race All.txt",sep="\t",
                                lineterminator='\r', dtype={'State Code': 'str'})
    all_mortality = cleanup_mortality_data(all_mortality)
    
    
    
    # Reading csv file of circ_mortality that is mortality due to circulatory diseases putting it back in circ_mortality after cleaning up.
    
    circ_mortality = pd.read_csv(f"{input_path}/Underlying Cause of Death, 2018-2021, Single Race Circulatory.txt",sep="\t",
                                 lineterminator='\r', dtype={'State Code': 'str'})
    circ_mortality = cleanup_mortality_data(circ_mortality)
    
    
    # Reading and cleaning data for mortality due to diabeties.
    
    endoc_mortality = pd.read_csv(f"{input_path}/Underlying Cause of Death, 2018-2021, Single Race Endocrine.txt",sep="\t", 
                                  lineterminator='\r', dtype={'State Code': 'str'})
    endoc_mortality = cleanup_mortality_data(endoc_mortality)
    
    
    #concatenating two DataFrames, 'circ_mortality' and 'endoc_mortality', using the 'concat' function and saving the result in final. 
    
    
    circ_endoc_mortality = pd.concat([circ_mortality, endoc_mortality])
    
    #grouping the data by 'State Code' and calculating the sum of the 'Deaths' column for each state.
    
    circ_endoc_mortality = circ_endoc_mortality.groupby('State Code')['Deaths'].sum()
            
    
    
    #Combining the two data frames(all_mortality and final) by common column of 'State Code' through the function of merge. 
    #The 'merge_mortality' DataFrame should contain information from both the 'all_mortality' and 'final' DataFrames for the
    # rows where the state code matches.
    final_mortality = pd.merge(all_mortality, circ_endoc_mortality, how="inner", on=["State Code"])
    
    # renaming the columns from 'Deaths_y' and 'Deaths_x' to 'Deaths_conditions' and 'Deaths_All'
    final_mortality = final_mortality.rename( columns={'Deaths_y':'Deaths_conditions', 'Deaths_x':'Deaths_All'} )
    
    #calculating the crude rate of death by conditions over 100,000 of population.
    #final_mortality['Crude_Death_Rate_Conditions'] = (final_mortality['Deaths_conditions'] / merge_mortality['Deaths_All']) * 100000
    # Calculating mortality by conditions with respect to total population of the state
    final_mortality['Crude_Death_Rate_Conditions_Overall'] = (final_mortality['Deaths_conditions'] / final_mortality['Population']) * 100000
    
    return final_mortality
