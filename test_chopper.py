__author__ = 'sf713420'

def chopper(in_file):
    import subprocess
    from nipype.utils.filemanip import split_filename
    import os

    """cmd1 = ["robustfov", "-i", in_file]
    proc = subprocess.Popen(cmd1,stdout = subprocess.PIPE)
    res = proc.communicate()
    print(res)
    newfov = res[0].decode("utf-8").split("\n")[3].split(" ")[:-1]
    print(newfov)
    _,fname,ext = split_filename(in_file)
    out_file = os.path.abspath(fname+"_chop"+ext)
    cmd2 = ["fslroi", in_file, out_file] + newfov
    print(cmd2)
    proc2 = subprocess.Popen(cmd2)
    proc2.wait()

    """

    from nipype.interfaces.fsl import RobustFOV, Reorient2Std
    rfov = RobustFOV()
    rfov.inputs.in_file = in_file
    res = rfov.run()

    reo = Reorient2Std()
    reo.inputs.in_file = res.outputs.out_roi
    res = reo.run()
    out_file = res.outputs.out_file

    return out_file

if __name__ == '__main__':
    in_file = '/data/henry7/PBR/subjects/mse5466/nii/ms1244-mse5466-040-MPRAGE_64channel_p2.nii.gz'
    chopper(in_file)