#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
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
L0,L1,D_tr2sr = getSc()
def getScIndex(Str):
    if Str in D_tr2sr:
        idx_sc = L0.index(D_tr2sr[Str])
    else:
        idx_sc1 = len(L1)-1
        for i in range(len(L1)-1):
            if L1[i] in Str:
                idx_sc1 = i
                break
        idx_sc = len(L0)+idx_sc1
    return idx_sc
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
    D_sc_ac1 = {}
    D_sc_ac76 = {}
    Num_ac1 = 0
    Num_ac76 = 0
    D_time_ac1 = {d: 0 for d in T}
    D_time_ac76 = {d: 0 for d in T}
    for h in history_list:
        act = h.split('[&]')
        timeIndex = date_to_timestamp(act[0])
        Num_ac1 += 1
        D_time_ac1[T[timeIndex]] += 1
        idx_sc = str(getScIndex(act[2]))
        if idx_sc in D_sc_ac1:
            D_sc_ac1[idx_sc] += 1
            if '76' in act[1]:
                Num_ac76 += 1
                D_time_ac76[T[timeIndex]] += 1
                D_sc_ac76[idx_sc] += 1
        else:
            D_sc_ac1[idx_sc] = 1
            D_sc_ac76[idx_sc] = 0
            if '76' in act[1]:
                Num_ac76 += 1
                D_time_ac76[T[timeIndex]] += 1
                D_sc_ac76[idx_sc] = 1
    rate_all = Num_ac76 / (Num_ac1 + 0.1)
    rate_each_sc = ['[=]'.join([d,'%0.6f'%(D_sc_ac76[d]/D_sc_ac1[d])]) for d in D_sc_ac76 if D_sc_ac76[d]>0]
    rate_each_time = ['%0.6f'%(D_time_ac76[T[i]] / (D_time_ac1[T[i]] + 0.1)) for i in range(len(T))]
    X_user = ['%0.6f'%rate_all,'[&]'.join(rate_each_sc),'[&]'.join(rate_each_time)]
    S = [userid]+X_user
    S = '\t'.join(S)
    sys.stdout.write("%s\n" % S)

