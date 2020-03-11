#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
def getkeywords():
    with open('keywords.txt') as f:
        keywords = f.read().strip().split()
    return keywords
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    #T = [0,6,12,18,22,24]
    T = [i for i in range(25)]
    Hour = int(date[-8:-6])
    i = 0
    while Hour >= T[i] and i < len(T):
        i += 1
    Time = i-1
    return Time
T = [str(i) for i in range(24)]
#T = ['0-6','6-12','12-18','18-22','22-24']
Num_ac1 = 0
Num_ac76 = 0
keywords = getkeywords()
keywords.append('otherwords')
D_sc_ac1 = {d:0 for d in keywords}
D_sc_ac76 = {d:0 for d in keywords}
D_time_ac1 = {d:0 for d in T}
D_time_ac76 = {d:0 for d in T}
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    sessid = fields[0]
    action_history = fields[1]
    history_list = action_history.split('[->]')
    for h in history_list:
        act = h.split('[&]')
        timeIndex = date_to_timestamp(act[0])
        Num_ac1 += 1
        D_time_ac1[T[timeIndex]] += 1
        flag = 0
        for w in keywords:
            if w in act[2]:
                flag += 1
                D_sc_ac1[w] += 1
                if '76' in act[1]:
                    D_sc_ac76[w] += 1
        if flag==0:
            D_sc_ac1['otherwords'] += 1
            if '76' in act[1]:
                D_sc_ac76['otherwords'] += 1
        if '76' in act[1]:
            Num_ac76 += 1
            D_time_ac76[T[timeIndex]] += 1
S = 'Number_ac=1&ac=76\t'
S += str(Num_ac1)
S += '\t'
S += str(Num_ac76)
sys.stdout.write("%s\n" % S)

S = 'scene\t'
S += '\t'.join([keywords[i] for i in range(len(keywords))])
S += '\n'
S += 'num_scene_ac1\t'
S += '\t'.join([str(D_sc_ac1[keywords[i]]) for i in range(len(keywords))])
S += '\n'
S += 'num_scene_ac76\t'
S += '\t'.join([str(D_sc_ac76[keywords[i]]) for i in range(len(keywords))])
sys.stdout.write("%s\n" % S)

S = 'time\t'
S += '\t'.join([T[i] for i in range(len(T))])
S += '\n'
S += 'num_time_ac1\t'
S += '\t'.join([str(D_time_ac1[T[i]]) for i in range(len(T))])
S += '\n'
S += 'num_time_ac76\t'
S += '\t'.join([str(D_time_ac76[T[i]]) for i in range(len(T))])
sys.stdout.write("%s\n" % S)
