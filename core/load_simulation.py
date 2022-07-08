from core.time_slots import *
import core.stochastic_distribution as sd
import numpy as np
import pandas as pd

"""
LoBi: Load profiles from Bills

load profile generation: different way to distribute load are available    
"""
        
def random_profile(p_min,p_max,bill_name):
    """
    
    Parameters
    ----------
    p_min : float 
        minimum load, for example fridge laod [kW or kWh]
    p_max : float
        maximum load, committed power [kW or kWh]
    bill :  str
        bill file name, the file must be formatted as bill_example.xlsx

    Returns
    -------
    file.csv 
    simulated laod profile each hour of the year [kWh]

    """
    
    # import bill
    bill = pd.read_excel(f"bills/{bill_name}.xlsx") # dataframe 12x3
    
    # initialise load profile
    load = np.zeros(8760)

    # simulate load each hour
    for h in np.arange(8760):
        ts = time_slots[h]
        m = months_8760[h]    
        load[h] = sd.mmm_distribution( p_min, p_max, (bill[ts][m] / hours_available[ts][m]) , 3)
                                  
    load = pd.DataFrame(load)
    load.to_csv(f"generated_profiles/{bill_name}_random_profile.csv")
        
    return()        
                           

def weighted_profile(p_min,p_max,bill_name,weights):
    """
    
    Parameters
    ----------
    p_min : float 
        minimum load, for example fridge laod [kW or kWh]
    p_max : float
        maximum load, committed power [kW or kWh]
    bill :  str
        bill file name, the file must be formatted as bill_example.xlsx
    weights: dict
        "w1":
        "w2":
        "w3":

    Returns
    -------
    file.csv 
    simulated laod profile each hour of the year [kWh]


    """
    
    # import bill
    bill = pd.read_excel(f"bills/{bill_name}.xlsx") # dataframe 12x3
    
    # initialise load profile
    load = np.zeros(8760)

    # simulate load each hour
    for h in np.arange(8760):
        ts = time_slots[h]
        m = months_8760[h]    
        load[h] = sd.mmm_distribution( p_min, p_max, (bill[ts][m] / hours_available[ts][m]) , 3)
                                  
    load = pd.DataFrame(load)
    load.to_csv(f"generated_profiles/{bill_name}_random_profile.csv")
    
    return()









