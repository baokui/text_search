import numpy as np
import os
import sys
def getSc():
    with open('../Config/table-trigger.txt') as f:
        S = [w.strip() for w in f]
    S = [a.split('\t') for a in S]
    L0 = [a[1] for a in S]
    L0 = list(set(L0))
    D_tr2sr = {a[0]:a[1] for a in S}
    with open('../Config/table-search-caption.txt') as f:
        L1 = [w.strip() for w in f]
    L1 += ['others']
    return L0,L1,D_tr2sr
def getScIndex(Str):
    if Str in D_tr2str:
        idx_sc = L0.index(D_tr2str[Str])
    else:
        idx_sc1 = len(L1)-1
        for i in range(len(L1)-1):
            if L1[i] in Str:
                idx_sc1 = i
                break
        idx_sc = len(L0)+idx_sc1
    return idx_sc
def userfile_merge(files,savepath0,useridSize=16):
    #files=['feature_user/user_'+idx for idx in '0123456789abcdef']
    files = files.split(',')
    for file in files:
        savepath = savepath0+'/'+file[-6:]
        userid_list = []
        D = []
        for part in range(5):
            fil = os.path.join(file,'part-0000'+str(part))
            print(fil)
            f_r = open(fil,'r')
            line = f_r.readline()
            while line:
                info = line.strip().split("\t")
                if len(info)!=3:
                    print(info)
                    line = f_r.readline()
                    continue
                userid_list.append(info[0])
                d = info[2].split('#')
                r0 = [float(d[0])]
                r1 = []
                if len(d[1])>0:
                    for d1 in d[1].split('[&]'):
                        dd = d1.split('[=]')
                        r1.append([int(dd[0]),float(dd[1])])
                r2 = [float(d2) for d2 in d[2].split('[&]')]
                D.append(r0+r1+r2)
                line=f_r.readline()
        np.save(savepath+'data.npy',D)
        np.save(savepath+'list.npy', userid_list)
if __name__=='__main__':
    L0, L1, D_tr2str = getSc()
    files,savepath0,useridSize = sys.argv[1:4]
    useridSize = int(useridSize)
    userfile_merge(files, savepath0, useridSize)