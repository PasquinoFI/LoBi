"""
LoBi: Load profiles from Bills

push run!
"""

from core import load_simulation as ls

#%%################################################################ INPUT FILES

folder = 'input_test' # folder in wwiich the input files are (you could creare your own input_dev and manage it from run_dev)

bills_ele = 'bills_ele_test'
profiles = 'ele_profiles_test'
#profiles = 'ele_profiles_commercial_cigre'
#profiles = 'ele_profiles_industrial_cigre'
#profiles = 'ele_profiles_residential_cigre'

bills_gas = 'bills_gas_test'
schedules = 'heating_schedules_test'
dhw = 'dhw_test'

festivities = 'festivities_test'
holidays = 'holidays_test'


#%%################################################################ RUN

# ele load profiles generation
ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021)

# try to add casuality to the electricity serie or to perform load shifting between time slots
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021, random = [0.002,3])
#ls.electricity_profile(folder,bills_ele,profiles,festivities,holidays, 2021, random = [0.002,3], shifting = {"F3F1":30,"F2F1":20})

# heating load profiles generation
#ls.heating_profile(folder,bills_gas,schedules,festivities,holidays,dhw, 2021, latitude = 43.76, longitude = 11.28, climate_zone=True)

# you can find the generated profiles in "generated_profiles" folder.


