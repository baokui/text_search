#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import time
import os
def get_sessionfile(rootpath):
    datas = []
    def eachFile(filepath):
        fileNames = os.listdir(filepath)  # 获取当前路径下的文件名，返回List
        for file in fileNames:
            newDir = filepath + '/' + file  # 将文件命加入到当前文件路径后面
            # print(newDir)
            # if os.path.isdir(newDir): # 如果是文件夹
            if os.path.isfile(newDir):  # 如果是文件
                if 'part-' in newDir:
                    datas.append(newDir)
            else:
                eachFile(newDir)  # 如果不是文件，递归这个文件夹的路径
    eachFile(rootpath)
    return datas
def feature_global(files,config_global):
    Sc = config_global.get_sc()
    def getdata(filepath):
        with open(filepath,'r') as f:
            s = f.read().split('\n')
        if len(s)<7:
            return []
        N = s[0].split('\t')[1:3]
        nb_ac1 = int(N[0])
        nb_ac76 = int(N[1])
        nb_sc_ac1 = [int(ss) for ss in s[2].split('\t')[1:]]
        nb_sc_ac76 = [int(ss) for ss in s[3].split('\t')[1:]]
        nb_time_ac1 = [int(ss) for ss in s[5].split('\t')[1:]]
        nb_time_ac76 = [int(ss) for ss in s[6].split('\t')[1:]]
        return nb_ac1,nb_ac76,np.array(nb_sc_ac1),np.array(nb_sc_ac76),np.array(nb_time_ac1),np.array(nb_time_ac76)
    nb_ac1, nb_ac76 = 0,0
    nb_sc_ac1, nb_sc_ac76  = np.zeros((len(Sc),)),np.zeros((len(Sc),))
    nb_time_ac1, nb_time_ac76 = np.zeros((len(config_global.T),)),np.zeros((len(config_global.T),))
    for file in files:
        subfiles = os.listdir(file)
        for sfile in subfiles:
            if 'part' not in sfile:
                continue
            filepath = os.path.join(file,sfile)
            x = getdata(filepath)
            if len(x)==6:
                nb_ac1 += x[0]
                nb_ac76 += x[1]
                nb_sc_ac1 += x[2][:len(Sc)]
                nb_sc_ac76 += x[3][:len(Sc)]
                nb_time_ac1 += x[4]
                nb_time_ac76 += x[5]
    r_ac76 = nb_ac76 / (nb_ac1 + 1.0)
    r_sc_ac76 = [nb_sc_ac76[i] / (nb_sc_ac1[i] + 0.01) for i in range(len(nb_sc_ac1))]
    r_time_ac76 = [nb_time_ac76[i] / (nb_time_ac1[i] + 0.01) for i in range(len(nb_time_ac1))]
    return r_ac76,r_sc_ac76,r_time_ac76
def feature_user(files):
    def getdata(filepath):
        d = {}
        f = open(filepath,'r')
        line = f.readline()
        while line:
            line = line.strip()
            s = line.split('\t')
            userid = s[0]
            x = [float(ss) for ss in s[1:]]
            d[userid] = np.array(x)
            line = f.readline()
        f.close()
        return d
    D = {}
    for file in files:
        for part in range(5):
            filepath = os.path.join(file,'part-0000'+str(part))
            Dnew = getdata(filepath)
            D.update(Dnew)
    return D
def userFeatureParse(data,nb_feature_user,T_len,nb_sc):
    x = np.zeros((nb_feature_user,))
    x[0] = data[0]
    x[-T_len:] = data[-T_len:]
    for i in range(1,len(data)-T_len):
        if data[i][0]>=nb_sc:
            continue
        x[data[i][0]+1] = data[i][1]
    return x
