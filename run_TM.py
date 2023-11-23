"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

# choose input files
folder = 'input_TM'
bills_ele = 'bills_ele_TM'
profiles = 'ele_profiles_test'
bills_gas = 'bills_gas_TM'
schedules = 'heating_schedules_test'
dhw = 'dhw_test'
festivities = 'festivities_test'
holidays = 'holidays_test'


# ele load profiles generation
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021)
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021, random = [0.002,3])
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021, random = [0.002,3], shifting = {"F3F1":30,"F2F1":20})

# heating load profiles generation
ls.heating_profile(folder,bills_gas,schedules,festivities,holidays,dhw, 2021, latitude = 43.21, longitude = 11.43, climate_zone=True)

# you can find the generated profiles in "generated_profiles" folder.