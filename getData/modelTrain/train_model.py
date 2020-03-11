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
        self.testlines = 1000000
config_model = modelconfig()
Sc = config_model.get_sc()
def data_initial(path_global,path_user,user,Sc,resultpath):
    if not os.path.exists(os.path.join(resultpath,'tmpdata')):
        os.mkdir(os.path.join(resultpath,'tmpdata'))
    if os.path.exists(os.path.join(resultpath,'tmpdata',user+'list.npy')):
        print('data-initial of userdata from exist data...')
        userlist = np.load(os.path.join(resultpath,'tmpdata',user+'list.npy'))
        userdata = np.load(os.path.join(resultpath,'tmpdata',user+'data.npy'))
        D_user = {userlist[i]: userdata[i] for i in range(len(userlist))}
    else:
        feature_user = [os.path.join(path_user, user)]
        D_user = modules.feature_user(feature_user,Sc)
        List = [k for k in D_user]
        Data = [D_user[List[i]] for  i in range(len(List))]
        np.save(os.path.join(resultpath,'tmpdata',user+'list.npy'),List)
        np.save(os.path.join(resultpath,'tmpdata',user+'data.npy'),Data)
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
    return r_all,r_sc_all,r_time_all,D_user
def train(path_global,path_user,path_session, resultpath,model,joining=False):
    config_train=Config_train()
    config_model=modelconfig()
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
    completed = 0
    data_train = os.listdir(path_session)
    usernb = 0
    for path in data_train:
        usernb += 1
        datapath = modules.get_sessionfile(os.path.join(path_session,path))
        print('training on '+ path)
        time0 = time.time()
        users = path
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global,path_user,users,Sc,resultpath)
        D_other = [r_all] + r_sc_all + r_time_all
        iter = modules.iterData(datapath, D_user, D_other, r_sc_all, r_time_all,batch_size=config_train.train_batch_size, rate_skip = config_train.skip_rate,rate_skip_neg=1-r_all,config_global=config_model,joining=joining)
        epoch = 0
        loss_ = 0
        while epoch<config_train.epochs:
            data = next(iter)
            if data == '__STOP__':
                iter = modules.iterData(datapath, D_user, D_other, r_sc_all, r_time_all,batch_size=config_train.train_batch_size, rate_skip=1-r_all,config_global=config_model,joining=joining)
                epoch += 1
                continue
            x0, y0 = data
            y0 = np.array(y0)
            y0 = np.reshape(y0,(len(y0),1))
            if step%config_train.step_saveckpt==0:
                saver.save(session, os.path.join(path_ckpt, 'model.ckpt'), global_step=global_step)
                print('loss in step-{} is {}'.format(step,loss_))
            _,loss_, = session.run([train_op,loss],feed_dict={X_holder:x0, y_holder:y0, learning_rate:learning_rate_})
            step += 1
        completed += 1
        KK = len(data_train) - completed
        print('training used time %0.2f mins and needs about %0.2f mins for the rest users'%((time.time()-time0)/60,(time.time()-time0)/60*KK))
def test(path_global,path_user,path_session, resultpath,model,joining=False):
    config_train=Config_train()
    config_model=modelconfig()
    config_train.feature_dim = config_model.get_nb_features()[0]
    if joining:
        config_train.feature_dim+=1
    tf.reset_default_graph()
    if model=='lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(config_train)
    elif model=='lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(config_train)
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    path_ckpt = os.path.join(resultpath,config_train.CKPT_path)
    if not os.path.exists(path_ckpt):
        print('no model')
        return
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    if ckpt_file:
        saver.restore(session, ckpt_file)
    else:
        print('no model')
        return
    learning_rate_ = config_train.learning_rate
    step = 0
    completed = 0
    data_train = os.listdir(path_session)
    usernb = 0
    for path in data_train:
        usernb += 1
        datapath = modules.get_sessionfile(os.path.join(path_session,path))
        print('training on '+ path)
        time0 = time.time()
        users = path
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global,path_user,users,Sc,resultpath)
        D_other = [r_all] + r_sc_all + r_time_all
        iter = modules.iterData(datapath, D_user, D_other, r_sc_all, r_time_all,batch_size=config_train.testlines, rate_skip = config_train.skip_rate,rate_skip_neg=0,config_global=config_model,joining=joining)
        data = next(iter)
        x0, y0 = data
        feed_dict = {X_holder: x0, learning_rate: learning_rate_}
        yp = session.run(predict_y,feed_dict=feed_dict)
        yp = [yp[i][0] for i in range(len(yp))]
        auc = modules.calAUC(prob=yp, labels=y0)
        print('ckpt is {} with auc is {}'.format(ckpt_file,auc))
def predict(path_global,path_user,path_session,resultpath,model,path_ckpt='',path_userData='userData',joining=False,user_idx='a'):
    ####################################################
    auc,predictpaths=test(path_global,path_user,path_session,resultpath,model,path_ckpt,path_userData,joining,user_idx)
    savepaths = [predictpath.replace('predict', 'result') for predictpath in predictpaths]
    for i in range(len(savepaths)):
        modules.print_result(predictpaths[i], savepaths[i])
if __name__=='__main__':
    mode = sys.argv[1]
    path_global, path_user, path_session, resultpath, model = sys.argv[2:]
    if mode=='train':
        train(path_global,path_user,path_session, resultpath,model)
    if mode=='test':
        test(path_global,path_user,path_session, resultpath,model)