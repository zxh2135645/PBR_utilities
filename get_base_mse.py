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
    import pandas as pd
    import os
    from glob import glob
    from shutil import copyfile

    config = get_config()
    path_list = glob('/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/ms*.txt')
    ms_list = [ms.split('/')[-1].split('.')[0] for ms in path_list]
    status = pd.DataFrame()

    for msid in ms_list:
        mse_list = pd.read_table('/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/{0}.txt'.format(msid))
        mseid = mse_list[0]
        print(mse_list[0])
        for mse_idx, mse in enumerate(mseid):
            lst_edit_check = glob(os.path.join(config["output_directory"], mse, 'mindcontrol', '*FLAIR*',
                                           'lst', 'lst_edits', 'no_FP_filled_FN_dr2*'))
            if len(lst_edit_check) == 1:
                lesion_edit = ''.join(lst_edit_check)
                break
            elif len(lst_edit_check) > 1:
                raise ValueError("lst_edits files have more than one inputs, please check PBROUT directory",
                                 os.path.split(lst_edit_check[0]))
            elif len(lst_edit_check) == 0:
                raise ValueError("lst_edits files do not have edited lesion in the mindcontrol for msid:",
                                 "\n {0}".format(msid))
        status['msid'] = msid
        status['mse'] = mse

    status.to_csv('/data/henry7/james/antje_cohort/baseline_mse.csv')