def iterData(files,D_user,D_other,r_sc_all,r_time_all,punc=set('?!.,？！。，'),batch_size=32,epochs=1,rate_skip = 0.5,rate_skip_neg=0.996,max_line=np.inf,config_global={},joining=False):
    T_len = len(config_global.T)
    nb_features, nb_features_session, nb_features_user, nb_features_global=config_global.get_nb_features()
    X = []
    y = []
    k = 0
    for epoch in range(epochs):
        for file in files:
            f = open(file,'r')
            line = f.readline()
            k += 1
            if k >= max_line:
                yield '__STOP__'
            while line:
                line = line.strip()
                s = line.split('\t')
                sessid = s[0]
                #训练集1-7，测试集0
                '''
                if sessid[-1]=='0':
                    line = f.readline()
                    continue
                '''
                if np.random.uniform() < rate_skip:
                    line = f.readline()
                    continue
                if s[-1] == '0' and np.random.uniform() < rate_skip_neg:
                    line = f.readline()
                    continue
                userid = s[1]
                s = s[2:]
                ##################################
                hour = float(s[0])
                interval_last_76 = 0
                timeIndex = int(s[1])
                time_slot = np.zeros((len(r_time_all),))
                time_slot[timeIndex] = 1.0
                sc = np.zeros((len(r_sc_all),))
                scIndex = int(s[3])
                if scIndex>=len(r_sc_all):
                    line = f.readline()
                    continue
                sc[scIndex] = 1.0
                inputStr = s[4]
                pun_appear = int(sum([int(p in inputStr) for p in punc])>0)
                feature_session = [hour] + [interval_last_76] + list(sc) + list(time_slot) + [len(inputStr)] + [pun_appear]
                feature_session = np.array(feature_session)
                ####################################
                if userid not in D_user:
                    feature_user = D_other
                else:
                    feature_user = userFeatureParse(D_user[userid],nb_features_user,T_len,len(r_sc_all))
                ####################################
                r_sc_all_ = r_sc_all[scIndex]
                feature_global = np.array([r_sc_all_,r_time_all[timeIndex]])
                ####################################
                feature_platform = []
                if joining:
                    if len(userid) == 32:
                        feature_platform = [1]
                    else:
                        feature_platform = [0]
                feature_platform = np.array(feature_platform)
                ####################################
                x = np.concatenate((feature_session, feature_user, feature_global, feature_platform))
                X.append(x)
                y.append(float(s[-1]))
                if len(X)==batch_size:
                    yield X,y
                    X = []
                    y = []
                line = f.readline()
                k += 1
                if k>=max_line:
                    yield '__STOP__'
    yield '__STOP__'
