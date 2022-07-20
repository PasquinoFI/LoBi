"""
LoBi: Load profiles from Bills

stochastic distribution used to simulate load
"""

import random

def mmm_distribution(minimum, maximum, mean, decimal):      
    """
    This function randomly extracts a value from a probability distribution 
    of which we know the minimum, maximum and mean.
    The total amount does not change, the probability of the average is respected.
    The distribution used is the combination of two uniform distributions.
    Decimal is the number of decimal to return
    """
    
    delta=maximum-minimum
    
    if delta>0:
        left=mean-minimum
        k=left/delta
        d=random.random()
        
        if d>k:  
            v=random.uniform(minimum,mean)
        else:
            v=random.uniform(mean,maximum)  
    
    else:
        v = 0
        
    return(round(v,decimal))

    
    