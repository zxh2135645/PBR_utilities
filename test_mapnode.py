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

    #config["plugin"] = "Linear"#"SGE"
    #config["plugin_args"] = {}#{"qsub_args":"-q ms.q -l arch=lx24-amd64 -l h_stack=32M \
    #-l h_vmem=4G -l hostname=graf -v MKL_NUM_THREADS=1"}

    config["working_directory"] = "/working/henry_temp/keshavan/"
    config["output_directory"] = "/data/henry7/PBR/subjects"
    config["crash_directory"] = "/working/henry_temp/keshavan/crashes"
    config["mni_template"] = "/data/henry6/PBR/templates/OASIS-30_Atropos_template_in_MNI152.nii.gz"
    return config

def check_length(moving_image, fixed_image):

    if len(moving_image) != 1 or len(fixed_image) != 1:
        if len(moving_image) >= len(fixed_image):
            new_fixed_image = []
            for i in range(len(fixed_image)):
                fixed_temp = [fixed_image[i]] * len(moving_image)
                new_fixed_image += fixed_temp
            new_moving_image = moving_image * len(fixed_image)
        elif len(fixed_image) > len(moving_image):
            new_moving_image = []
            for i in range(len(moving_image)):
                moving_temp = [moving_image[i]] * len(fixed_image)
                new_moving_image += moving_temp
            new_fixed_image = fixed_image * len(moving_image)
    else:
        new_fixed_image = fixed_image
        new_moving_image = moving_image

    return new_moving_image, new_fixed_image

def get_msid(name):
    msid = name.split("/")[-1].split('-')[0]
    return msid

def get_mseid(str1):
    mseid1 = str1.split("/")[-1].split('-')[1]
    # mseid2 = str2.split("/")[-1].split('-')[1]
    return mseid1



def get_seriesnum(list1):
    num1 = []
    for str1 in list1:
        num1.append(str1.split('/')[-1].split('-')[2])
    if len(num1) >= 2:
        return num1
    else:
        return ['']

def test_mapnode(config, moving_image, fixed_image):
    import nipype.interfaces.fsl as fsl
    from nipype.pipeline.engine import Node, Workflow, MapNode
    from nipype.interfaces.io import DataSink, DataGrabber
    from nipype.interfaces.utility import IdentityInterface, Function
    import os

    moving_mse = get_mseid(moving_image[0])
    fixed_mse = get_mseid(fixed_image[0])
    print(moving_mse, fixed_mse)
    seriesNum_moving = get_seriesnum(moving_image)
    seriesNum_fixed = get_seriesnum(fixed_image)
    print("seriesNum for moving and fixed are {}, {} respectively".format(seriesNum_moving, seriesNum_fixed))

    register = Workflow(name="test_mapnode")
    register.base_dir = config["working_directory"]
    inputnode = Node(IdentityInterface(fields=["moving_image", "fixed_image"]),
                     name="inputspec")
    inputnode.inputs.moving_image = moving_image
    inputnode.inputs.fixed_image = fixed_image

    check_len = Node(Function(input_names=["moving_image", "fixed_image"],
                              output_names=["new_moving_image", "new_fixed_image"], function=check_length),
                     name="check_len")
    register.connect(inputnode, 'moving_image', check_len, 'moving_image')
    register.connect(inputnode, 'fixed_image', check_len, 'fixed_image')

    flt_rigid = MapNode(fsl.FLIRT(), iterfield=['in_file', 'reference'], name="FLIRT_RIGID")
    flt_rigid.inputs.dof = 6
    flt_rigid.output_type = 'NIFTI_GZ'
    register.connect(check_len, 'new_moving_image', flt_rigid, 'in_file')
    register.connect(check_len, 'new_fixed_image', flt_rigid, 'reference')

    sinker = Node(DataSink(), name="DataSink")
    sinker.inputs.base_directory = '/data/henry7/james'
    sinker.inputs.container = 'test_mapnode'


    """
    def getsubs(moving_image, fixed_image, moving_mse, fixed_mse, seriesNum_moving, seriesNum_fixed):

        N = len(moving_image) * len(fixed_image)
        subs = []
        print("N is :" ,N)
        for i in range(N):
            for j in seriesNum_moving:
                seri_moving = ''
                if j != '':
                    seri_moving = '_' + j
                for k in seriesNum_fixed:
                    seri_fixed = ''
                    if k != '':
                        seri_fixed = '_' + k
                    subs += [('_FLIRT_RIGID%d'%i, moving_mse + seri_moving + '__' + fixed_mse + seri_fixed)]
        print("subs are: ", subs)
        return subs
    """

    def getsubs(moving_image, fixed_image, moving_mse, fixed_mse):
        N = len(moving_image) * len(fixed_image)
        subs = [('_flirt', '_trans')]
        if N == 1:
            subs += [('_FLIRT_RIGID%d'%0, moving_mse + '__' + fixed_mse)]
        else:
            for i in range(N):
                subs += [('_FLIRT_RIGID%d'%i, moving_mse + '__' + fixed_mse + '_' + str(i+1))]
        return subs

    get_subs = Node(Function(input_names=["moving_image", "fixed_image", "moving_mse", "fixed_mse"],
                             output_names=["subs"], function=getsubs),
                    name="get_subs")
    get_subs.inputs.moving_mse = moving_mse
    get_subs.inputs.fixed_mse = fixed_mse
    # get_subs.inputs.seriesNum_moving = seriesNum_moving
    # get_subs.inputs.seriesNum_fixed = seriesNum_fixed

    register.connect(inputnode, 'moving_image', get_subs, 'moving_image')
    register.connect(inputnode, 'fixed_image', get_subs, "fixed_image")
    register.connect(get_subs, 'subs', sinker, 'substitutions')
    register.connect(flt_rigid, 'out_file', sinker, '@mapnode_out')

    register.write_graph(graph2use='orig')
    register.config["Execution"] = {"keep_inputs": True, "remove_unnecessary_outputs": False}
    return register

if __name__ == '__main__':
    mse2703 = ['/data/henry7/PBR/subjects/mse2703/alignment/ms1470-mse2703-002-AX_T1_3D_IRSPGR.nii.gz']
    mse2704 = ['/data/henry7/PBR/subjects/mse2704/alignment/ms1470-mse2704-002-AX_T1_3D_IRSPGR.nii.gz',
               #'/data/henry7/PBR/subjects/mse2704/alignment/ms1470-mse2704-010-AX_T1_3D_IRSPGR.nii.gz'
               ]
    config = get_config()
    wf = test_mapnode(config, mse2703, mse2704)
    wf.run()


