"""
LoBi: Load profiles from Bills

load shifting   
"""


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
            
            bill[to][m] += bill[from_][m] * ( shifting[ls] / 100 )
            bill[from_][m] += - bill[from_][m] * ( shifting[ls] / 100 )
    
    return(bill)