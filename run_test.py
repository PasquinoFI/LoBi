"""
LoBi: Load profiles from Bills

push run!
"""

import core.load_simulation as ls

ls.electricity_profile("bills_test", "example_0", 2021)
ls.electricity_profile("bills_test", "example_0", 2021, random = [0.002,3])
ls.electricity_profile("bills_test", "example_0", 2021, random = [0.002,3], shifting = {"F3F1":30,"F2F1":20})





