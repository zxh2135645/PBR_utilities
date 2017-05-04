#! /usr/bin/env python
__author__ = 'sf713420'

from glob import glob
from os.path import split, join
import os
from subprocess import Popen, run, PIPE

def get_collection(port=3001):
    from pymongo import MongoClient
    client = MongoClient("localhost", port)
    db =  client.meteor
    collection = db.subjects
    return collection, client

def check_before_edit_lst(mse, outdir, meteor_port, entry_types=None, type_of_img="alignment"):
    coll, cli = get_collection(meteor_port+1)
    finder = {"subject_id": mse}
    if entry_types is not None:
        finder["entry_type"] = {"$in": entry_types}
    entries = coll.find(finder)
    for entry in entries:
        print(entry)
        if "name" in entry.keys():
            name = entry["name"]
            print("name is:", name)

    folders = [split(q)[1] for q in glob(join(outdir, mse, "*"))]
    ratio_file = join(outdir, mse, type_of_img, name + ".nii.gz")
    assert os.path.exists(ratio_file), "{} file does not exist {}".format(type_of_img, ratio_file)

    if "antsCT" not in folders:
        print("There is no antsCT folder in /data/henry7/PBR/subjects/{0}"
              "\n pbr {0} -w ants -R will be run".format(mse))
        cmd = ['pbr', mse, '-w', 'ants', '-R']
        proc = Popen(cmd)
        proc.wait()
    if "lst" not in folders:
        print("There is no lst folder in /data/henry7/PBR/subjects/{0}"
        "\n pbr {0} -w lst -R will be run".format(mse))
        cmd = ['pbr', mse, '-w', 'lst', '-R']
        proc = Popen(cmd)
        proc.wait()

    return name

if __name__ == '__main__':
    outdir = '/data/henry7/PBR/subjects'
    name = check_before_edit_lst('mse3670', outdir, 5050, entry_types=["transform"])

