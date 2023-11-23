"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

# choose input files
folder = 'input_Vele'
bills_gas = 'bills_gas_Vele'
schedules = 'heating_schedules_test'
dhw = 'dhw_test'
festivities = 'festivities_test'
holidays = 'holidays_test'



# heating load profiles generation
ls.heating_profile(folder,bills_gas,schedules,festivities,holidays,dhw, 2021, latitude = 44.26, longitude = 9.45, climate_zone=True)

# you can find the generated profiles in "generated_profiles" folder.