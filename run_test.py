"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

ls.electricity_profile("bills_test", "example_0_ele", 2021)
ls.electricity_profile("bills_test", "example_0_ele", 2021, random = [0.002,3])
ls.electricity_profile("bills_test", "example_0_ele", 2021, random = [0.002,3], shifting = {"F3F1":30,"F2F1":20})

ls.heating_profile("bills_test", "example_0_heat", 2021, latitude = 43.46, longitude = 11.14, climate_zone=True)
