# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:10:38 2020

@author: szh002
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as opt
# import seaborn as sns
import sugawara



### Read the output.asc file
skip_rows = 16  # Number of rows to skip in the output file
output_file = 'output.asc' # Name of the output file

# Read data from the output file
data = pd.read_csv(output_file,
                   skiprows=skip_rows,
                   skipinitialspace=True,
                   index_col='Time')

# Create vector with time stamps
time_index = pd.date_range('1994 12 07 20:00', periods=len(data), freq='H')

# Add time stamps to observations
data.set_index(time_index, inplace=True)

# =============================================================================
# Ex_1
# =============================================================================
# Resampling the data so the average of 1 year is presented. Feel free to explore with different 
data_print = data['Qrec'].resample('1Y').mean()
plt.plot(data_print)
plt.xticks(rotation=25)
plt.savefig('Year_Shaoxu')
plt.show()

# =============================================================================
# Ex_2
# =============================================================================
# build a test coding matrix with 0.01 difference
data_print = data['Qrec'][:1000]
    
for i in range(1000):
    data_print[i] = 0.01*i + data_print[i]
    plt.plot(data_print)
plt.show()