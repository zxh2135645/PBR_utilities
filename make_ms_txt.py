__author__ = 'sf713420'

import numpy as np
import pbr
import os
from nipype.utils.filemanip import load_json
from pbr.workflows.nifti_conversion.utils import description_renamer
heuristic = load_json(os.path.join(os.path.split(pbr.__file__)[0], "heuristic.json"))["filetype_mapper"]
import pandas as pd
from subprocess import Popen, PIPE
import pandas as pd
import argparse
from os.path import join

get_numerical_msid = lambda x: str(int(x[2:]))

def get_all_mse(msid):
    cmd = ["ms_get_patient_imaging_exams", "--patient_id", get_numerical_msid(msid)]
    proc = Popen(cmd, stdout=PIPE)
    lines = [l.decode("utf-8").split() for l in proc.stdout.readlines()[5:]]
    tmp = pd.DataFrame(lines, columns=["mse", "date"])
    tmp["mse"] = "mse"+tmp.mse
    tmp["msid"] = msid
    return tmp

def get_modality(mse, nii_type="T1"):
    output = pd.DataFrame()
    num = mse.split("mse")[-1]
    cmd = ["ms_dcm_exam_info", "-t", num]
    proc = Popen(cmd, stdout=PIPE)
    lines = [description_renamer(" ".join(l.decode("utf-8").split()[1:-1])) for l in proc.stdout.readlines()[8:]]
    if nii_type:
        files = filter_files(lines, nii_type, heuristic)
        output["nii"] = files
    else:
        output["nii"] = lines
    output["mse"] = mse
    return output

def filter_files(descrip,nii_type, heuristic):
    output = []
    for i, desc in enumerate(descrip):
        if desc in list(heuristic.keys()):
            if heuristic[desc] == nii_type:
                 output.append(desc)
    return output

if __name__ == '__main__':
    df = pd.read_csv("/home/sf522915/antje_transition_cohort.csv")
    msid_set = set(df['msid'])
    msid_set_sorted = sorted(list(msid_set))
    print("There are {} msid patient will be tested". format(len(msid_set_sorted)))

    for msid in msid_set_sorted:
        # msid = msid.replace('ms', '')
        print(msid)
        out_filename = '/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/' + msid + '.txt'
        mse_df = get_all_mse(msid)
        print(mse_df.mse)
        with open(out_filename, 'w') as f:
            mse_list = mse_df.mse
            for mse in mse_list:
                seriesDesc = get_modality(mse, "T1")
                print(seriesDesc["nii"])
                if seriesDesc["nii"].any():
                    f.write(mse, "\n")



