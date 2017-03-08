__author__ = 'sf713420'

from glob import glob
from subprocess import run
# Test ms1244 of ants
mseIDs = ['mse2439', 'mse3662', 'mse2440', 'mse2441', 'mse2442', 'mse2445', 'mse2443', 'mse2446',
          'mse3634', 'mse3633', 'mse3670', 'mse5466']
input_dir = [glob("/data/henry7/PBR/subjects/{0}/antsCT/ms1244*/BrainSegmentation.nii.gz".format(f)) for f in mseIDs]
print(input_dir)
output_dir = '/data/henry7/james/test_ants'

for i in range(1, len(input_dir)):
    tp0 = ''.join(input_dir[i-1])
    tp1 = ''.join(input_dir[i])
    print(tp0, tp1)
    run(['siena', tp0, tp1, '-o', output_dir])
