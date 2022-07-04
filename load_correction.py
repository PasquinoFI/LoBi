import numpy as np
import pandas as pd
import random
from collections import Counter
import matplotlib.pyplot as plt


def load_correction(load, bill, newfilename, committed_power, print_balances = False):
    """
    load: 'filename.csv' hourly laod curve of 8760 values [kWh] load = None if there is not an original curve to correct
    bill: 'filename.xlsx' 12x3 matrix containing the consumption each month in each time slot F1 F2 F3 [kWh]
    committet_power: [kW] --> kWh/h
    
    return corrected load
    """

    ############################################ Time slot definition F1 F2 F3
    
    Weekday = np.ones(24)
    Saturday = np.zeros(24)
    Sunday = np.zeros(24)    
    Day_type = np.ones(365) # 1=Weekday 2=Saturday 3=Sunday
     
    ### F3
    Day_type[6:365:7] = 3 
    Sunday[0:24] = 3 
    Weekday[0:7] = 3
    Weekday[23] = 3
    Saturday[0:7] = 3
    Saturday[23] = 3    
    
    ### F2
    Day_type[5:365:7] = 2 
    Saturday[7:23] = 2
    Weekday[7] = 2
    Weekday[19:23] = 2     
    
    ### F1 where the value 1 remains

    
    dm=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # duration of months [days]
    months_365 = [] # idx = day (0-365), value = month (0-11). Usefull below.
    for m in range(len(dm)):
        for d in range(dm[m]):    
            months_365.append(m)
        
        
    ############################################  comparison of energy demands
    if load == None:
        original_load = np.zeros(8760)
    else:
        original_load = pd.read_csv('data/'+load)['0'] # array 8760
    original_demand = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # dataframe 12x3

    bill_demand = pd.read_excel('data/'+bill) # dataframe 12x3
    bill_demand.columns = ('kWh',1,2,3,'Tot') # index correction
    
    ##### load shifting
# =============================================================================
#     for m in range(12):
#         bill_demand[1][m] += bill_demand[2][m]*0.2 + bill_demand[3][m]*0.2
#         bill_demand[2][m] = bill_demand[2][m]*0.8
#         bill_demand[3][m] = bill_demand[3][m]*0.8
# =============================================================================
    
    
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
            e = original_load[d*24+h]
            original_demand[f][m] += e 
            
    time_slots = np.array(time_slots)
    months_8760 = np.array(months_8760)
    
    add_demand = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # initialise dataframe 12x3 energy to add for each month for each time slot
    remove_demand = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # initialise dataframe 12x3 energy to remove for each month for each time slot
    hours_available = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # initialise dataframe 12x3 available hours of each time slot in every month
    
    print(original_demand)
    #print(bill_demand)
    
    print(sum(original_demand[1]))
    print(sum(original_demand[2]))
    print(sum(original_demand[3]))
    
    for f in original_demand:
        for m in np.arange(12):
            
            e = bill_demand[f][m] - original_demand[f][m]
            if e >0:
                add_demand[f][m] = e
            else:
                remove_demand[f][m] = - e 
                
            hours_available[f][m] = Counter(time_slots[months_8760==m])[f]
    
    ##################################################### add or remove energy
    def mmm_distibution(minimum, maximum, mean):    
        """
        This function randomly extracts a value from a probability distribution 
        of which we know the minimum, maximum and mean.
        The total amount does not change, the probability of the average is respected.
        The distribution used is the combination of two uniform distributions.
        """
        
        delta=maximum-minimum
        left=mean-minimum
        k=left/delta
        d=random.random()
        
        if d>k:  
            v=random.uniform(minimum,mean)
        else:
            v=random.uniform(mean,maximum)   
        
        return(v)
    
    add_load = np.zeros(8760)
    remove_load = np.zeros(8760)
    corrected_load = np.zeros(8761)
    
    for h in range(8760):
        f = time_slots[h]
        m = months_8760[h]
        
        mean = add_demand[f][m] / hours_available[f][m]
        maximum = committed_power        
        add_load[h] = mmm_distibution(0, maximum, mean)
        #add_load[h] = mean
        
        mean = remove_demand[f][m] / hours_available[f][m]
        maximum = committed_power
        remove_load[h] = mmm_distibution(0, maximum, mean)
        #remove_load[h] = mean

        
        corrected_load[h] += original_load[h] + add_load[h] - remove_load[h]
        
        ### correction considering committet_power 
        if corrected_load[h] > committed_power:
            corrected_load[h+1] += corrected_load[h] - committed_power
            corrected_load[h] = committed_power
        
        ### correction negative valued (may happen beause of remove_load)
            ### 25 Wh/h is the minimu (Fridge)
        if corrected_load[h] <0.025:
            corrected_load[h+1] += corrected_load[h]-0.025
            corrected_load[h] = 0.025
    
    corrected_load = corrected_load [:8760]
    
    if print_balances:
        print('\n')
        print(f"original demand = {sum(original_demand[1])+sum(original_demand[2])+sum(original_demand[3])}")
        print(f"bill demand = {sum(bill_demand[1])+sum(bill_demand[2])+sum(bill_demand[3])}")
        #print(f"to add demand = {sum(add_demand[1])+sum(add_demand[2])+sum(add_demand[3])}")       
        #print (f"added demand = {sum(add_load)} kWh")
        #print(f"to remove demand = {sum(remove_demand[1])+sum(remove_demand[2])+sum(remove_demand[3])}") 
        #print (f"removed demand = {sum(remove_load)} kWh")
        print(f"new demand = {sum(corrected_load)} kWh")
        
        
