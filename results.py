# -*- coding: ascii -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""

__author__ = 'Gerard Noseworthy gnoseworthy@gmail.com'
__maintainer__ = '$'
__vcs_id__ = '$'


from csv import DictReader
from collections import defaultdict
import matplotlib.pyplot as plt

import operator
collected = defaultdict(float)

sample_wind = r".\climate\output\sample_wind_site.csv"

times = []
wind = []
with open(sample_wind) as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        t_val = int(row.get('time'))
        s_val = float(row.get('wind_potential'))
        collected[t_val] += s_val
        times.append(t_val)
        wind.append(s_val)

sample_sun = r".\output\sample_solar_site.csv"

solar = []
with open(sample_sun) as csv_file:
    reader = DictReader(csv_file)
    for row in reader:

        t_val = int(row.get('time'))
        s_val = float(row.get('solar_pot'))
        # times.append(t_val)
        solar.append(s_val*10)
#

# plt.plot(times, solar)
three_solar = []
for i, val in enumerate(solar):
    try:
        three_solar.append(val + solar[i+1] + solar[i+2])
    except IndexError:
        pass

three_wind = []
for i, val in enumerate(wind):
    try:
        three_wind.append(val + wind[i+1] + wind[i+2])
    except IndexError:
        pass

fig, ax1 = plt.subplots()

ax1.plot(times[2:], three_wind, c='blue', label='Wind')



ax1.plot(times[2:], three_solar, c='orange',  label='Solar')

sums = [a + b for a, b in zip(three_wind, three_solar)]

ax1.plot(times[2:], sums, c='red', label='Total')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),shadow=True, ncol=3)


plt.show()

