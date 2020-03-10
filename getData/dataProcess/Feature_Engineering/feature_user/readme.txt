reducer:
#time split:[0-6,6-12,12-18,18-22,22-24]
time_stamp = int(time.mktime(time_array))/3600.0-435112.0 #按小时记，减去2019-08-22 00:00:00对应的时间

import sys
import numpy as np
import time
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    T = [0,6,12,18,22,24]
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))/3600.0-435112.0
    Hour = int(date[-8:-6])
    i = 0
    while Hour >= T[i] and i < len(T):
        i += 1
    Time = str(i-1)
    return str(time_stamp),Time
random_bin = [i/20.0 for i in range(21)]
group = 'abcdefghigklmnopqrst'
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    sessid = fields[0]
    action_history = fields[1]
    history_list = action_history.split('[->]')
    try:
        for h in history_list:
            x = np.random.uniform()
            i = 0
            while x>=random_bin[i] and i<len(random_bin):
                i+=1
            Id=group[i-1]
            t, ac, query, sc = h.split('[&]')
            t0,t1 = date_to_timestamp(t)
            S = [Id,sessid,t0,t1,ac,query,sc]
            S = '\t'.join(S)
            sys.stdout.write("%s\n" % S)
    except:
        continue


#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import random
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    T = [0,6,12,18,22,24]
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))/3600.0-435112.0
    Hour = int(date[-8:-6])
    i = 0
    while Hour >= T[i] and i < len(T):
        i += 1
    Time = str(i-1)
    return str(time_stamp),Time
random_bin = [i/20.0 for i in range(21)]
group = 'abcdefghigklmnopqrst'
#按小时记，减去2019-08-22 00:00:00对应的时间
L = ['阿布']
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    sessid = fields[0]
    action_history = fields[1]
    history_list = action_history.split('[->]')
    for h in history_list:
        i = random.randint(0,len(group)-1)
        Id=group[i]
        t, ac, query, sc = h.split('[&]')
        t0,t1 = date_to_timestamp(t)
        S = [Id,sessid,t0,t1,ac,query,sc]
        S = '\t'.join(S)
        sys.stdout.write("%s\n" % S)