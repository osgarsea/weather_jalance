# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 07:16:00 2021

@author: costao1
"""

import pandas as pd


file_name = 'Temperaturas_Jalance.xls'

raw_data = pd.read_excel('data\{}'.format(file_name), sheet_name = None, header = 1)


year = 1986

year_data = raw_data[str(year)]

# Rename months column
year_data.rename(columns = {year : 'month'}, inplace = True)
# Fill null month names
year_data['month'] = year_data['month'].fillna(method='ffill')




def extract_rain (year_data):
    # Extract rain data
    rain_mm = year_data.iloc[26:39,[0,7]]
    
    
    # Rename the months with numbers
    orig = rain_mm.month.unique().tolist()
    new = list(range(1, 13)) + ['Annual']
    rain_mm['month'] = rain_mm['month'].replace(orig, new)
    
    # Use months as indexes
    rain_mm.set_index('month', inplace = True)
    
    # Rename column
    rain_mm.rename(columns = {6: year}, inplace = True)
    
    # Convert string values to float
    rain_mm[year] = rain_mm[year].astype(float)
    
    return rain_mm


rain_mm = extract_rain (year_data)



temperature = year_data.iloc[0:24,0:33]


orig = temperature.month.tolist()
new = list(range(1, 13)) + ['Annual']
rain_mm['month'] = rain_mm['month'].replace(orig, new)
