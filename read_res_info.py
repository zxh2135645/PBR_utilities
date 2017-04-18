__author__ = 'sf713420'

import os
import signal
from subprocess import Popen, PIPE
import sys

cmd = ['fslhd', '/data/henry7/PBR/subjects/mse5466/alignment/ms1244-mse5466-040-MPRAGE_64channel_p2.nii.gz']
proc = Popen(cmd, stdout=PIPE)
dim_lines = [l.decode("utf-8").split() for l in proc.stdout.readlines()[5:8]]

x_pix = int(dim_lines[0][1])
y_pix = int(dim_lines[1][1])
z_pix = int(dim_lines[2][1])
print(x_pix,y_pix,z_pix)

proc = Popen(cmd, stdout=PIPE)
res_lines = [l.decode("utf-8").split() for l in proc.stdout.readlines()[18:21]]
x_res = float(res_lines[0][1])
y_res = float(res_lines[1][1])
z_res = float(res_lines[2][1])
print(x_res, y_res, z_res)



