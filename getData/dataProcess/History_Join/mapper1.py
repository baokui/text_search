#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
#[last_session_id,Time,userid,rc,'#'.join(AC),query,CI,iC,Post,F]
filepath = os.environ.get('mapreduce_map_input_file')
filename = os.path.split(filepath)[0].strip()
idx = filename.find('userhistory_godText/user_')+len('userhistory_godText/user_')+2
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)!=2:
        continue
    try:
        day = filename[idx:idx+9]
        S = data+'\t'+day
        sys.stdout.write("%s\n" % S)
    except:
        continue