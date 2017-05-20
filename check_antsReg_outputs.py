#! /usr/bin/env python
from glob import glob
from nipype.utils.filemanip import load_json, save_json
import os
import pandas as pd

if __name__ == '__main__':
    outdir = '/data/henry7/PBR/subjects/'
    df = pd.read_csv("/data/henry7/james/antje_cohort/no_qb3_antje_transition_cohort.csv")
    msid_set = set(df['msid'])
    msid_set_sorted = sorted(list(msid_set))
    print("msid scanned are :", msid_set_sorted)
    check = {}
    check['not_run_yet'] = []
    check['need_rerun'] = []
    check['finished'] = []
    for msid in msid_set_sorted:
        check_status = glob(os.path.join(outdir, msid, 't1Ants_reg_long', 'status.json'))
        if len(check_status) == 0:
            check['not_run_yet'].append(msid)
        else:
            print(check_status)
            check_status = ''.join(check_status)
            status = load_json(check_status)
            if len(status['mseIDs']) == len(status['fixed_image']) + 1:
                check['finished'].append(msid)
            else:
                check['need_rerun'].append(msid)
    print(check)
    save_json('/data/henry7/james/antje_cohort/check_pbr_outputs.json', check)






