"""
LoBi: Load profiles from Bills

load simulation   
"""

import core.stochastic_distribution as sd
from core.load_shifting import load_shifting
import numpy as np
import pandas as pd
import os
import pvlib
import pickle


def electricity_profile(folder, bills, profiles, festivities, holidays, year, random=False, shifting=False, output=False):
    """
    
    Parameters
    ----------

    filename :  str
        bill file name, the file must be formatted as bill_example.xlsx
        
    folder: str
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
        
    name = bills # save name for results
    
    # reading input data
    bills = pd.read_excel(f"{folder}/{bills}.xlsx", header=0, index_col='Month')
    festivities = pd.read_excel(f"{folder}/{festivities}.xlsx", header=0)    
    festivities = pd.to_datetime(festivities['Festivities']).dt.date.tolist() # Transform "festivities" DataFrame in a List 
    festivities = [date_obj.strftime('%Y-%m-%d') for date_obj in festivities]   
    holidays = pd.read_excel(f"{folder}/{holidays}.xlsx", header=0)
    holidays = pd.to_datetime(holidays['Holidays']).dt.date.tolist()
    holidays = [date_obj.strftime('%Y-%m-%d') for date_obj in holidays]
    
    weights = {}
    for m0 in range(12):
        m = m0+1
        weights[m] = pd.read_excel(f"{folder}/{profiles}.xlsx", header=0, index_col='Hour', sheet_name = m0)
    
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
        if df.loc[date,'DayType'][0] < 6:
            df.loc[date, 'DayType'] = 7                                                          # Set holidays
    
    # Month
    df['Month'] = df.index.month
    
    # Yearly unit profile generation
    df['UnitLoad'] = 0    
    for i, datetime in enumerate(df.index):
        daytype = df.loc[datetime,'DayType']    
        month = df.loc[datetime,'Month']
        df.loc[datetime,'UnitLoad'] = weights[month].loc[df.index.hour[i], weights[month].columns[daytype]]               
       
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
                          
    if shifting:
        shift = ""
        for ls in shifting:    
            shift += "_"+str(shifting[ls])
            shift += "("+str(ls)+")"
        name += shift
    if random:
        name += '_rp'
        
    df = df.round(3)
    df.rename(columns={'Load':'kW'}, inplace=True)
    load = df.loc[:,'kW']
    load = pd.DataFrame(load)
    load.to_csv(f"{directory}/{name}.csv")
    
    if output:
        return(df)
    else:
        return()        
                           
    

def heating_profile(folder, bills, schedules, festivities, holidays, dhw, year, latitude, longitude, climate_zone=False, output=False):
    """
    
    Parameters
    ----------

    filename :  str
        bill file name, the file must be formatted as bill_example.xlsx
        
    folder: str
        name of the folder in which the bill is
        
    year: int
        
    latitude,longitude: float
    
    climate_zone: bool
        if True GG, climate climate_zone and relative limits on heating ignition are calculated and imposed
        
    Returns
    -------
    file.csv 
    simulated heatig profile each hour of the year [kWh]

    """

    name = bills # save name for results

    # reading input data
    bills = pd.read_excel(f"{folder}/{bills}.xlsx", header=0, index_col='Month')
    bills['kW'] = bills['smc'] * 10.69
    schedules = pd.read_excel(f"{folder}/{schedules}.xlsx",  header=0, index_col='Hour')
    dhw_profile = pd.read_excel(f"{folder}/{dhw}.xlsx", header=0, index_col='Hour')
    festivities = pd.read_excel(f"{folder}/{festivities}.xlsx",  header=0)    
    festivities = pd.to_datetime(festivities['Festivities']).dt.date.tolist() # Transform "festivities" DataFrame in a List 
    festivities = [date_obj.strftime('%Y-%m-%d') for date_obj in festivities]   
    holidays = pd.read_excel(f"{folder}/{holidays}.xlsx", header=0)
    holidays = pd.to_datetime(holidays['Holidays']).dt.date.tolist()
    holidays = [date_obj.strftime('%Y-%m-%d') for date_obj in holidays]
    
    # Generation of the basic datetime index
    datetime_index = pd.date_range(start = f'01-01-{year} 00:00', end   = f'31-12-{year} 23:00', freq  = 'H')    
    df = pd.DataFrame(datetime_index).set_index(0) 
    
    # Day type 0-7
    df['DayType'] = df.index.weekday      
    for date in festivities:                                                                 # Set festivities
        df.loc[date, 'DayType'] = 6
    for date in holidays:                                                                   
        df.loc[date, 'DayType'] = 7                                                          # Set holidays
   
    # Month and day
    df['Month'] = df.index.month
    df['Hour'] = df.index.hour
       
    # Air-temperature
    check = True # True if latitude and longitude are not changed from the old simulation
    directory = './previous_simulation'
    if not os.path.exists(directory): os.makedirs(directory)
    if os.path.exists('previous_simulation/location.pkl'):
        with open('previous_simulation/location.pkl', 'rb') as f: location = pickle.load(f) # previous simulation location
        if location['latitude'] != latitude or location['longitude'] != longitude:
            check = False  
    else:
        check = False                     
    if check and os.path.exists('previous_simulation/air_temperatures.csv'): # if the prevoius air_previous_simulatuion series can be used
        temp = pd.read_csv('previous_simulation/air_temperatures.csv')
    else: # if new air_temperature data must be downoladed from PV gis
        print('Downolading typical metereological year data from PVGIS')   
        temp = pvlib.iotools.get_pvgis_tmy(latitude, longitude, map_variables=True)[0]['temp_air']
        temp = pd.DataFrame(temp)
        temp.to_csv('previous_simulation/air_temperatures.csv')
        # save new location in previous_simulation            
        with open('previous_simulation/location.pkl', 'wb') as f: pickle.dump({'latitude':latitude,'longitude':longitude}, f)     
    
    # Schedules
    schedules.columns = [0,1,2,3,4,5,6,7]
    for i,ind in enumerate(df.index):
        h = df.loc[ind,'Hour']
        dt = df.loc[ind,'DayType']
        df.loc[ind,'schedules'] = schedules.loc[h,dt]
    
    # GG
    datetime_index = pd.date_range(start = f'01-01-{year} 00:00', end   = f'31-12-{year} 23:00', freq  = 'H')    
    temp.index = datetime_index
    temp = temp.resample('D').mean() # daily mean temperature
    temp['Month'] = temp.index.month
    temp['GG'] = 20 - temp['temp_air']
    temp.loc[temp['GG'] < 0 , 'GG'] = 0
    
    # dhw + cooking 
    bills['dhw_arera'] = [0.3307,0.3378,0.3002,0.2830,0.2545,0.2403,0.2133,0.2106,0.2400,0.2622,0.2984,0.3218] #ARERA
    bills['dhw'] = 0
    for m,ind in enumerate(bills.index):
        bills.loc[ind,'dhw'] = min( bills.loc[ind,'kW'] , bills.loc[ind,'dhw_arera'] / bills.loc[9,'dhw_arera'] * bills.loc[9,'kW'])
    
    # calculate GGa and relative climate zone limits
    GGa = temp.loc[: , 'GG'].sum()
    if GGa < 600:
        climate_zone = ['03-15','12-01'] # A
        bills.loc[4:11,'dhw'] = bills.loc[4:11,'kW']
    elif GGa < 900:
        climate_zone = ['03-31','12-01'] # B
        bills.loc[4:11,'dhw'] = bills.loc[4:11,'kW']
    elif GGa < 1400:
        climate_zone = ['03-31','11-15'] # C
        bills.loc[4:10,'dhw'] = bills.loc[4:10,'kW']
    elif GGa < 2100:
        climate_zone = ['04-15','11-01'] # D
        bills.loc[5:10,'dhw'] = bills.loc[5:10,'kW']
    elif GGa < 3000:
        climate_zone = ['04-15','10-15'] # E
        bills.loc[5:10,'dhw'] = bills.loc[5:10,'kW']
    else:
        climate_zone = False             # F
        bills.loc[5:10,'dhw'] = bills.loc[5:10,'kW']
            
    if climate_zone:
        zone1 = f"{year}-{climate_zone[0]}"
        zone2 = f"{year}-{climate_zone[1]}"
        df.loc[zone1:zone2,'schedules'] = 0
            
    bills['heating'] = bills['kW'] - bills['dhw'] # devide heat from dhw and cooking
    
    temp['switch-on hours'] = df.resample('D').sum()['schedules']
    
    temp.loc[temp['switch-on hours']==0,'GG'] = 0 
         
    for i,gm in enumerate(temp.resample('M').sum()['GG']):
        bills.loc[i+1,'GM'] = gm
        if gm>0:
            bills.loc[i+1,'heating/GM'] = bills.loc[i+1,'heating'] / gm
        else:
            bills.loc[i+1,'heating/GM'] = 0
            
    for i, ind in enumerate(temp.index):
        m = temp.loc[ind,'Month']
        temp.loc[ind,'heating'] = temp.loc[ind,'GG'] * bills.loc[m,'heating/GM']
        
    temp['heating/soh'] = temp['heating'] / temp['switch-on hours']
    
    # dhw: from monthly to daily
    temp['ng'] = 1
    temp.loc[df.resample('D').mean()['DayType']==7,'ng'] = 0 # festivities
    bills['dhw/ng'] = 0
    
    for i,ng in enumerate(temp.resample('M').sum()['ng']):     
        bills.loc[i+1,'dhw/ng'] = bills.loc[i+1,'dhw'] / ng
    
    # from daily to houyrly
    
    df['heating'] = 0
    df['dhw'] = 0
    for i,ind in enumerate(df.index):
        
        if df.loc[ind,'schedules'] == 1:
           
            ind2 = ind.date().strftime('%Y-%m-%d')
            df.loc[ind,'heating'] = temp.loc[ind2,'heating/soh']
            
        if df.loc[ind,'DayType'] != 7:
            m = df.loc[ind,'Month']
            h = df.loc[ind,'Hour']
            df.loc[ind,'dhw'] = bills.loc[m,'dhw/ng'] * dhw_profile.loc[h,'Profile'] / sum(dhw_profile['Profile'])
                 
    df['kW'] = df['heating'] + df['dhw']

    df = df.round(3)
    load = df.loc[:,'kW']
    load = pd.DataFrame(load)
    
    # save file.csv
    directory = './generated_profiles'
    if not os.path.exists(directory): os.makedirs(directory)
    load.to_csv(f"{directory}/{name}.csv")
  
    if output:
        return(df,temp,bills)
    else:
        return()
    
        
    

    

    
        

    
    
    
    
    
    
    
    
    

    
                
                
    
    
    
    


    



