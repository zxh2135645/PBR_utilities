__author__ = 'sf713420'

from glob import glob
import numpy as np
import scipy.io as spio

affine = glob('/data/henry7/PBR/subjects/ms1244/t1Ants_reg_long/mse3670__mse3633/*Affine*')
affine = ''.join(affine)
matdata = spio.loadmat(affine)
print(matdata)
