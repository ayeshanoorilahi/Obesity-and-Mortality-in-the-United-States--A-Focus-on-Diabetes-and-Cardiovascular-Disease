# -*- coding: utf-8 -*-
"""
Created on Sat May  6 11:40:48 2023

@author: ayesh
"""

import matplotlib.pyplot as plt
import seaborn as sns

def scatter_plot(output_path, data):
    #drawing a scatter plot for obesity and mortality by conditions
    plt.rcParams['figure.dpi'] = 300
    fig,ax = plt.subplots()
    data.plot.scatter(ax=ax,x='ObesityPercent', y='Crude_Death_Rate_Conditions_Overall')
    plt.title('Obesity and Mortality by Diabetes and Cardiovascular Disease')
    plt.xlabel('Obesity%')
    plt.ylabel('Mortality Rate By Conditions')
    fig.tight_layout()
    plt.savefig(f'{output_path}/scatter_plot.png')




def reg_plot(output_path, data):
    # Set plot title and labels with reglot with confidence interval
    plt.rcParams['figure.dpi'] = 300
    fig,ax = plt.subplots()
    sns.regplot(data=data, x="ObesityPercent", y="Crude_Death_Rate_Conditions_Overall", ci =90)
    
    plt.title("Diabetes and Cardiovascular disease with 90% Confidence Interval")
    plt.suptitle("Regression plot of Obesity and Mortality")
    plt.xlabel('Obesity%')
    plt.ylabel('Mortality Rate By Conditions')
    
    # Save the regplot as a PNG file
    plt.savefig(f"{output_path}/regplot.png")