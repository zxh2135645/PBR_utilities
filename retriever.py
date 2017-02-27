#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 01:46:26 2017

@author: sf713420
"""

import urllib.request
import os
from nipype.interfaces.base import isdefined


def retri(msid, mseid1, mseid2, bet_thresh): #pathname is
    if not isdefined(bet_thresh):
        bet_thresh = ''
    for i in range(len(mseid1)):
        pathname = os.path.join('file:///data/henry7/PBR/subjects/', msid, 'siena', mseid1[i]+'__'+mseid2[i]+bet_thresh, 'report.html')
        #msid is str, mseid1 and mseid2 are list
        response = urllib.request.urlopen(pathname)
        #'file:///data/henry7/PBR/subjects/ms1244/siena/mse2439__mse3622/report.html'

        word = 'PBVC:'
        res_list = response.read().decode("utf-8").split()
        #print(res_list)
        #if word in res_list:
        #    print(word) 

        for word_count, line in enumerate(res_list):
            #Because this is 0-index based
            if word == line:
                break
    
        PBVC_pre = res_list[word_count + 1]
        PBVC = PBVC_pre.split('<')[0] 
        print(word, PBVC)    
    
        text_folder = os.path.join('/data/henry7/PBR/subjects/', msid, 'siena', 'PBVC.txt'+bet_thresh)
        text_file = open(text_folder, 'w+')
        mseids = mseid1[i]+'__'+mseid2[i]
        text_file.write("{0} {1} \r\n".format(mseids, float(PBVC)))
    text_file.close()
    
    
    