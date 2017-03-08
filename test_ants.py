__author__ = 'sf713420'

from glob import glob
from subprocess import run
import os
# Test ms1244 of ants
mseIDs = ['mse2439', 'mse3622', 'mse2440', 'mse2441', 'mse2442', 'mse2445', 'mse2443', 'mse2446',
          'mse3634', 'mse3633', 'mse3670', 'mse5466']
input_dir = [glob("/data/henry7/PBR/subjects/{0}/antsCT/ms1244*/BrainSegmentation.nii.gz".format(f)) for f in mseIDs]
print(input_dir)
output_dir = '/data/henry7/james/test_ants/'

for i in range(1, len(input_dir)):
    tp0 = ''.join(input_dir[i-1])
    tp1 = ''.join(input_dir[i])
    output_path = os.path.join(output_dir, mseIDs[i-1] + '__' + mseIDs[i])
    print(tp0, tp1)
    print(output_path)
    run(['siena', tp0, tp1, '-o', output_path])
