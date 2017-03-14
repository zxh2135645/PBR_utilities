__author__ = 'sf713420'

#from itertools import tee
import os
import sys
from subprocess import run
import urllib.request
from siena_plotting import siena_plotting
#from nipype.interfaces.base import isdefined


print("Argument List:", str(sys.argv), "\n")

def retri(msid, mseid1, mseid2, seriesnum1='', seriesnum2='', bet_thresh=''):

    text_folder = os.path.join('/data/henry7/PBR/subjects/', msid, 'siena', 'PBVC'+bet_thresh+'.txt')
    text_file = open(text_folder, 'w+')

    for i in range(len(mseid1)):
        pathname = os.path.join('file:///data/henry7/PBR/subjects/', msid, 'siena', mseid1[i] + seriesnum1 + '__' + mseid2[i] + seriesnum2 + bet_thresh, 'report.html')
        #msid is str, mseid1 and mseid2 are list
        response = urllib.request.urlopen(pathname)
        #'file:///data/henry7/PBR/subjects/ms1244/siena/mse2439__mse3622/report.html'

        word = 'PBVC:'
        res_list = response.read().decode("utf-8").split()

        for word_count, line in enumerate(res_list):
            #Because this is 0-index based
            if word == line:
                break

        PBVC_pre = res_list[word_count + 1]
        PBVC = PBVC_pre.split('<')[0]
        print(word, PBVC)
        mseids = mseid1[i]+'__'+mseid2[i]

        text_file.write("{0} {1} \r\n".format(mseids, float(PBVC)))
    text_file.close()

def make_PairList(arg):
    f = open(arg)
    mse_str = f.read()
    #print(mse_str)

    mse_list = mse_str.split('\n')
    if mse_list[-1] == '':
        mse_list = mse_list[:-1]
    print("mse list is: ", mse_list, "\n")

    pair_list = []

    for i in range(len(mse_list) - 1):
        j = []
        j.append(mse_list[i])
        j.append(mse_list[i+1])
        pair_list.append(j)

    return pair_list

def get_msid(arg):
    # Input is /data/henry6/mindcontrol_ucsf_env/watchlists/long/VEO/ms*.txt
    msid = arg.split('/')[-1].split('.')[0]
    return msid

def get_mseidList(pair_list, n): # n = 0 or 1 corespond to mseid1 or mseid2
    mseid = []
    for ids in pair_list:
        mseid.append(ids[n])
    return mseid

if __name__ == '__main__':

    msid = sys.argv[1]
    print("msID is: ", msid,"\n")

    if sys.argv.__len__() == 3:
        bet_thresh = sys.argv[2]
        print("bet_thresh is: ", bet_thresh)

    PBVC_dir = os.path.join('/data/henry7/PBR/subjects', msid, 'pbr_siena')
    siena_plotting(PBVC_dir, msid)

