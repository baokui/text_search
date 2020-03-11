#!/usr/bin/python
# -*- coding: utf-8 -*-
from modeling import *
import numpy as np
import tensorflow as tf
import os
import modules
import sys
sys.path.append(r'./Config')
from ModelConfig import modelconfig
import time
import shutil
class Config_train(object):
    def __init__(self):
        self.batch_size = None
        self.feature_dim = None
        self.hiddenSize = 256
        self.skip_rate = 0.5
        self.train_batch_size = 1024
        self.test_batch_size = 1024
        self.init_learning_rate = 0.1
        self.end_learning_rate = 0.01
        self.learning_rate = 0.5
        self.keep_prob = 0.8
        self.nb_examples = 100000
        self.epochs = 1
        self.CKPT_path = 'ckpt'
        self.step_saveckpt = 100
        self.testlines = 5000000
config_model = modelconfig()
Sc,_ = config_model.get_sc()
def data_initial(path_global,path_user,users,path_tmpfile0,path_userData='userData'):
    if os.path.exists(path_userData):
        print('data-initial of userdata from exist data...')
        userlist = np.load(path_userData + '/' + users[0] + 'list.npy')
        userdata = np.load(path_userData + '/' + users[0] + 'data.npy')
        D_user = {userlist[i]: userdata[i] for i in range(len(userlist))}
    else:
        feature_user = [os.path.join(path_user, path) for path in users]
        D_user = modules.feature_user(feature_user)
    path_globalData = os.path.join(path_tmpfile0,'data_global.npy')
    if os.path.exists(path_globalData):
        data_global = np.load(path_globalData)
        r_all = data_global[0]
        r_sc_all = list(data_global[1:1+len(Sc)])
        r_time_all = list(data_global[-len(config_model.T):])
    else:
        file_global = os.listdir(path_global)
        feature_global = [os.path.join(path_global, path) for path in file_global]
        r_all, r_sc_all, r_time_all = modules.feature_global(feature_global, config_model)
        data_global = [r_all] + r_sc_all + r_time_all
        np.save(path_globalData,data_global)
    return r_all,r_sc_all,r_time_all,D_user
def main(path_global,path_user,path_session,user, path_tmpfile0,epoch,Date_sess, path_userData,joining=False):
    Date_sess = Date_sess.replace('/','')
    config_train=Config_train()
    path_tmpfile = os.path.join(path_tmpfile0,'feature')
    path_session_user=os.path.join(path_session,user)
    if not os.path.exists(path_session_user):
        print(path_session_user+' is not exist')
        return
    try:
        datapath = modules.get_sessionfile(path_session_user)
        users = [user]
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global,path_user,users,path_tmpfile0,path_userData)
        D_other = [r_all] + r_sc_all + r_time_all
        iter = modules.iterData(datapath, D_user, D_other, r_sc_all, r_time_all,batch_size=config_train.train_batch_size, rate_skip = config_train.skip_rate,rate_skip_neg=1-r_all,config_global=config_model,joining=joining)
        data = next(iter)
        step = 0
        while data!='__STOP__':
            nb_tmpfiles = len(os.listdir(path_tmpfile))
            while nb_tmpfiles>32:
                time.sleep(1)
                nb_tmpfiles = len(os.listdir(path_tmpfile))
            np.save(os.path.join(path_tmpfile,user+'-'+epoch+'-'+Date_sess+'-'+str(step)+'.npy'),data)
            data = next(iter)
            step += 1
            with open(os.path.join(path_tmpfile0,'trainedlist.txt'),'a+') as f:
                f.write(user+'-'+epoch+'-'+Date_sess+'-'+str(step)+'.npy'+'\n')
    except:
        print('failed to get tmpfile %s'%path_session_user)
    shutil.rmtree(path_session_user)
if __name__=='__main__':
    path_global = sys.argv[1]
    path_user = sys.argv[2]
    path_session = sys.argv[3]
    user = sys.argv[4]
    path_tmpfile = sys.argv[5]
    epoch = sys.argv[6]
    Date_sess = sys.argv[7]
    path_userData = sys.argv[8]
    joining=False
    if len(sys.argv) > 9:
        joining = bool(int(sys.argv[9]))
    main(path_global, path_user, path_session, user, path_tmpfile,epoch,Date_sess,path_userData,joining=joining)
