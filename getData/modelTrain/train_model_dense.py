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
def data_initial(path_global,path_user,users,path_userData='userData'):
    if os.path.exists(path_userData):
        print('data-initial of userdata from exist data...')
        userlist = np.load(path_userData + '/' + users[0] + 'list.npy')
        userdata = np.load(path_userData + '/' + users[0] + 'data.npy',allow_pickle=True)
        D_user = {userlist[i]: userdata[i] for i in range(len(userlist))}
    else:
        feature_user = [os.path.join(path_user, path) for path in users]
        D_user = modules.feature_user(feature_user)
    path_globalData = os.path.join(resultpath,'tmpdata','data_global.npy')
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
        r_sc_all = np.array(r_sc_all)
        r_time_all = np.array(r_time_all)
    return r_all,r_sc_all,r_time_all,D_user
def train(path_tmpfile,resultpath,model,joining=False):
    config_train=Config_train()
    config_train.feature_dim = config_model.get_nb_features()[0]
    if joining:
        config_train.feature_dim+=1
    tf.reset_default_graph()
    if model=='lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(config_train)
    elif model=='lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(config_train)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    path_ckpt = os.path.join(resultpath,config_train.CKPT_path)
    if not os.path.exists(path_ckpt):
        os.mkdir(path_ckpt)
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    if ckpt_file:
        saver.restore(session, ckpt_file)
    else:
        init = tf.global_variables_initializer()
        session.run(init)
    learning_rate_ = config_train.learning_rate
    step = 0
    time0 = time.time()
    waittime=0
    while True:
        files = os.listdir(path_tmpfile)
        if len(files)==0:
            time.sleep(10)
            waittime += 10
            files = os.listdir(path_tmpfile)
        else:
            waittime = 0
        if waittime > 2*60*60:
            break
        for file in files:
            try:
                path = os.path.join(path_tmpfile,file)
                data = np.load(path,allow_pickle=True)
                x0, y0 = data
                x0 = list(x0)
                y0 = np.reshape(y0,(len(y0),1))
                if step%config_train.step_saveckpt==0:
                    saver.save(session, os.path.join(path_ckpt, 'model.ckpt'), global_step=global_step)
                session.run(train_op,feed_dict={X_holder:x0, y_holder:y0, learning_rate:learning_rate_})
                step += 1
                os.remove(path)
                print('training used time %0.2f mins for %d steps'%((time.time()-time0)/60,step))
            except:
                print('fail to train on %s'%path)
                os.remove(path)
