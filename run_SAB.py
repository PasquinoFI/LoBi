"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

# choose input files
folder = 'input_SAB'

bills_ele = 'bills_ele_SAB'
bills_ele = 'bills_ele_Dino'
bills_ele = 'bills_ele_NEXT'
#bills_ele = 'bills_ele_NEXT_GIMA'
bills_ele = 'bills_ele_Acco'
bills_ele = 'bills_ele_Landucci'
bills_ele = 'bills_ele_Tom'
#bills_ele = 'bills_ele_4S'

bills_ele = 'bills_ele_Golf'
bills_gas = 'bills_gas_Golf'


profiles = 'ele_profiles_test'
festivities = 'festivities_test'
holidays = 'holidays_test'
schedules = 'heating_schedules_test'
dhw = 'dhw_test'


# heating load profiles generation
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021)
ls.heating_profile(folder,bills_gas,schedules,festivities,holidays,dhw, 2021, latitude = 43.706, longitude = 11.761, climate_zone=True)
# you can find the generated profiles in "generated_profiles" folder.