__author__ = 'sf713420'

import os
from glob import glob
import pandas as pd
from nipype.utils.filemanip import save_json, load_json

def get_config():
    """
    ===========================
    Configuration for Workflows
    ===========================
    plugin: "Linear", "SGE" for grid
    plugin_args: qsub args
    outputsink_directory: where to store results
    working_directory: where to run things
    """
    config = dict()

    #config["plugin"] = "Linear"#"SGE"
    #config["plugin_args"] = {}#{"qsub_args":"-q ms.q -l arch=lx24-amd64 -l h_stack=32M \
    #-l h_vmem=4G -l hostname=graf -v MKL_NUM_THREADS=1"}

    config["working_directory"] = "/working/henry_temp/keshavan/"
    config["output_directory"] = "/data/henry7/PBR/subjects"
    config["crash_directory"] = "/working/henry_temp/keshavan/crashes"
    config["mni_template"] = "/data/henry6/PBR/templates/OASIS-30_Atropos_template_in_MNI152.nii.gz"

    return config

if __name__ == '__main__':
    config = get_config()
    df = pd.read_csv("/data/henry7/james/antje_cohort/antje_transition_cohort.csv")
    msid_sorted = sorted(list(set(df['msid'])))
    print("msid scanned are :", msid_sorted, '\nThere are {} mse'.format(len(msid_sorted)))
    # print(df[['msid', 'mse']])

    t1_check = {}
    t1_check['missing'] = {}
    t1_check['more_than_one'] = {}
    t1_check['no_alignment'] = {}
    no_alignment = []

    for ms in msid_sorted:
        t1_check['missing'][ms] = []
        t1_check['more_than_one'][ms] = []
        t1_check['no_alignment'][ms] = []

    for index, row in df.iterrows():
        print(index, row['msid'], row['mse'])

        status_dir = os.path.join(config["output_directory"], row['mse'], 'alignment', 'status.json')
        try:
            status = load_json(status_dir)
        except:
            print("No alignment status.json file, please check that directory")
            t1_check['no_alignment'][row['msid']].append(row['mse'])
            no_alignment.append(row['msid'])

        if len(status['t1_files']) == 0:
            t1_check['missing'][row['msid']].append(row['mse'])
        elif len(status['t1_files']) > 1:
            t1_check['more_than_one'][row['msid']].append(row['mse'])

    for ms in msid_sorted:
        if t1_check['missing'].get(ms) == []:
            t1_check['missing'].pop(ms, None)
        if t1_check['more_than_one'].get(ms) == []:
            t1_check['more_than_one'].pop(ms, None)
        if t1_check['no_alignment'].get(ms) == []:
            t1_check['no_alignment'].pop(ms, None)

    outdir = '/data/henry7/james/antje_cohort'
    save_json(os.path.join(outdir, 'T1_status.json'), t1_check)

    msid_for_t2flair = list(set(msid_sorted) - set(no_alignment))
    print(msid_for_t2flair)
    t2flair_check = {}
    t2flair_check['missing'] = {}
    t2flair_check['more_than_one'] = {}

    for ms in msid_for_t2flair:
        t2flair_check['missing'][ms] = []
        t2flair_check['more_than_one'][ms] = []

    for index, row in df.iterrows():
        print(index, row['msid'], row['mse'])
        status_dir = os.path.join(config["output_directory"], row['mse'], 'alignment', 'status.json')
        if row['msid'] in msid_for_t2flair:
            status = load_json(status_dir)
        if len(status['flair_files']) == 0 and len(status['t2_files']) == 0:
            t2flair_check['missing'][row['msid']].append(row['mse'])
        elif len(status['flair_files']) > 1:
            t2flair_check['more_than_one'][row['msid']].append(row['mse'])
        elif len(status['flair_files']) == 0 and len(status['t2_files']) > 1:
            t2flair_check['more_than_one'][row['msid']].append(row['mse'])

    for ms in msid_sorted:
        if t2flair_check['missing'].get(ms) == []:
            t2flair_check['missing'].pop(ms, None)
        if t2flair_check['more_than_one'].get(ms) == []:
            t2flair_check['more_than_one'].pop(ms, None)

    save_json(os.path.join(outdir, 'T2_FLAIR_status.json'), t2flair_check)