__author__ = 'sf713420'

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

    config["working_directory"] = "/working/henry_temp/keshavan/"
    config["output_directory"] = "/data/henry7/PBR/subjects"
    config["crash_directory"] = "/working/henry_temp/keshavan/crashes"
    config["james_output_dir"] = "/data/henry7/james/subjects"

    return config

def run_algebra(var, formula, image1, image2, out_image):
    from subprocess import Popen, run, PIPE
    print("In algebra, the output image is: ", out_image)
    cmd = ['Algebra', '-v', var, formula, image1, image2, out_image]
    run(cmd)

    return out_image

def run_unicorr(inputImage, outputImage):
    from subprocess import run
    cmd = ['Unicorr', inputImage, outputImage]

    run(cmd)
    return outputImage

def get_msid(name):
    msid = name.split("/")[-4]
    return msid

def get_fixed_mseid(str1):
    mseid1 = str1.split("/")[-1].split('_')[0]
    return mseid1

def get_warped_mseid(str1):
    mseid1 = str1.split("/")[-2].split('__')[0]
    return mseid1

def create_jim_workflow(config, fixed, warped):
    """
    Inputs::

        config: Dictionary with PBR configuration options. See config.py
        fixed: full path of t1 image from fixed image
        warped: full path of t1 image from warped image

    Outputs::

        nipype.pipeline.engine.Workflow object

    """

    import nipype.interfaces.ants as ants
    from nipype.pipeline.engine import Node, Workflow, MapNode
    from nipype.interfaces.io import DataSink, DataGrabber
    from nipype.interfaces.utility import IdentityInterface, Function
    import nipype.interfaces.fsl as fsl
    from nipype.utils.filemanip import load_json
    import os
    from nipype.caching import Memory

    mse_tp1 = get_warped_mseid(warped)
    mse_tp2 = get_fixed_mseid(fixed)
    msid = get_msid(fixed)
    Jim_node = "Jim_substract_{0}_{1}-{2}".format(msid, mse_tp2, mse_tp1)
    register = Workflow(name=Jim_node)
    register.base_dir = config["working_directory"]
    inputnode = Node(IdentityInterface(fields=["fixed_image", "moving_image"]),
                     name="inputspec")
    inputnode.inputs.moving_image = warped
    inputnode.inputs.fixed_image = fixed

    unicorr = Node(Function(input_names=['inputImage', 'outputImage'], output_names=['uni_output'],
                            function=run_unicorr), name='Unicorr')
    unicorr.inputs.outputImage = os.path.join(config["working_directory"], Jim_node, 'Unicorr',
                                              os.path.split(fixed)[1].split('.')[0] + '_corrected.nii.gz')
    register.connect(inputnode, 'fixed_image', unicorr, 'inputImage')

    substract = Node(Function(input_names=['var', 'formula', 'image1', 'image2', 'out_image'],
                              output_names=['sub_output'], function=run_algebra), name='Algebra')
    substract.inputs.out_image = os.path.join(config["working_directory"], Jim_node, 'Algebra',
                                              'fixed-warped.hdr')
    substract.inputs.var = "I1,I2"
    substract.inputs.formula = "I1-I2"
    register.connect(unicorr, 'uni_output', substract, 'image1')
    register.connect(inputnode, 'moving_image', substract, 'image2')

    sinker = Node(DataSink(), name="sinker")
    sinker.inputs.base_directory = os.path.join(config["james_output_dir"], msid, 'affine_substraction')
    sinker.inputs.container = mse_tp2 + '-' + mse_tp1

    register.connect(unicorr, 'uni_output', sinker, '@corrected')
    register.connect(substract, 'sub_output', sinker, '@substracted')

    register.write_graph(graph2use='orig')
    register.config["Execution"] = {"keep_inputs": True, "remove_unnecessary_outputs": False}

    #Memory.clear_previous_runs(register, warn=True)
    return register
"""
if __name__ == '__main__':

    out_image = run_algebra('I1,I2', 'I1-I2',
                            '/data/henry7/james/Jim6/pbr_test/mse2442_T1_corrected.nii.gz',
                            '/data/henry7/james/Jim6/pbr_test/output_warped_image.nii.gz',
                            '/data/henry7/james/Jim6/pbr_test/pbr_substraction')
    print(out_image)
"""