# =============================================================================
#     series_frame = pd.DataFrame(corrected_load)
#     series_frame.to_csv(f"data/{newfilename}.csv")
# =============================================================================
    
    return(original_load,add_load,remove_load)



if __name__ == "__main__":
    
    """
    Functional test
    """
           
    load_correction('ramp_u1.csv','bill_p1.xlsx','load_p1',3,True)
# =============================================================================
#     load_correction('ramp_u0.csv','bill_p2.xlsx','load_p2',5,True) # p2 si risonosce per il load maggiore veiocli elettrici
#     
#     load_correction('ramp_u2.csv','bill_c1.xlsx','load_c1',3,True) # c1 e c2 simili
#     load_correction('ramp_u4.csv','bill_c2.xlsx','load_c2',3,True) 
#     load_correction('ramp_u3.csv','bill_c3.xlsx','load_c3',3,True) # c3 consuma un po di più degli altri
#     
#     
#     load_correction('ramp_u23.csv','bill_p3.xlsx','load_p3',3,True) # p3 using u2 survey
#     load_correction('ramp_u44.csv','bill_p4.xlsx','load_c5',3,True) # c5 using u4 survey
#     load_correction('ramp_u04.csv','bill_c3.xlsx','load_c4',3,True) # c4 using u0 survey and c3 bill
# =============================================================================
    
    
# =============================================================================
#     p1=pd.read_csv('data/load_p1.csv')
#     p2=pd.read_csv('data/load_p2.csv')
#     p3=pd.read_csv('data/load_p3.csv')
#     p4=pd.read_csv('data/load_p4.csv')
#     c1=pd.read_csv('data/load_c1.csv')
#     c2=pd.read_csv('data/load_c2.csv')
#     c3=pd.read_csv('data/load_c3.csv')
#     c4=pd.read_csv('data/load_c4.csv')
# =============================================================================
    
# =============================================================================
#     load_correction('ramp_u1bis.csv','bill_p1.xlsx','shifted_load_p1bis',3,True)
#     load_correction('ramp_u0.csv','bill_p2.xlsx','shifted_load_p2bis',5,True) # p2 si risonosce per il load maggiore veiocli elettrici
#     
#     load_correction('ramp_u2bis.csv','bill_c1.xlsx','shifted_load_c1bis',3,True) # c1 e c2 simili
#     load_correction('ramp_u4bis.csv','bill_c2.xlsx','shifted_load_c2bis',3,True) 
#     load_correction('ramp_u3bis.csv','bill_c3.xlsx','shifted_load_c3bis',3,True) # c3 consuma un po di più degli altri
#     
#     
#     load_correction('ramp_u23bis.csv','bill_p3.xlsx','shifted_load_p3bis',3,True) # p3 using u2 survey
#     load_correction('ramp_u44bis.csv','bill_p4.xlsx','shifted_load_p4bis',3,True) # p4 using u4 survey
#     load_correction('ramp_u04bis.csv','bill_c3.xlsx','shifted_load_c4bis',3,True) # c4 using u0 survey and c3 bill
#     
# =============================================================================
    


#%% grafici per mostrare le correzioni
original,added,removed = load_correction('ramp_u1.csv','bill_p1.xlsx','shifted_load_p1',3,True)
original = original.to_numpy()

for g in np.arange(100):
    ori = original [g*24:g*24+24]
    add = added [g*24:g*24+24]
    rem = removed [g*24:g*24+24]
    x = np.arange(len(ori))
    width = 0.9
    
    if sum(rem)>0:
        plt.figure(dpi=1000,figsize=(10,5))
    
        plt.bar(x, ori, width, label='simulated', zorder=3,color='#4169e1')
        plt.bar(x, add, width,  label='added',bottom=ori, zorder=3,color='orange')
        plt.bar(x, rem, width,  label='removed', bottom=ori-add, zorder=3,color='red')
       
        plt.grid(axis='y',zorder=0)
            
        plt.legend()
        plt.ylabel("Hourly energy [kWh/h]")
        plt.xlabel("Time [h]")
        #plt.title("Energy community 4.6 kW 1.7 kWh Day "+str(70))
        plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24],['0','2','4','6','8','10','12','14','16','18','20','22','24'],fontsize=10)
        plt.ylim(ymin=0)
        #plt.yticks([-2,-1,0,1,2],['-2','-1','0','1','2'])
        plt.show()
      
#%% grafico 8 medie

user = ['p1','p2','p3','c1','c2','c3','c4','c5']        

plt.figure(dpi=1000,figsize=(10,5))

for u in user:
    p = pd.read_csv('data/load_'+u+'.csv')['0'].to_numpy()
    p = np.reshape(p,(365,24))
    pa = np.zeros(24)
    for e in p:
        pa += e
    pa = pa/365
    
    pa = list(pa)
    pa.append(pa[0])
    pa = np.array(pa)
    plt.plot(np.arange(25),pa,label=u)
    
plt.legend()
plt.ylabel("Hourly energy [kWh/h]")
plt.xlabel("Time [h]")
plt.ylim(ymin=0)
plt.grid(axis='y',zorder=0)
plt.xlim(0,24)
plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24],['0','2','4','6','8','10','12','14','16','18','20','22','24'],fontsize=10)
plt.show()



