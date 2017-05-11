__author__ = 'sf713420'
import sys
import pandas as pd
from glob import glob
import os

def index_lesion_workflow(msid, mseid, lesion):
    import nipype.interfaces.ants as ants
    from nipype.pipeline.engine import Node, Workflow, MapNode
    from nipype.interfaces.io import DataSink, DataGrabber
    from nipype.interfaces.utility import IdentityInterface, Function
    import nipype.interfaces.fsl as fsl
    from nipype.utils.filemanip import load_json

    working_directory = '/working/henry_temp/keshavan/'
    output_directory = os.path.split(lesion)[0]

    register = Workflow(name="indexed_lesion_{0}_{1}".format(msid, mseid))
    register.base_dir = working_directory
    inputnode = Node(IdentityInterface(fields=["lesion"]),
                     name="inputspec")
    inputnode.inputs.lesion = lesion

    bin_math = Node(fsl.BinaryMaths(), name="Convert_to_binary")
    bin_math.inputs.operand_value = 1
    bin_math.inputs.operation = 'min'
    register.connect(inputnode, "lesion", bin_math, "in_file")

    cluster_lesion = Node(fsl.Cluster(threshold=0.0001,
                                      out_index_file = True,
                                      use_mm=True),
                       name="cluster_lesion")

    sinker = Node(DataSink(), name="sinker")
    sinker.inputs.base_directory = output_directory
    sinker.inputs.container = '.'
    sinker.inputs.substitutions = [('_maths', '')]

    register.connect(bin_math, "out_file", cluster_lesion, "in_file")
    register.connect(cluster_lesion, "index_file", sinker, "@cluster")

    from nipype.interfaces.freesurfer import SegStats
    segstats_lesion = Node(SegStats(), name="segstats_lesion")
    register.connect(cluster_lesion, "index_file", segstats_lesion, "segmentation_file")
    register.connect(segstats_lesion, "summary_file", sinker, "@summaryfile")

    register.write_graph(graph2use = 'orig')
    register.config["Execution"] = {"keep_inputs": True, "remove_unnecessary_outputs": False}
    return register

if __name__ == '__main__':
    """python index_lesion.py

    Description::
        This code is taking antje's cohort and making indexed cluster of lesion masks
    """
    in_csv = pd.read_csv('/data/henry7/james/antje_cohort/antje_transition_cohort.csv')
    file_list = []
    for idx, mse in enumerate(in_csv["mse"]):
        fname = glob(os.path.join('/data/henry7/PBR/subjects/', mse, 't1_lst_lesions',
                                  '{0}-{1}_thr50.nii.gz'.format(in_csv["msid"][idx], mse)))
        if len(fname) == 1:
            fname = ''.join(fname)
            print(fname)
            file_list.append(fname)
        elif len(fname) > 1:
            raise ValueError("more than one file was found, please check: ", mse)

    print(file_list)

    for lesion in file_list:
        msid = os.path.split(lesion)[1].split('-')[0]
        mseid = os.path.split(lesion)[1].split('-')[1].split('_')[0]

        wf = index_lesion_workflow(msid, mseid, lesion)
        wf.config = {"execution": {"crashdump_dir": os.path.join("/working/henry_temp/keshavan/crashes",
                                                                 "jim_substraction_{}_{}".format(msid, mseid))}}
        wf.run()