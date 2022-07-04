import numpy as np
import pandas as pd
import random
from collections import Counter
import matplotlib.pyplot as plt

" load profiles from bills"


# import bill
bill_demand = pd.read_excel('bill.xlsx') # dataframe 12x3
bill_demand.columns = ('kWh',1,2,3,'Tot') # index correction

# household input
o = 4 # occupants
do = 1 # occupants during daylight hours

# iperparameters


############################################ Time slot definition F1 F2 F3

Weekday = np.ones(24)
Saturday = np.zeros(24)
Sunday = np.zeros(24)    

Day_type = np.ones(365) # 1=Weekday 2=Saturday 3=Sunday
Day_type[5:365:7] = 2 
Day_type[6:365:7] = 3 
 
### F3
Sunday[0:24] = 3 
Weekday[0:7] = 3
Weekday[23] = 3
Saturday[0:7] = 3
Saturday[23] = 3    

### F2
Saturday[7:23] = 2
Weekday[7] = 2
Weekday[19:23] = 2     

### F1 where the value 1 remains

dm=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # duration of months [days]
months_365 = [] # idx = day (0-365), value = month (0-11). Usefull below.
for m in range(len(dm)):
    for d in range(dm[m]):    
        months_365.append(m)

time_slots = [] # idx = hour (0-8760), value = time_slot (1,2,3). Usefull below.
months_8760 = [] # idx = hour (0-8760), value = month (0-11). Usefull below.

for d in range(365):        
    
    dt = Day_type[d] # 1=Weekday 2=Saturday 3=Sunday 
    m = months_365[d] # Month 0-11
    
    for h in range(24):
        
        if dt == 1:
            f = Weekday[h]
        if dt == 2:
            f = Saturday[h]
        if dt == 3:
            f = Sunday[h]
            
        time_slots.append(f)
        months_8760.append(m)
        
time_slots = np.array(time_slots)
months_8760 = np.array(months_8760)