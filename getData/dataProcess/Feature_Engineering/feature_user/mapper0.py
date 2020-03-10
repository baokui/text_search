#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import random
def getSc():
    with open('table-trigger.txt') as f:
        S = [w.strip() for w in f]
    S = [a.split('\t') for a in S]
    L0 = [a[1] for a in S]
    L0 = list(set(L0))
    D_tr2sr = {a[0]:a[1] for a in S}
    with open('table-search-caption.txt') as f:
        L1 = [w.strip() for w in f]
    L1 += ['others']
    return L0,L1,D_tr2sr
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
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    userid = fields[0]
    action_history = fields[1]
    history_list = action_history.split('[->]')
    L0, L1, D_tr2sr = getSc()
    D_sc_ac1 = {d: 0 for d in L0}
    D_sc_ac76 = {d: 0 for d in L0}
    D_sc_ac1_cap = {'caption-' + d: 0 for d in L1}
    D_sc_ac76_cap = {'caption-' + d: 0 for d in L1}
    L = L0 + ['caption-' + d for d in L1]
    Num_ac1 = 0
    Num_ac76 = 0
    D_time_ac1 = {d: 0 for d in T}
    D_time_ac76 = {d: 0 for d in T}
    for h in history_list:
        act = h.split('[&]')
        timeIndex = date_to_timestamp(act[0])
        Num_ac1 += 1
        D_time_ac1[T[timeIndex]] += 1
        if act[2] in D_tr2sr:
            D_sc_ac1[D_tr2sr[act[2]]] += 1
            if '76' in act[1]:
                Num_ac76 += 1
                D_time_ac76[T[timeIndex]] += 1
                D_sc_ac76[D_tr2sr[act[2]]] += 1
        else:
            idx_sc = -1
            for i in range(len(L1)):
                if L1[i] in act[2]:
                    idx_sc = i
                    break
            D_sc_ac1_cap['caption-' + L1[idx_sc]] += 1
            if '76' in act[1]:
                Num_ac76 += 1
                D_time_ac76[T[timeIndex]] += 1
                D_sc_ac76_cap['caption-' + L1[idx_sc]] += 1
    D_sc_ac1.update(D_sc_ac1_cap)
    D_sc_ac76.update(D_sc_ac76_cap)
    rate_all = Num_ac76/(Num_ac1+0.1)
    rate0 = [D_sc_ac76[L[i]]/(D_sc_ac1[L[i]]+0.1) for i in range(len(L))]
    rate_each_sc = ['[=]'.join([L[i],'%0.4f'%rate0[i]]) for i in range(len(L)) if rate0[i]>0]
    rate_each_time = ['%0.4f'%(D_time_ac76[T[i]] / (D_time_ac1[T[i]] + 0.1)) for i in range(len(T))]
    X_user = ['%0.4f'%rate_all,'[&]'.join(rate_each_sc),'[&]'.join(rate_each_time)]
    S = [userid]+X_user
    S = '\t'.join(S)
    sys.stdout.write("%s\n" % S)

