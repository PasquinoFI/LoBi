"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

# choose input files
folder = 'input_PM'

bills_ele = 'bills_ele_NEXT'
#bills_ele = 'bills_ele_NEXT_GIMA'

profiles = 'ele_profiles_test'
festivities = 'festivities_test'
holidays = 'holidays_test'


# ele load profiles generation
ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021)

# you can find the generated profiles in "generated_profiles" folder.