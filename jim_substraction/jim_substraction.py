__author__ = 'sf713420'

import os
#PACKAGE_PARENT = '..'
#SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from .utils import get_config, create_jim_workflow
from glob import glob
from nipype.utils.filemanip import split_filename, load_json, save_json


def create_status(config, msid, mseIDs):
    from os.path import join
    outputs = {}
    outputs["mseIDs"] = mseIDs
    outputs["fixed_corrected"] = sorted(glob(join(config["james_output_dir"], msid, 'substraction', 'mse*-mse*',                                                  '*_corrected.nii.gz')))
    outputs["substracted_header"] = sorted(glob(join(config["james_output_dir"], msid, 'substraction', 'mse*-mse*',
                                                     'fixed-warped.hdr')))
    outputs["substracted_img"] = sorted(glob(join(config["james_output_dir"], msid, 'substraction', 'mse*-mse*',
                                                     'fixed-warped.img')))

    return outputs


def run_workflow(msid):
    print("jim_substraction msID [-o <output directory>]")
    config = get_config()
    # msid = sys.argv[1]
    print("msID is: ", msid, "\n")

    """
    # This is not implemented so far
    #TODO
    if sys.argv.__len__() == 4:
        out_dir = sys.argv[3]
        print("Output directory is: ", out_dir)
    """

    status = load_json(os.path.join(config["output_directory"], msid, 't1Ants_reg_long', 'status.json'))
    fixed_list = status["fixed_image"]
    warped_list = status["warped_brain"]
    mseIDs = status["mseIDs"]

    if len(fixed_list) + 1 != len(mseIDs) or len(warped_list) + 1 != len(mseIDs):
        raise NotImplementedError("The script assuming the list is one dimension, please modify it")

    for i, fixed in enumerate(fixed_list):
        print(fixed, warped_list[i])
        wf = create_jim_workflow(config,
                                 fixed,
                                 warped_list[i])

        wf.config = {"execution": {"crashdump_dir": os.path.join(config["crash_directory"],
                                                                 os.path.split(fixed)[1][0:-7]
                                                                 + '-'
                                                                 + os.path.split(warped_list[i])[1][0:-7],
                                                                 'jim_substraction')}}
        wf.run()

    outputs = create_status(config, msid, mseIDs)
    save_json(os.path.join(config["james_output_dir"], msid, 'substraction', 'status.json'), outputs)