def test(path_global,path_user,path_session,resultpath,model,path_ckpt='',path_userData='userData',joining=False,user_idx='a'):
    ####################################################
    config_train = Config_train()
    config_train.feature_dim = config_model.get_nb_features()[0]
    if joining:
        config_train.feature_dim+=1
    tf.reset_default_graph()
    if model == 'lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(
            config_train)
    elif model == 'lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(
            config_train)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver()
    session = tf.Session()
    if len(path_ckpt)==0:
        path_ckpt = os.path.join(resultpath, config_train.CKPT_path)
        if not os.path.exists(path_ckpt):
            os.mkdir(path_ckpt)
        ckpt_file = tf.train.latest_checkpoint(path_ckpt)
        print('ckpt file is %s' % ckpt_file)
        if ckpt_file:
            saver.restore(session, ckpt_file)
        else:
            return
    else:
        print('ckpt file is %s'%path_ckpt)
        ckpt_file = path_ckpt
        if ckpt_file:
            saver.restore(session, ckpt_file)
        else:
            return
    idx = ckpt_file.find('model.ckpt-')+len('model.ckpt-')
    if not os.path.exists(os.path.join(resultpath,'test')):
        os.mkdir(os.path.join(resultpath,'test'))
    predictpath0 = os.path.join(resultpath,'test','predict'+ckpt_file[idx:])

    learning_rate_ = config_train.learning_rate
    data_train = os.listdir(path_session)
    auc = 0
    auc_each = []
    predictpaths = []
    for path in data_train:
        predictpath = predictpath0 + '-' + path + '.txt'
        datapath = modules.get_sessionfile(os.path.join(path_session, path))
        users = [path]
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global, path_user, users,path_userData)
        D_other = [r_all] + r_sc_all + r_time_all
        iter = modules.Data_test(datapath, D_user,D_other, r_sc_all, r_time_all, user_idx=user_idx,batch_size = config_train.test_batch_size, punc=config_model.punc,
                                       max_line=config_train.testlines, config_global=config_model,joining=joining)
        data = next(iter)
        #y_p = []
        #user = []
        #y = []
        nb_batch=0
        f_write = open(predictpath, 'w+')
        while data!="__STOP__":
            X, y0, userbatch =  data
            y0 = np.array(y0)
            y0 = np.reshape(y0, (len(y0), 1))
            X_test = X
            y_test = y0
            y_p0 = session.run(predict_y, feed_dict={X_holder: X_test, y_holder: y_test, learning_rate: learning_rate_})
            #y_p.append(y_p0)
            #y.append(y0)
            #user.extend(userbatch)
            print(nb_batch,config_train.testlines/config_train.test_batch_size)
            #y_p = np.concatenate(y_p)
            #y = np.concatenate(y)
            tmp = ['\t'.join([userbatch[ii], str(int(y0[ii][0])), str(y_p0[ii][0])]) for ii in range(len(y0))]
            f_write.write('\n'.join(tmp))
            f_write.write('\n')
            data = next(iter)
            nb_batch += 1
        auctmp = modules.getAUC(predictpath)
        auc_each.append('%0.4f'%auctmp)
        auc += auctmp
        predictpaths.append(predictpath)
        print('testing on file %s with auc = %0.4f and ckptfile is %s'%(os.path.join(path_session, path),auctmp,ckpt_file))
    auc = auc/len(data_train)
    print('testing on path %s with average auc = %0.4f and ckptfile is %s'%(path_session, auc,ckpt_file))
    if os.path.exists(os.path.join(resultpath, 'test-auc-ckpt.txt')):
        with open(os.path.join(resultpath, 'test-auc-ckpt.txt'), 'r') as f:
            stmp = f.read().strip().split('\n')
        auc0 = float(stmp[-1].split('\t')[0])
    else:
        stmp = []
        auc0 = 0
    if auc > auc0:
        ckpt_backup = os.path.join(resultpath, "ckpt_backup")
        if not os.path.exists(ckpt_backup):
            os.mkdir(ckpt_backup)
        tmpfile = tf.train.latest_checkpoint(path_ckpt)
        file = tmpfile + ".*"
        cmdstr = "cp " + file + " " + ckpt_backup
        os.system(cmdstr)
        stmp.append('%0.4f' % auc + '\t' + '\t'.join(auc_each) + '\t' + tmpfile)
        with open(os.path.join(resultpath, 'test-auc-ckpt.txt'), 'w') as f:
            f.write('\n'.join(stmp))
    return auc,predictpaths
def predict(path_global,path_user,path_session,resultpath,model,path_ckpt='',path_userData='userData',joining=False,user_idx='a'):
    ####################################################
    auc,predictpaths=test(path_global,path_user,path_session,resultpath,model,path_ckpt,path_userData,joining,user_idx)
    savepaths = [predictpath.replace('predict', 'result') for predictpath in predictpaths]
    for i in range(len(savepaths)):
        modules.print_result(predictpaths[i], savepaths[i])
if __name__=='__main__':
    mode = sys.argv[1]
    model = sys.argv[2]
    path_global = sys.argv[3]
    path_user = sys.argv[4]
    path_session = sys.argv[5]
    path_session_test = sys.argv[6]
    resultpath = sys.argv[7]
    path_userData = sys.argv[8]
    joining=False
    if len(sys.argv) > 9:
        joining = bool(int(sys.argv[9]))
    path_ckpt = ''
    if len(sys.argv)>10:
        path_ckpt = sys.argv[10]
    if mode=='train':
        train(path_session, resultpath, model,joining=joining)
    elif mode=='test':
        test(path_global,path_user,path_session_test,resultpath,model,path_ckpt='',joining=joining,path_userData=path_userData)
    elif mode=='predict':
        predict(path_global, path_user, path_session_test, resultpath, model, path_ckpt,joining=joining, path_userData=path_userData)