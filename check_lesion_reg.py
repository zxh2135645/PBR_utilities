#! /usr/bin/env python
__author__ = 'sf713420'

from glob import glob
from os.path import split, join
import os
from subprocess import Popen, run, PIPE
from pbr.config import config as cc

def get_collection(port=3001):
    from pymongo import MongoClient
    client = MongoClient("localhost", port)
    db =  client.meteor
    collection = db.subjects
    return collection, client

def get_descrip_name(mse, meteor_port, entry_types=None):
    coll, cli = get_collection(meteor_port+1)
    finder = {"subject_id": mse}
    if entry_types is not None:
        finder["entry_type"] = {"$in": entry_types}
    entries = coll.find(finder)
    name = ''
    saved = []
    for entry in entries:
        print(entry)
        if "name" in entry.keys():
            name = entry["name"]
            print("name is:", name)
            if "loggedPoints" not in entry.keys() and "checkedBy" in entry.keys():
                saved.append("checked")
            elif "loggedPoints" in entry.keys():
                saved.append("logged")
            else:
                saved.append("unrun")
    return name, saved


def check_before_edit_lst(mse, outdir, meteor_port, entry_types=None, type_of_img="alignment"):
    name, saved = get_descrip_name(mse, meteor_port, entry_types)
    if name == '':
        raise ValueError("name is empty!")

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

    return 1

def edit_lst(mse, entry_types):
    # name, saved = check_before_edit_lst(mse, outdir, meteor_port, entry_types)
    for entry in entry_types:
        cmd = ['edit_lst.py', '-e', entry, mse]
        proc=Popen(cmd)
        proc.wait() # TODO
    return 1

def check_after_edit_lesion(mse_tp1, mse_tp2, outdir, meteor_port, entry_types):
    import warnings
    from shutil import copyfile
    # After edit_lst, check if there is no_FP_filled_FN_dr2* generated
    if outdir != cc["output_directory"]:
        warnings.warn("The outdir is not PBROUT directory, please be careful")
    name, saved = get_descrip_name(mse_tp1, meteor_port, entry_types)
    for entry in entry_types:
        if "logged" in saved:
            prev_lesion = join(outdir, mse_tp1, "mindcontrol", name, entry, "lst_edits",
                               "no_FP_filled_FN_dr2_{}.nii.gz".format(name))
            dst_file = join(outdir, mse_tp2, "transforms", "prev_lesion.nii.gz")
            copyfile(prev_lesion, dst_file)
        elif "checked" in saved:
            print("The previous timepoint lesions were checked in the mindcontrol, \n"
                  "and there was no need to edit it")
        elif "unrun" in saved:
            raise AttributeError("edit_lst.py was not run for {}, please run it".format(mse_tp1))

    return 1

def run_pbr_apply_transform(mse_tp2):
    cmd = ['pbr', mse_tp2, '-w', 'transform', '-R']
    proc = Popen(cmd)
    proc.wait()
    return 1

def mc_up(mse_tp2):
    cmd = ['mc_up', '-e', 'production', '-s', mse_tp2]
    proc = Popen(cmd)
    proc.wait()
    return 1

def email_to(to, subject, message):
    # to is string
    import smtplib

    # Gmail Sign In
    gmail_sender = 'sender@gmail.com'
    gmail_passwd = 'password'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % to,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % subject,
                    '', message])

    try:
        server.sendmail(gmail_sender, [to], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()
    return 1

if __name__ == '__main__':
    import argparse
    import pandas as pd
    parser = argparse.ArgumentParser()
    parser.add_argument('msid', nargs="+")
    args = parser.parse_args()
    msid = args.msid
    outdir = cc["output_directory"]
    #outdir should be PBROUT

    for ms in msid:
        text_file = '/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/{}.txt'.format(ms)
        fread = pd.read_table(text_file,
                                 header=None)
        f_reversed = fread.iloc[::-1]
        mse_reversed = list(f_reversed[0])
        for i in range(len(mse_reversed)):
            name = check_before_edit_lst('mse3670', outdir, 5050, entry_types=["transform"])

