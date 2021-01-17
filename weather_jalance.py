# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 07:16:00 2021

@author: costao1
"""

import pandas as pd
import numpy as np

file_name = 'Temperaturas_Jalance.xls'

raw_data = pd.read_excel('data\{}'.format(file_name), sheet_name = None, header = 1)




def extract_sheet (year, year_data):
    # Rename months column
    year_data.rename(columns = {year_data.columns[0] : 'month'}, inplace = True)
    # Fill null month names
    year_data['month'] = year_data['month'].fillna(method='ffill')
    
    return year_data



def extract_rain (year, year_data):
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


def extract_temperature (year, year_data):
    temperature = year_data.iloc[0:24,0:33]
    
    
    # Rename the months with integers
    # Assuming the order is correct
    temperature['month'] = np.arange(temperature.shape[0])/2 + 1
    temperature.loc[1::2,"month"] = temperature['month']-0.5
    temperature['month'] = temperature['month'].astype(int)
    
    # Rename second column
    temperature.rename(columns = {temperature.columns[1]: 'max_min'}, inplace = True)
    
    # Some columns are imported as float, convert all of them as int
    orig = list(temperature.columns[2:])
    new = list(map(int, list(map(float, orig))))
    dic = dict(zip(orig, new))
    temperature.rename(columns = dic, inplace = True)
    
    # Homogenise the column that says whether it is max or min temperature
    temperature['max_min'] = temperature['max_min'].str.lower()
    temperature.loc[temperature['max_min'].str.contains('max'), 'max_min'] = 't_max'
    temperature.loc[temperature['max_min'].str.contains('min'), 'max_min'] = 't_min'
    
    # Convert values to float
    for col in temperature.columns[2:]:
        temperature[col] = temperature[col].astype(float)
    
    temperature.set_index(['month', 'max_min'], inplace = True)
    
    temperature_stack = temperature.stack().unstack('max_min')
    temperature_stack.rename_axis(['month', 'day'], inplace = True)
    
    return temperature_stack


def reformat_temperature (year, temperature_stack, t_max, t_min, i):
    t_max_tmp = temperature_stack['t_max'].rename(year, inplace = True).to_frame()
    t_min_tmp = temperature_stack['t_min'].rename(year, inplace = True).to_frame()
    
    
    if i == 1:
        t_max = t_max_tmp
        t_min = t_min_tmp
    else:
        t_max = pd.concat([t_max, t_max_tmp], axis = 1)
        t_min = pd.concat([t_min, t_min_tmp], axis = 1)
    
    return t_max, t_min


def tmax_tmin (raw_data):
    i = 1
    
    t_max = ''
    t_min = ''
    
    # year = 1986
    # year_data = extract_sheet (year, raw_data)
    
    for key, year_data in raw_data.items():
        
        year = int(key)
        value = year_data
        print('-------------------------------------------')
        print('Extract Sheet for {}'.format(year))
        year_data = extract_sheet (year, value)
        
        # print(year_data)
        # Fill null month names
        year_data['month'] = year_data['month'].fillna(method='ffill')
        
       
        # rain_mm = extract_rain (year, year_data)
    
        print('Extract Temperature for {}'.format(year))
        temperature = extract_temperature (year, year_data)
        
        print('Reformat Temperature for {}'.format(year))
        t_max, t_min = reformat_temperature (year, temperature, t_max, t_min, i)
        
        i += 1
        
        if year == 2000:
            t2000 = temperature
        
    return t_max, t_min, t2000
    
    
t_max, t_min, t2000 = tmax_tmin (raw_data)



