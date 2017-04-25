__author__ = 'sf713420'

from .utils import get_msid, get_config, get_mseid, create_jim_workflow
from glob import glob
import os
from nipype.utils.filemanip import split_filename, load_json, save_json
import sys

def create_status(msid, mseIDs):
    from os.path import join
    outputs = {}
    outputs["mseIDs"] = mseIDs
    outputs["fixed_corrected"] = sorted(glob(join(config["james_output_dir"], msid, 'substraction', 'mse*-mse*',                                                  '*_corrected.nii.gz')))
    outputs["substracted_image"] = sorted(glob(join(config["james_output_dir"], msid, 'substraction', 'mse*-mse*',
'fixed-warped.nii.gz')))

    return outputs



if __name__ =='__main__':
    print("jim_substraction msID [-o <output directory>]")
    config = get_config()
    msid = sys.argv[1]
    print("msID is: ", msid, "\n")

    # This is not implemented so far
    #TODO
    if sys.argv.__len__() == 4:
        out_dir = sys.argv[3]
        print("Output directory is: ", out_dir)

    status = load_json(os.path.join(config["output_directory"], msid, 't1Ants_reg_long', 'status.json'))
    fixed_list = status["fixed_image"]
    warped_list = status["warped_brain"]
    mseIDs = status["mseIDs"]

    if len(fixed_list) + 1 != len(mseIDs) or len(warped_list) + 1 != len(mseIDs):
        raise NotImplementedError("The script assuming the list is one dimension, please modify it")

    for i, fixed in enumerate(fixed_list):
        wf = create_jim_workflow(config,
                                 fixed,
                                 warped_list[i])

        wf.config = {"execution": {"crashdump_dir": os.path.join(config["crash_directory"],
                                                                 os.path.split(fixed)[1][0:-7]
                                                                 + '-'
                                                                 + os.path.split(warped_list[i])[1][0:-7],
                                                                 + 'jim_substraction')}}
        wf.run()

    outputs = create_status(msid, mseIDs)
    save_json(os.path.join(config["james_output_dir"], msid, 'substraction', 'status.json'), outputs)