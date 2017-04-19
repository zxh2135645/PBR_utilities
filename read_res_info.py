__author__ = 'sf713420'

import os
import signal
from subprocess import Popen, PIPE
import sys
from nipype.utils.filemanip import load_json


def convert_to_coordinate(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    cmd = ['fslhd', '/data/henry7/PBR/subjects/mse5466/alignment/ms1244-mse5466-040-MPRAGE_64channel_p2.nii.gz']
    proc = Popen(cmd, stdout=PIPE)
    dim_lines = [l.decode("utf-8").split() for l in proc.stdout.readlines()[5:8]]

    x_pix_fov = int(dim_lines[0][1])
    y_pix_fov = int(dim_lines[1][1])
    z_pix_fov = int(dim_lines[2][1])
    #print(x_pix_fov,y_pix_fov,z_pix_fov)

    proc = Popen(cmd, stdout=PIPE)
    res_lines = [l.decode("utf-8").split() for l in proc.stdout.readlines()[18:21]]
    x_res = float(res_lines[0][1])
    y_res = float(res_lines[1][1])
    z_res = float(res_lines[2][1])
    #print(x_res, y_res, z_res)

    z_new = z # The slice don't change

    x_new = (x - x_pix_fov/2) * x_res
    y_new = (y_pix_fov/2 - y) * y_res

    return [x_new, y_new, z_new]

if __name__ == '__main__':
    working_dir = '/data/henry7/james/Jim6'
    centroids = load_json(os.path.join(working_dir, 'mse5466_centroids.json'))['reference']['present']
    new_coord = []
    with open(os.path.join(working_dir, 'mse5466_write.roi'), 'w') as f:
        for key, value in centroids.items():
            print(key, value)
            new_xyz = convert_to_coordinate(value)
            new_coord.append(new_xyz)
            f.writelines(["Begin Marker ROI\n",
                          "  Slice={}\n".format(new_xyz[2]),
                          "  Begin Shape\n",
                          "    X={0}; Y={1}\n".format(new_xyz[0], new_xyz[1]),
                          "  End Shape\n",
                          "End Marker ROI\n"])

    print(new_coord)




