"""
author: James Zhang
"""

import matplotlib.pyplot as plt
from math import floor, ceil


f = open('/data/henry7/PBR/subjects/ms1244/siena/PBVC.txt')
lines = f.readlines()
print(lines)
f.close()
PBVC_list = []
for idx in lines:
    element = idx.split()
    PBVC_list.append(float(element[1]))
    
print(PBVC_list)
    
x_axis = list(range(1, len(lines)+1))
plt.plot(x_axis, PBVC_list, 'ro')
plt.axis([0, len(lines)+2, floor(min(PBVC_list)), ceil(max(PBVC_list))])
plt.show()