def iterData_save(files,D_user,D_other,r_sc_all,r_time_all,path_tmpfile0,user,Date_sess,epoch,punc=set('?!.,？！。，'),batch_size=32,epochs=1,rate_skip = 0.5,rate_skip_neg=0.996,max_line=np.inf,config_global={},joining=False):
    print('test0')
    step = 0
    path_tmpfile = os.path.join(path_tmpfile0, 'feature')
    def datawriter(data,step):
        nb_tmpfiles = len(os.listdir(path_tmpfile))
        while nb_tmpfiles>32:
            time.sleep(1)
            nb_tmpfiles = len(os.listdir(path_tmpfile))
        np.save(os.path.join(path_tmpfile,user+'-'+epoch+'-'+Date_sess+'-'+str(step)+'.npy'),data)
        with open(os.path.join(path_tmpfile0,'trainedlist.txt'),'a+') as f:
            f.write(user+'-'+epoch+'-'+Date_sess+'-'+str(step)+'.npy'+'\n')
    T_len = len(config_global.T)
    nb_features, nb_features_session, nb_features_user, nb_features_global=config_global.get_nb_features()
    X = []
    y = []
    k = 0
    print('test1')
    for epoch in range(epochs):
        for file in files:
            print('test2')
            f = open(file,'r')
            line = f.readline()
            k += 1
            if k >= max_line:
                return
            while line:
                print('test3')
                line = line.strip()
                s = line.split('\t')
                sessid = s[0]
                #训练集1-7，测试集0
                '''
                if sessid[-1]=='0':
                    line = f.readline()
                    continue
                '''
                if np.random.uniform() < rate_skip:
                    line = f.readline()
                    continue
                if s[-1] == '0' and np.random.uniform() < rate_skip_neg:
                    line = f.readline()
                    continue
                userid = s[1]
                s = s[2:]
                ##################################
                hour = float(s[0])
                interval_last_76 = 0
                timeIndex = int(s[1])
                time_slot = np.zeros((len(r_time_all),))
                time_slot[timeIndex] = 1.0
                sc = np.zeros((len(r_sc_all),))
                scIndex = int(s[3])
                if scIndex>=len(r_sc_all):
                    line = f.readline()
                    continue
                sc[scIndex] = 1.0
                inputStr = s[4]
                pun_appear = int(sum([int(p in inputStr) for p in punc])>0)
                feature_session = [hour] + [interval_last_76] + list(sc) + list(time_slot) + [len(inputStr)] + [pun_appear]
                feature_session = np.array(feature_session)
                ####################################
                if userid not in D_user:
                    feature_user = D_other
                else:
                    feature_user = userFeatureParse(D_user[userid],nb_features_user,T_len,len(r_sc_all))
                ####################################
                r_sc_all_ = r_sc_all[scIndex]
                feature_global = np.array([r_sc_all_,r_time_all[timeIndex]])
                ####################################
                feature_platform = []
                if joining:
                    if len(userid) == 32:
                        feature_platform = [1]
                    else:
                        feature_platform = [0]
                feature_platform = np.array(feature_platform)
                ####################################
                x = np.concatenate((feature_session, feature_user, feature_global, feature_platform))
                X.append(x)
                y.append(float(s[-1]))
                print('test4',len(X),batch_size)
                if len(X)==batch_size:
                    data = X,y
                    print('test-before-write')
                    datawriter(data, step)
                    print('test-after-write')
                    step += 1
                    X,y = [],[]
                line = f.readline()
                k += 1
                if k>=max_line:
                    return
def Data_test(files,D_user,D_other, r_sc_all,r_time_all,user_idx = 'a',batch_size=1024,punc=set('?!.,？！。，'),rate_skip=0.0,max_line=5000000,last76_drop=False, config_global={},joining=False):
    if 'ios' in files[0]:
        user_idx = '0123'
    T_len = len(config_global.T)
    nb_features, nb_features_session, nb_features_user, nb_features_global = config_global.get_nb_features()
    X = []
    y = []
    user = []
    nb_lines = 0
    for file in files:
        f = open(file,'r')
        line = f.readline()
        while line:
            line = line.strip()
            s = line.split('\t')
            sessid = s[0]
            userid = s[1]
            if userid[0] not in user_idx or userid[5] not in user_idx:
                line = f.readline()
                continue
            s = s[2:]
            ##################################
            hour = float(s[0])
            interval_last_76 = 0
            timeIndex = int(s[1])
            time_slot = np.zeros((len(r_time_all),))
            time_slot[timeIndex] = 1.0
            sc = np.zeros((len(r_sc_all),))
            scIndex = int(s[3])
            if scIndex >= len(r_sc_all):
                line = f.readline()
                continue
            sc[scIndex] = 1.0
            inputStr = s[4]
            pun_appear = int(sum([int(p in inputStr) for p in punc])>0)
            feature_session = [hour] + [interval_last_76] + list(sc) + list(time_slot) + [len(inputStr)] + [pun_appear]
            feature_session = np.array(feature_session)
            ####################################
            if userid not in D_user:
                feature_user = D_other
            else:
                feature_user = userFeatureParse(D_user[userid],nb_features_user,T_len,len(r_sc_all))
            ####################################
            r_sc_all_ = r_sc_all[scIndex]
            feature_global = np.array([r_sc_all_,r_time_all[timeIndex]])
            ####################################
            feature_platform = []
            if joining:
                if len(userid) == 32:
                    feature_platform = [1]
                else:
                    feature_platform = [0]
            feature_platform = np.array(feature_platform)
            ####################################
            x = np.concatenate((feature_session, feature_user, feature_global, feature_platform))
            X.append(x)
            y.append(float(s[-1]))
            user.append(userid)
            if len(X)==batch_size:
                yield X,y,user
                X = []
                y = []
                user = []
            if nb_lines>=max_line:
                yield "__STOP__"
            line = f.readline()
            nb_lines += 1
    yield "__STOP__"
