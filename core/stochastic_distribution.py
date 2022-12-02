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
    
    if minimum <= mean < maximum:
        
        left=mean-minimum
        k=left/(maximum-minimum)
        d=random.random()
        
        if d>k:  
            v=random.uniform(minimum,mean)
        else:
            v=random.uniform(mean,maximum)  
    
    else:
        if mean < minimum:
            v = mean
        
        if minimum > maximum:
            print("the minimum must be less than the maximum")
            v = 0
            
        if mean > maximum:
            v = maximum
            print(mean)
            print(maximum)
            print("the mean must be less than the maximum")

    return(round(v,decimal))

    
    