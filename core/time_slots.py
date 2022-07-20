"""
LoBi: Load profiles from Bills

Time slot definition: F1 F2 F3 under Italian regoulation
"""

import numpy as np
import pandas as pd
from collections import Counter

f_St = 0 # first saturday of the year 01/01/2022 was Saturday 

Weekday = np.ones(24)
Saturday = np.zeros(24)
Sunday = np.zeros(24)    

Day_type = np.ones(365) # 1=Weekday 2=Saturday 3=Sunday
Day_type[f_St:365:7] = 2 
Day_type[(f_St)+1:365:7] = 3 
 
### F3
Sunday[0:24] = 3 
Weekday[0:7] = 3
Weekday[23] = 3
Saturday[0:7] = 3
Saturday[23] = 3    
# F3 holidays
Day_type[0] = 3 # 01/01
Day_type[5] = 3 # 06/01
Day_type[114] = 3 # 25/04
Day_type[120] = 3 # 01/05
Day_type[152] = 3 # 02/06
Day_type[226] = 3 # 15/08
Day_type[304] = 3 # 01/11
Day_type[341] = 3 # 08/12
Day_type[358] = 3 # 25/12
Day_type[359] = 3 # 26/12

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
            ts = Weekday[h]
        if dt == 2:
            ts = Saturday[h]
        if dt == 3:
            ts = Sunday[h]
            
        time_slots.append(ts)
        months_8760.append(m)
        
time_slots = np.array(time_slots)
months_8760 = np.array(months_8760)

# counting hours avaible in each time-slot of each month
hours_available = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # initialise dataframe 12x3 available hours of each time slot in every month
for ts in [1,2,3]:
    for m in np.arange(12):                            
        hours_available[ts][m] = Counter(time_slots[months_8760==m])[ts]
