"""
author: James Zhang
"""

import matplotlib.pyplot as plt
from math import floor, ceil
from matplotlib.pyplot import grid
import numpy as np


f = open('/Users/jameszhang/PBR_utilities/PBVC.txt')
lines = f.readlines()
print(lines)
f.close()
PBVC_list = []
for idx in lines:
    element = idx.split()
    PBVC_list.append(float(element[1]))
    
print(PBVC_list)

I = 100
brain_volume = []
brain_volume.append(I)
for i in range(len(PBVC_list)):
    I = I * (1 + PBVC_list[i]/100)
    brain_volume.append(I)
print(brain_volume)

# Plotting
    
x_axis = list(range(1, len(lines)+1))
fig, ax = plt.subplots()
ax.plot(x_axis, PBVC_list, 'bx', linewidth = 2, markeredgewidth = 2)
ax.axis([0, len(lines)+2, floor(min(PBVC_list)), ceil(max(PBVC_list))])
grid()
ax.axhline(y=0, color='b', linestyle = '--')
ax.set_xlabel('Mse Pairs Through Time')
ax.set_ylabel('Percentage of Brain Volume Change', color = 'b')
ax.tick_params('y', colors = 'b')

# Add trend line
z = np.polyfit(x_axis, PBVC_list, 1)
p = np.poly1d(z)
ax.plot(x_axis, p(x_axis), 'b-', linewidth = 1.5)
# the line equation
print("y = %.6fx + (%.6f)" %(z[0], z[1]))

if z[1] >= 0:
    ax.text(len(lines)/2 - 1, -0.5, "y = %.4fx + %.4f" %(z[0], z[1]))
else:
    ax.text(len(lines) / 2 - 1, -0.5, "y = %.4fx - %.4f" % (z[0], np.abs(z[1])))

# Hold on
x_axis = list(range(1, len(lines)+2))
ax1 = ax.twinx()
ax1.plot(x_axis, brain_volume, 'r-', linewidth = 2)
ax1.set_ylabel('Brain Volume Change', color = 'r')
ax1.tick_params('y', colors = 'r')

fig.tight_layout()
plt.show()


"""
#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.2,10,100)
fig, ax = plt.subplots()
ax.plot(x, 1/x)
ax.plot(x, np.log(x))
ax.set_aspect('equal')
ax.grid(True, which='both')

ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.show()
"""





