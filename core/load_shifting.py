"""
LoBi: Load profiles from Bills

load shifting   
"""


def load_shifting(bills,shifting):
    '''
    
    Parameters
    ----------
    bills : database 12x3
        enercy consumed in each time slot of each month
    shifting : dict
        "F1F2": float [0-100] energy to shift from F1 to F2
        "F1F3": float [0-100] energy to shift from F1 to F3
        "F2F1": ...
        "F2F3": ...
        "F3F1": ...
        "F3F2": ...       

    Returns
    -------
    New bill (database 12x3)

    '''
     
    for m in bills.index:
        for ls in shifting:
            
            from_ = ls[0:2]
            to = ls[2:4]
          
            bills.loc[m,to] += round(bills.loc[m,from_] * ( shifting[ls] / 100 ),3)
            bills.loc[m,from_] += - round(bills.loc[m,from_] * ( shifting[ls] / 100 ),3)
          
    return(bills)

    