def calAUC(prob, labels):
    f = list(zip(prob, labels))
    rank = [values2 for values1, values2 in sorted(f, key=lambda x: x[0])]
    rankList = [i + 1 for i in range(len(rank)) if rank[i] == 1]
    posNum = 0.0
    negNum = 0.0
    for i in range(len(labels)):
        if (labels[i] == 1):
            posNum += 1
        else:
            negNum += 1
    auc = (sum(rankList) - (posNum * (posNum + 1)) / 2) / (posNum * negNum)
    # print(auc)
    return auc
def getAUC(file):
    with open(file,'r') as f:
        s = f.read().strip().split('\n')
    s = [ss.split('\t') for ss in s]
    s = [ss for ss in s if len(ss)>=3]
    prob = [float(ss[2]) for ss in s]
    labels = [int(ss[1]) for ss in s]
    auc = calAUC(prob,labels)
    return auc
def print_result(file,savepath,t0 = [i * 0.01 for i in range(0, 100)],r0_show=[1.0,0.975,0.95,0.925,0.9,0.875,0.85,0.8,0.7,0.6,0.5,0]):
    with open(file,'r') as f:
        s = f.read().strip().split('\n')
    s = [ss.split('\t') for ss in s]
    s = [ss for ss in s if len(ss)>=3]
    userlist = [ss[0] for ss in s]
    prob = [float(ss[2]) for ss in s]
    labels = [int(ss[1]) for ss in s]
    user_set = set(userlist)
    sess_ac76 = [int(t==1) for t in labels]
    user_ac76 = [userlist[i] for i in range(len(userlist)) if labels[i]==1]
    user_ac76 = set(user_ac76)
    nb_sess = len(s)
    auc = calAUC(prob,labels)
    R = [['threshold', 'showing-decrease', 'click-decrease', 'pv', 'uv', 'cover']]
    r_bin = [r0_show[0],r0_show[1]]
    k = 0
    for t in t0:
        sess_new = [s[i] for i in range(len(s)) if prob[i]> t]
        nb_show = len(sess_new)
        rate_show = nb_show/(nb_sess+0.0)
        if rate_show>r_bin[1] and t!=0:
            continue
        k+=1
        r_bin = [r0_show[k],min(r0_show[k+1],rate_show)]
        nb_click = len([i for i in range(len(sess_new)) if sess_new[i][1]=='1'])
        rate_click = nb_click/(nb_show+0.0)
        decrease_click = nb_click/(sum(sess_ac76)+0.0)
        user_new = [sess_new[i][0] for i in range(len(sess_new))]
        user_new_click = [sess_new[i][0] for i in range(len(sess_new)) if sess_new[i][1]=='1']
        rate_user = len(set(user_new_click))/(len(set(user_new))+0.0)
        cover = len(set(user_new))/(len(user_set)+0.0)
        rr = ['%0.4f'%t,"%0.4f"%rate_show,"%0.4f"%decrease_click,"%0.4f"%rate_click,"%0.4f"%rate_user,"%0.4f"%cover]
        R.append(rr)
        if rate_show<r0_show[-2]:
            break
    R = ['\t'.join(r) for r in R]
    with open(savepath, 'w+') as f:
        f.write('\n'.join(R))
        f.write('\nauc:%s' % str(auc))
    return R,auc
if __name__ == '__main__':
    pass