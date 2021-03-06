#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import random
def getkeywords():
    with open('keywords.txt') as f:
        keywords = f.read().strip().split()
    return keywords
keywords = getkeywords()
keywords.append('otherwords')
def getScIndex(inputStr):
    flag = 0
    idx = []
    for i in range(len(keywords)-1):
        w = keywords[i]
        if w in inputStr:
            idx.append(str(i))
            flag += 1
    if flag == 0:
        idx.append(str(len(keywords)-1))
    return idx
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    T = [i for i in range(25)]
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))/3600.0-435112.0
    Hour = int(date[-8:-6])
    i = 0
    while Hour >= T[i] and i < len(T):
        i += 1
    Time = str(i-1)
    Hour = Hour/24.0
    return time_stamp,Time,'%0.2f'%Hour
ID = list('0123457')
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    userid = fields[0]
    action_history = fields[1]
    history_list = action_history.split('[->]')
    abs_time = -1
    Y = []
    X = []
    abs_time_last76 = -1
    for h in history_list:
        feature = []
        act = h.split('[&]')
        abs_time,timeIndex,hour = date_to_timestamp(act[0])
        feature.append(hour) #time 0-24 --> [0,1)
        feature.append(timeIndex) #time is split by [0,6,12,18,22,24]
        if len(X)==0:
            relative_time = 24.01  #
        if  abs_time_last76 == -1:
            relative_time = 24.01  #
        else:
            relative_time = abs_time - abs_time_last76
        feature.append(str(int(relative_time<24)))#time interval from last click
        sc_index = '#'.join(getScIndex(act[2]))
        feature.append(sc_index)# scene index
        feature.append(act[2]) # user input
        X.append(feature) #[hour,timeIndex,time-interval-lastclick,scene,userInput]
        if '76' in act[1]:
            Y.append('1')
        else:
            Y.append('0')
    for i in range(len(Y)):
        random.shuffle(ID)
        sessid = ''.join(ID)
        S = [sessid]+[userid]+X[i]+[Y[i]]
        S = '\t'.join(S)
        #if random.uniform(0,1)>0.5:
        sys.stdout.write("%s\n" % S)

