__author__ = 'sf713420'

import os
from glob import glob
import pandas as pd
from nipype.utils.filemanip import save_json

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
    df = pd.read_csv("/home/sf522915/antje_transition_cohort.csv")
    msid_set = set(df['msid'])
    msid_set_sorted = sorted(list(msid_set))
    print("msid scanned are :", msid_set_sorted)

    mse_text_list = ['/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/{}.txt'.format(msid)
                for msid in msid_set_sorted]
    print(mse_text_list)
    check = {}
    check['exist'] = {}
    check['miss'] = []
    check['more_than_one'] = {}
    exist_list = []
    more_than_one_list = []

    for f in mse_text_list:
        fread = pd.read_table(f, header=None)
        f_reversed = fread.iloc[::-1]
        msid = f.split('/')[-1].split('.')[0]
        check['more_than_one'][msid] = []

        for mse_idx, mse in enumerate(f_reversed[0]):
            lst_edit_check = glob(os.path.join(config["output_directory"], mse, 'mindcontrol', '*FLAIR*',
                                                      'lst', 'lst_edits', 'no_FP_filled_FN_dr2*'))
            if len(lst_edit_check) == 1:
                print("One lst edits of {0} is found in {1} ". format(msid, mse))
                check['exist'][msid] = mse
                exist_list.append(msid)
                break
            elif len(lst_edit_check) > 1:
                print("More than one lst edits file were found in {}". format(msid))

                more_than_one_list.append(msid)
                for lesion_fname in lst_edit_check:
                    check['more_than_one'][msid].append(lesion_fname.split('/')[5])

                # raise ValueError("lst_edits files have more than one inputs, please check PBROUT directory",
                #                  os.path.split(lst_edit_check[0])[0])

    print(exist_list)
    print(more_than_one_list)

    print("For ms patients that only have more than one lst_edits: ",
          set(more_than_one_list) - (set(exist_list) & set(more_than_one_list)))

    print("For ms patients that found both multiple lst_edits and single lst_edits in different mse: ",
          set(exist_list) & set(more_than_one_list))

    only_one = list(set(exist_list) - (set(exist_list) & set(more_than_one_list)))
    print("For patients that found has only one lst_edits: ", only_one)

    miss_list = list(msid_set - (set(exist_list) | set(more_than_one_list)))
    print("For ms patients that missing mindcontrol lst_edits: ", miss_list)
    check['miss'] = miss_list

    for msid in msid_set_sorted:
        if check['more_than_one'].get(msid) == []:
            check['more_than_one'].pop(msid, None)

    outdir = '/data/henry7/james/antje_cohort'
    save_json(os.path.join(outdir, 'lst_status.json'), check)



