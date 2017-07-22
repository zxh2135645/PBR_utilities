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


def check_before_mc_up(mse, outdir, meteor_port, entry_types=None, type_of_img="alignment", lesion_mse=None):
    name, saved = get_descrip_name(mse, meteor_port, entry_types)
    if name == '':
        raise ValueError("name is empty!")

    folders = [split(q)[1] for q in glob(join(outdir, mse, "*"))]
    ratio_file = join(outdir, mse, type_of_img, name + ".nii.gz")
    assert os.path.exists(ratio_file), "{} file does not exist {}".format(type_of_img, ratio_file)

    if mse == lesion_mse:
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

        if "lesion_reg" not in folders:
            print("There is no lesion_reg folder in /data/henry7/PBR/subjects/{0}"
                  "\n pbr {0} -w ants -R will be run".format(mse))
            cmd = ['pbr', mse, '-w', 'transform', '-R']
            proc = Popen(cmd)
            proc.wait()
    else:
        if "lesion_reg" not in folders:
            print("There is no lesion_reg folder in /data/henry7/PBR/subjects/{0}"
                  "\n pbr {0} -w ants -R will be run".format(mse))
            cmd = ['pbr', mse, '-w', 'transform', '-R']
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
            print("Copying file from {0} to {1}".format(prev_lesion, dst_file))
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

def get_msid(mseid):
    from nipype.utils.filemanip import load_json
    status = load_json(os.path.join(cc["output_directory"], mseid, 'alignment', 'status.json'))
    t1_files = status["t1_files"]
    if len(t1_files) == 0:
        raise ValueError("No T1 file is found.")
    elif len(t1_files) == 1:
        t1_file = ''.join(t1_files)
    else:
        t1_file = t1_files[0]

    msid = t1_file.split("/")[-1].split("-")[0]
    return msid

def get_mseid(msid, mse_reversed, lesion_mse):
    from subprocess import call
    lesion_idx = mse_reversed.index(lesion_mse)
    print("lesion_idx is:", lesion_idx)
    mse_list1 = mse_reversed[lesion_idx:]
    print("mse_list1 is:", mse_list1)
    mse_list2_bc = mse_reversed[:lesion_idx]
    mse_list2_bc.reverse()
    mse_list2 = mse_list2_bc
    print("mse_list2 is:", mse_list2)
    mse_tp1 = ''
    mse_tp2 = ''
    # Exclude the lesion_mse

    check_tlc = glob(os.path.join(cc["output_directory"], lesion_mse, 'tlc', 'status.json'))
    if len(check_tlc) == 0:
        print("No T1 lesions found in tlc folder, running pbr first...")
        cmd = ['pbr', lesion_mse, '-w', 'tlc', '-R']
        call(cmd)

    print("searching for lesion_reg folder for registered lesions.")
    for mse_idx, mse in enumerate(mse_list1):
        check_lesion_reg = glob(os.path.join(cc["output_directory"], mse, 'lesion_reg', 'status.json'))
        if mse != lesion_mse:
            if len(check_lesion_reg) == 0:
                mse_tp1 = mse_list1[mse_idx-1]
                mse_tp2 = mse_list1[mse_idx]
                break
    if mse_tp1 is '' and mse_tp2 is '' and len(mse_list2) != 0:
        for mse_idx, mse in enumerate(mse_list2):
            check_lesion_reg = glob(os.path.join(cc["output_directory"], mse, 'lesion_reg', 'status.json'))
            if mse != lesion_mse:
                if len(check_lesion_reg) == 0:
                    mse_tp1 = mse_list2[mse_idx-1]
                    mse_tp2 = mse_list2[mse_idx]
                    break
    if mse_tp1 is '' and mse_tp2 is '':
        print("Congratulations! You finished this subject: ", msid)
        # To add this info to a csv file
    return mse_tp1, mse_tp2


if __name__ == '__main__':
    import argparse
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument('msid', nargs="+")
    args = parser.parse_args()
    msid = args.msid
    outdir = cc["output_directory"]
    print("msid is:", msid)


    #outdir should be PBROUT

    for ms in msid:
        text_file = '/data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/test/{}.txt'.format(ms)
        fread = pd.read_table(text_file,
                                 header=None)
        f_reversed = fread.iloc[::-1]
        mse_reversed = list(f_reversed[0])
        print("mse list is:", mse_reversed)
        for mse_idx, mse in enumerate(mse_reversed):
            lst_edit_check = glob(os.path.join(outdir, mse, 'mindcontrol', '*FLAIR*',
                                               'lst', 'lst_edits', 'no_FP_filled_FN_dr2*'))
            if len(lst_edit_check) == 1:
                lesion_edit = ''.join(lst_edit_check)
                break
            elif len(lst_edit_check) > 1:
                raise ValueError("lst_edits files have more than one inputs, please check PBROUT directory",
                                 os.path.split(lst_edit_check[0]))

        try:
            print("The path of lsf lesion folder is:", lesion_edit)
            print("The lesion lst mse is:", mse)
        except NameError:
            print("The edited FLAIR lesion is not found in any timepoints, please check the corresponding directory.")
        mse_tp1, mse_tp2 = get_mseid(ms, mse_reversed, mse)
        if mse_tp1 is not '' and mse_tp2 is not '':
            if mse_tp1 == mse:
                check_after_edit_lesion(mse_tp1, mse_tp2, outdir, 5050, entry_types=["transform"])
                run_pbr_apply_transform(mse_tp2)
                check_before_mc_up(mse_tp2, outdir, 5050, entry_types=["transform"], lesion_mse=mse)
                mc_up(mse_tp2)
                print("Done!")
            else:
                check_after_edit_lesion(mse_tp1, mse_tp2, outdir, 5050, entry_types=["transform"])
                run_pbr_apply_transform(mse_tp2)
                check_before_mc_up(mse_tp2, outdir, 5050, entry_types=["transform"], lesion_mse=mse)
                mc_up(mse_tp2)
                print("Done!")
        else:
            print("Either mse_tp1 or mse_tp2 is empty, or both of them are empty:", mse_tp1, mse_tp2)




"""
            idx = mse_reversed.index(mseid)
            len_mse_list = len(mse_reversed)
            if mse != mseid:
                if idx == len_mse_list - 1:
                    print("Now it's transforming the base timepoint to the later timepoint")
                    mse_tp1 = mse
                    mse_tp2 = mse_reversed[mse_reversed.index(mseid) + 1]

                elif idx == 0:
                    print("Congrats! You finished running this subjects: ", msid)
                    break
                else:
                    if idx < mse_idx:
                        mse_tp1 = mseid
                        mse_tp2 = mse_reversed[mse_reversed.index(mseid) - 1]
                    elif idx > mse_idx:
                        mse_tp1 = mseid
                        mse_tp2 = mse_reversed[mse_reversed.index(mseid) + 1]
            else:
                print("This is the base timepoint. It's gonna apply to previous time point first")
"""




