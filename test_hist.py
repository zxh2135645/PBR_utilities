__author__ = 'sf713420'
from nibabel import freesurfer as nfs
import numpy as np
import nibabel as nib
from scipy.ndimage import label

#mgz = nfs.load('/data/henry6/PBR/surfaces/ms1244-mse5466-040-MPRAGE_64channel_p2/mri/aparc+aseg.mgz')
#print(mgz)

img = nib.load('/data/henry6/PBR//surfaces/ms1244-mse5466-040-MPRAGE_64channel_p2/mri/aparc+aseg_convert.nii.gz')
data = img.get_data()
print("The sum is: ", np.sum(data))

labels = [4, 5, 14, 15, 24, 43, 44, 72]
# 4 is Left-Lateral-Ventricle
# 5 is Left-Inf-Lat-Vent
# 14 is 3rd Ventricle
# 15 is 4th Ventricle
# 43 is Right-Lateral-Ventricle
# 44 is Right-Inf-Lat-Vent
# 24 is CSF
# 72 is Fifth-Ventricle

ventricle = np.where(np.logical_or.reduce([data == i for i in labels]))
print(ventricle)

img2 = nib.load('/data/henry7/PBR/subjects/mse5466/alignment/ms1244-mse5466-040-MPRAGE_64channel_p2.nii.gz')
data2, aff = img2.get_data(), img2.affine
print("The image is: ", data2[ventricle])

ventricle_median = np.median(data2[ventricle])
print("The median intensity of ventricle is:", ventricle_median)

mask = np.zeros(data2.shape)
mask[ventricle] = 1

#TODO How to find gray matters
#mask_out = nib.Nifti1Image(mask, affine=aff)
#nib.save(mask_out, '/data/henry6/PBR//surfaces/ms1244-mse5466-040-MPRAGE_64channel_p2/mri/ventricle_mask.nii.gz')

#labeled_img, nlabels = label(data > 0)
#print("The sum is: ", np.sum(labeled_img))
#print(labeled_img, nlabels)
