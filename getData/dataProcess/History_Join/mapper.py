#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
#[last_session_id,Time,userid,rc,'#'.join(AC),query,CI,iC,Post,F]
filepath = os.environ.get('mapreduce_map_input_file')
filename = os.path.split(filepath)[0].strip()
filelist = ['201910/0'+str(i) for i in range(10)]
filelist = filelist + ['201910/'+str(i) for i in range(10,21)]
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)!=2:
        continue
    idx = -1
    for i in range(len(filelist)):
        if filelist[i] in filename:
            idx = i
            break
    if idx==-1:
        continue
    S = data+'\t'+str(idx)
    sys.stdout.write("%s\n" % S)