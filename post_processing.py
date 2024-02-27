"""
LoBi: Load profiles from Bills

post processing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

a = pd.read_csv('C://Users//pasqui//Desktop//GIT//LoBi//generated_profiles//bills_ele_test.csv')
a.columns = ['Time','kWh']

# un anno
plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(0,8760)
plt.ylim(0,)
plt.show()

# giorno preciso
day = 9
plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*day,24*day+24)
plt.ylim(0,)
plt.xticks([24*day,24*day+6,24*day+12,24*day+18,24*day+24],[0,6,12,18,24])
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*9,24*16)
plt.ylim(0,)
plt.title('Settimana di gennaio')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*37,24*44)
plt.ylim(0,)
plt.title('Settimana di febbraio')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*65,24*72)
plt.ylim(0,)
plt.title('Settimana di marzo')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*93,24*100)
plt.ylim(0,)
plt.title('Settimana di aprile')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*121,24*128)
plt.ylim(0,)
plt.title('Settimana di maggio')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*151,24*160)
plt.ylim(0,)
plt.title('Settimana di giugno')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*263,24*270)
plt.ylim(0,)
plt.title('Settimana di settembre')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*293,24*300)
plt.ylim(0,)
plt.title('Settimana di ottobre')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*323,24*330)
plt.ylim(0,)
plt.title('Settimana di novembre')
plt.show()

plt.figure(dpi=1000)
plt.plot(a.index,a['kWh'])
plt.grid()
plt.xlim(24*334,24*342)
plt.ylim(0,)
plt.title('Settimana di dicembre')
plt.show()