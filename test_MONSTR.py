__author__ = 'sf713420'

from subprocess import Popen, run
import os

working_dir = '/data/henry7/james/MONSTR'
t1 = os.path.join(working_dir, 'ms1244-mse2442-002-AX_T1_3D_IRSPGR.nii')
atlas = os.path.join(working_dir, 'ADNI_atlas')
outdir = os.path.join(working_dir, 'test_subprocess')

cmd = ['MONSTR.sh', '--t1', t1, '--ncpu', '12', '--atlasdir', atlas, '--natlas', '5', '--o', outdir, '--robust']
# proc = Popen(cmd)
# print(proc.args)
run(cmd)