"""
LoBi: Load profiles from Bills

load shifting   
"""

from core.time_slots import *
import core.stochastic_distribution as sd

def load_shifting(bill,shifting):
    '''
    
    Parameters
    ----------
    bill : database 12x3
        enercy consumed in each time slot of each month
    shifting : dict
        "12": float [0-100] energy to shift from F1 to F2
        "13": float [0-100] energy to shift from F1 to F3
        "21": ...
        "23": ...
        "31": ...
        "32": ...       

    Returns
    -------
    New bill (database 12x3)

    '''
     
    for m in bill.index:
        for ls in shifting:
            
            from_ = int(str(ls)[0])
            to = int(str(ls)[1])
            
            bill[to][m] += round(bill[from_][m] * ( shifting[ls] / 100 ),3)
            bill[from_][m] += - round(bill[from_][m] * ( shifting[ls] / 100 ),3)
    
    return(bill)

def load_shifting2(serie,shifting):
    '''
    
    Parameters
    ----------
    serie : list of 8760 float 
        
    shifting : dict
        "12": float [0-100] energy to shift from F1 to F2
        "13": float [0-100] energy to shift from F1 to F3
        "21": ...
        "23": ...
        "31": ...
        "32": ...       

    Returns
    -------
    shiftes_serie

    '''

    bill = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # dataframe 12x3
    
    #bill count    
    for h,e in enumerate(serie):
        ts = time_slots[h]
        m = months_8760[h]
        bill[ts][m] += e
        
    old_bill = bill.copy()
    bill = load_shifting(bill,shifting)
    corrections = (bill-old_bill)/hours_available
        
    residual = pd.DataFrame(np.tile(np.zeros(3),(12,1)),index=np.arange(12),columns=(1,2,3)) # dataframe 12x3
    max_serie = max(serie)
    min_serie = min(serie)    
    
    for h in range(len(serie)):
        ts = time_slots[h]
        m = months_8760[h]
        
        mean = corrections[ts][m]
        
        if mean > 0: # adding load
            
            serie[h] += sd.mmm_distribution(0, max_serie, mean, 3) + residual[ts][m]
            
        else: # removing load
            serie[h] += - (sd.mmm_distribution(0, max_serie, -mean, 3) + residual[ts][m])
                
        if serie[h] > max_serie:
            residual[ts][m] = serie[h] - max_serie
            serie[h] = max_serie
                
        elif serie[h] < min_serie:
            residual[ts][m] = min_serie-serie[h]
            serie[h] = min_serie   
            
        else:
            residual[ts][m] = 0
            
    return(serie)
    