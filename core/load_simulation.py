from core.time_slots import *
import core.stochastic_distribution as sd
import numpy as np
import pandas as pd
import os

"""
LoBi: Load profiles from Bills

load profile generation: different way to distribute load are available    
"""
        
def random_profile(p_min,p_max,bill_folder,bill_name,):
    """
    
    Parameters
    ----------
    p_min : float 
        minimum load, for example fridge laod [kW or kWh]
    p_max : float
        maximum load, committed power [kW or kWh]
    bill_name :  str
        bill file name, the file must be formatted as bill_example.xlsx
    bill_folder: str
        name of the folder in which the bill is

    Returns
    -------
    file.csv 
    simulated laod profile each hour of the year [kWh]

    """
        
    # import bill
    bill = pd.read_excel(f"{bill_folder}/{bill_name}.xlsx") # dataframe 12x3

    # initialise load profile
    load = np.zeros(8760)

    # simulate load each hour
    for h in np.arange(8760):
        ts = time_slots[h]
        m = months_8760[h]    
        load[h] = sd.mmm_distribution( p_min, p_max, (bill[ts][m] / hours_available[ts][m]) , 3)
            

    directory = './generated_profiles'
    if not os.path.exists(directory):
        os.makedirs(directory)                              
    load = pd.DataFrame(load)
    load.to_csv(f"{directory}/{bill_name}_rp.csv")
        
    return()        
                           







