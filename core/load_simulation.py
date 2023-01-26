"""
LoBi: Load profiles from Bills

load simulation   
"""

import core.stochastic_distribution as sd
from core.load_shifting import load_shifting
import numpy as np
import pandas as pd
import os
        
def electricity_profile(foldername, filename, year, random=False, shifting=False, output=False):
    """
    
    Parameters
    ----------

    filename :  str
        bill file name, the file must be formatted as bill_example.xlsx
        
    foldername: str
        name of the folder in which the bill is
        
    random: list (optional)
        [p_min,p_max] float
        minimum and maximum load, for example fridge laod and committed power [kW or kWh]
        
    shifting: dict (optional)
        "F1F2": float [0-100] % of energy to shift from F1 to F2
        "F1F3": float [0-100] % of energy to shift from F1 to F3
        "F2F1": ...
        "F2F3": ...
        "F3F1": ...
        "F3F2": ...  

    Returns
    -------
    file.csv 
    simulated laod profile each hour of the year [kWh]

    """
        
    # reading input data
    bills = pd.read_excel(f"{foldername}/{filename}.xlsx", sheet_name='bills', header=0, index_col='Month')
    loads = pd.read_excel(f"{foldername}/{filename}.xlsx",  sheet_name='loads', header=0, index_col='Hour')
    festivities = pd.read_excel(f"{foldername}/{filename}.xlsx", sheet_name='festivities', header=0)    
    festivities = pd.to_datetime(festivities['Festivities']).dt.date.tolist() # Transform "festivities" DataFrame in a List 
    festivities = [date_obj.strftime('%Y-%m-%d') for date_obj in festivities]   
    holidays = pd.read_excel(f"{foldername}/{filename}.xlsx", sheet_name='holidays', header=0)
    holidays = pd.to_datetime(holidays['Holidays']).dt.date.tolist()
    holidays = [date_obj.strftime('%Y-%m-%d') for date_obj in holidays]
    
    
    if shifting:
        bills = load_shifting(bills,shifting)
        
    # Generation of the basic datetime index
    datetime_index = pd.date_range(start = f'01-01-{year} 00:00', end   = f'31-12-{year} 23:00', freq  = 'H')    
    df = pd.DataFrame(datetime_index).set_index(0)        
    
    # Day type 0-6
    df['DayType'] = df.index.weekday      
    for date in festivities:                                                                 # Set festivities
        df.loc[date, 'DayType'] = 6
   
    # Timeslots
    mask_F1   = (df['DayType'] < 5) & (df.index.hour >= 8)  & (df.index.hour < 19)           # Mask F1 
    mask_F2_m = (df['DayType'] < 5) & (df.index.hour == 7)                                   # Mask F2 workday morning
    mask_F2_e = (df['DayType'] < 5) & (df.index.hour >= 19) & (df.index.hour < 23)           # Mask F2 workday evening   
    mask_F2_s   = (df['DayType'] == 5) & (df.index.hour >= 7)  & (df.index.hour < 23)        # Mask F2 saturday    
    df['TimeSlot'] = 3                                                                       # Set 3 to F3
    df['TimeSlot'].where(~mask_F1, other=1, inplace=True)                                    # Set 1 to F1 for Workdays       
    df['TimeSlot'].where(~mask_F2_m, other=2, inplace=True)                                  # Set 2 to F2 Workdays morning
    df['TimeSlot'].where(~mask_F2_e, other=2, inplace=True)                                  # Set 2 to F2 Workdays evening
    df['TimeSlot'].where(~mask_F2_s, other=2, inplace=True)                                  # Set 2 to F2 Saturdays
    
    for date in holidays:                                                                   
        df.loc[date, 'DayType'] = 7                                                          # Set holidays
    
    # Month
    df['Month'] = df.index.month
    
    # Yearly unit profile generation
    df['UnitLoad'] = 0    
    for i, datetime in enumerate(df.index):
        daytype = df.loc[datetime,'DayType']                                                                                                           
        df.loc[datetime,'UnitLoad'] = loads.loc[df.index.hour[i], loads.columns[daytype]]               
       
    # Calculate c_star coefficient: Total energy (unit) divided by month and timeslot
    c_star  = df.pivot_table(index='Month', columns='TimeSlot', values='UnitLoad', aggfunc=np.sum)  # [U/month]
    c_star.columns = bills.columns
    c = bills / c_star                                                                              # [kWh/month] / [U/month] = [kWh/U}
      
    df['Load'] = 0
    for i, ind in enumerate(df.index):
        timeslot    = df.loc[ind,'TimeSlot']                                        # Extract current timeslot
        month = ind.month                                                           # Extract current month
        df.loc[ind,'Load'] = c.iloc[month-1,timeslot-1] * df.loc[ind,'UnitLoad']    # c * unit load
        
    if random:
        for i, datetime in enumerate(df.index):
            df.loc[datetime,'Load'] = sd.mmm_distribution( random[0], random[1], df.loc[datetime,'Load'])
      
    # save file.csv
    directory = './generated_profiles'
    if not os.path.exists(directory): os.makedirs(directory)   
                          
    name = filename
    if shifting:
        shift = ""
        for ls in shifting:    
            shift += "_"+str(shifting[ls])
            shift += "("+str(ls)+")"
        name += shift
    if random:
        name += '_rp'
        
    df = df.round(3)
    load = df.loc[:,'Load']
    load = pd.DataFrame(load)
    load.columns = ['kWh']
    load.to_csv(f"{directory}/{name}.csv")
    
    if output:
        return(df)
    else:
        return()        
                           
    

# =============================================================================
# def heating_profile():
#     # coming soon...
# =============================================================================
                
                
    
    
    
    


    



