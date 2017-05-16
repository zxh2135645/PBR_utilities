__author__ = 'sf713420'

from glob import glob
import numpy as np
import scipy.io as spio
import nibabel as nib

affine = glob('/data/henry7/PBR/subjects/ms776/t1Ants_reg_long/mse867__mse866/output_0GenericAffine.mat')
affine = ''.join(affine)
matdata = spio.loadmat(affine)
#print(matdata)
#print(matdata["fixed"])
print(matdata["AffineTransform_float_3_3"])
matrix = matdata["AffineTransform_float_3_3"][:9]
new_matrix = np.resize(matrix, (3, 3))
det = np.linalg.det(new_matrix)
print("The affine determinant is: ", det)



jcb = nib.load('/data/henry7/PBR/subjects/ms776/t1Ants_reg_long/mse867__mse866/output_jacobian.nii.gz')
jcb_data, aff = jcb.get_data(), jcb.affine

new_jcb_data = np.multiply(jcb_data, det)

new_image = nib.Nifti1Image(new_jcb_data, affine=aff)
outfile = '/data/henry7/james/subjects/ms776/affine_substraction/output_jacobian_scaled_affined.nii.gz'
# nib.save(new_image, outfile)

"""
convertToAffineType = '/data/henry7/PBR/subjects/ms1244/t1Ants_reg_long/mse5466__mse3670/matrix_convertToAffineType.mat'
matdata2 = spio.loadmat(convertToAffineType)
print(matdata2)
"""
