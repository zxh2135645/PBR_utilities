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
    df = df[df.scanner != 'qb3-3t (3T)']
    #print(df)

    outdir = os.path.join('/data/henry7/james/antje_cohort/no_qb3_antje_transition_cohort.csv')
    df.to_csv(outdir, index=False)

    df2 = pd.read_csv("/data/henry7/james/antje_cohort/antje_transition_cohort.csv")
    df2 = df2[df2.scanner == 'qb3-3t (3T)']

    outdir2 = os.path.join('/data/henry7/james/antje_cohort/qb3_antje_transition_cohort.csv')
    df2.to_csv(outdir2, index=False)