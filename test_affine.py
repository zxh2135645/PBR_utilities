__author__ = 'sf713420'

from glob import glob
import numpy as np
import scipy.io as spio

affine = glob('/data/henry7/PBR/subjects/ms1244/t1Ants_reg_long/mse5466__mse3670/output_0GenericAffine.mat')
affine = ''.join(affine)
matdata = spio.loadmat(affine)
print(matdata)
print(matdata["fixed"])
print(matdata["AffineTransform_float_3_3"])

convertToAffineType = '/data/henry7/PBR/subjects/ms1244/t1Ants_reg_long/mse5466__mse3670/matrix_convertToAffineType.mat'
matdata2 = spio.loadmat(convertToAffineType)
print(matdata2)
