"""
author: James Zhang
"""

import matplotlib.pyplot as plt
from math import floor, ceil
from matplotlib.pyplot import grid


f = open('/Users/jameszhang/PBR_utilities/PBVC.txt')
lines = f.readlines()
print(lines)
f.close()
PBVC_list = []
for idx in lines:
    element = idx.split()
    PBVC_list.append(float(element[1]))
    
print(PBVC_list)
    
x_axis = list(range(1, len(lines)+1))
fig, ax = plt.subplots()
ax.plot(x_axis, PBVC_list, 'ro')
ax.axis([0, len(lines)+2, floor(min(PBVC_list)), ceil(max(PBVC_list))])
grid()
ax.axhline(y=0, color='b')
plt.xlabel('Mse Pairs Through Time')
plt.ylabel('Percentage of Brain Volume Change')
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





