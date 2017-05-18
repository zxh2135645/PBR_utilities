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

labels = [4, 5, 14, 15, 24, 43, 44, 72, 213]
# 4 is Left-Lateral-Ventricle
# 5 is Left-Inf-Lat-Vent
# 14 is 3rd Ventricle
# 15 is 4th Ventricle
# 43 is Right-Lateral-Ventricle
# 44 is Right-Inf-Lat-Vent
# 24 is CSF
# 72 is Fifth-Ventricle
# 213 is lateral ventricle

labels2 = [2005, 2008, 2010, 2011, 2014, 2015, 2018, 2019, 2020, 2021, 2024, 2025, 2026, 2027, 2029, 2030, 2031, 2032, 2033, 2034,
           1005, 1008, 1010, 1012, 1014, 1018, 1019, 1020, 1022, 1024, 1025, 1026, 1027, 1029, 1031, 1032, 1035, 1032]

ventricle = np.where(np.logical_or.reduce([data == i for i in labels]))
gray_matter = np.where(np.logical_or.reduce([data == i for i in labels2]))
# print(ventricle)

img2 = nib.load('/data/henry7/PBR/subjects/mse5466/alignment/ms1244-mse5466-040-MPRAGE_64channel_p2.nii.gz')
data2, aff = img2.get_data(), img2.affine
print("The image is: ", data2[ventricle])

ventricle_median = np.median(data2[ventricle])
gray_matter_median = np.median(data2[gray_matter])
print("The median intensity of ventricle is:", ventricle_median,
      "The median intensity of gray matter is:", gray_matter_median)

mask = np.zeros(data2.shape)
mask[ventricle] = 1
mask2 = np.zeros(data2.shape)
mask2[gray_matter] = 1

#TODO How to find gray matters
#gray matters were roughly found
mask_out = nib.Nifti1Image(mask2, affine=aff)
#nib.save(mask_out, '/data/henry6/PBR//surfaces/ms1244-mse5466-040-MPRAGE_64channel_p2/mri/ventricle_mask.nii.gz')
nib.save(mask_out, '/data/henry6/PBR//surfaces/ms1244-mse5466-040-MPRAGE_64channel_p2/mri/gray_matter_mask.nii.gz')

#labeled_img, nlabels = label(data > 0)
#print("The sum is: ", np.sum(labeled_img))
#print(labeled_img, nlabels)
