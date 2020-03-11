#!/usr/bin/python
# -*- coding: utf-8 -*-
from modeling import *
import numpy as np
import tensorflow as tf
import os
import modules
import sys
sys.path.append(r'../Config')
from ModelConfig import modelconfig
import time
class Config_train(object):
    def __init__(self):
        self.batch_size = None
        self.feature_dim = None
        self.hiddenSize = 256
        self.skip_rate = 0.0
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
        self.testlines = np.inf
def data_initial(path_global,path_user,users,path_userData='userData'):
    config_global = modelconfig()
    file_global = os.listdir(path_global)
    feature_global = [os.path.join(path_global,path) for path in file_global]
    feature_user = [os.path.join(path_user,path) for path in users]
    r_all,r_sc_all,r_time_all = modules.feature_global(feature_global,config_global)
    if os.path.exists(path_userData):
        print('data-initial of userdata from exist data...')
        userlist = np.load(path_userData + '/' + users[0] + 'list.npy')
        userdata = np.load(path_userData + '/' + users[0] + 'data.npy')
        D_user = {userlist[i]: userdata[i] for i in range(len(userlist))}
    else:
        D_user = modules.feature_user(feature_user)
    return r_all,r_sc_all,r_time_all,D_user
def train(path_global,path_user,path_session, path_session_test,resultpath,model,path_userData='userData',joining=False):
    config_train=Config_train()
    config_model=modelconfig()
    dim_sess = 4+len(config_model.sc)+len(config_model.T)+1
    dim_user = 1+len(config_model.sc)+len(config_model.T)+1
    dim_global = 2
    config_train.feature_dim = dim_sess+dim_user+dim_global
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
        users = [path]
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global,path_user,users,path_userData)
        D_other = [r_all] + r_sc_all + r_time_all
        iter = modules.iterData(datapath, D_user, D_other, r_sc_all, r_time_all,batch_size=config_train.train_batch_size, rate_skip = config_train.skip_rate,rate_skip_neg=1-r_all,config_global=config_model,joining=joining)
        epoch = 0
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
            session.run(train_op,feed_dict={X_holder:x0, y_holder:y0, learning_rate:learning_rate_})
            step += 1
        completed += 1
        KK = len(data_train) - completed
        print('training used time %0.2f mins and needs about %0.2f mins for the rest users'%((time.time()-time0)/60,(time.time()-time0)/60*KK))
        if usernb%10==0:
            print('***testing for %s'%path_session_test)
            auc = test(path_global, path_user, path_session_test, resultpath, model)
            print('***test over for %s' % path_session_test)
def test(path_global,path_user,path_session,resultpath,model,path_ckpt='',path_userData='userData',joining=False):
    ####################################################
    config_train = Config_train()
    config_model = modelconfig()
    dim_sess = 4 + len(config_model.sc) + len(config_model.T) + 1
    dim_user = 1 + len(config_model.sc) + len(config_model.T) + 1
    dim_global = 2
    config_train.feature_dim = dim_sess + dim_user + dim_global
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

    learning_rate_ = config_train.learning_rate
    data_train = os.listdir(path_session)
    auc = 0
    for path in data_train:
        predictpath = os.path.join(resultpath, 'test', 'predict' + ckpt_file[idx:] +path+ '.txt')
        savepath = os.path.join(resultpath, 'test', 'result' + ckpt_file[idx:] +path+ '.txt')
        datapath = modules.get_sessionfile(os.path.join(path_session, path))
        users = [path]
        r_all, r_sc_all, r_time_all, D_user = data_initial(path_global, path_user, users,path_userData)
        D_other = [r_all] + r_sc_all + r_time_all
        X, y, user = modules.Data_test(datapath, D_user, D_other, r_sc_all, r_time_all, punc=config_model.punc,
                                       max_line=config_train.testlines, config_global=config_model,joining=joining)
        y = np.array(y)
        y = np.reshape(y, (len(y), 1))
        y_p = []
        batch_size = config_train.test_batch_size
        i = 0
        while i * batch_size < len(y):
            X_test = X[i * batch_size:(i + 1) * batch_size]
            y_test = y[i * batch_size:(i + 1) * batch_size]
            y_p0 = session.run(predict_y, feed_dict={X_holder: X_test, y_holder: y_test, learning_rate: learning_rate_})
            y_p.append(y_p0)
            i += 1
        y_p = np.concatenate(y_p)
        tmp = ['\t'.join([user[ii], str(int(y[ii][0])), str(y_p[ii][0])]) for ii in range(len(y))]
        with open(predictpath, 'w') as f:
            f.write('\n'.join(tmp))
        modules.print_result(predictpath, savepath)
def predict(test_users,model):
    ####################################################
    config_train = Config_train()
    config_model = modelconfig()
    config_train.feature_dim = config_model.get_nb_features()[0]
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
    ckpt_file = config_model.path_lrmodel
    saver.restore(session, ckpt_file)
    learning_rate_ = config_train.learning_rate
    path_session = config_model.path_userdata+'/feature_session/'
    path_global = config_model.path_userdata+'/feature_global/'
    path_user = config_model.path_userdata + '/feature_user/'
    path = test_users
    datapath = modules.get_sessionfile(os.path.join(path_session, path))
    print('testing on ' + path)
    users = [path]
    r_all, r_sc_all, r_time_all, D_user = data_initial(path_global, path_user, users)
    D_other = [r_all] + r_sc_all + r_time_all
    X, y, user = modules.Data_test(datapath, D_user, D_other, r_sc_all, r_time_all, punc=config_model.punc,
                                   max_line=100, config_global=config_model)
    y = np.array(y)
    y = np.reshape(y, (len(y), 1))
    y_p = []
    batch_size = config_train.test_batch_size
    i = 0
    while i * batch_size < len(y):
        X_test = X[i * batch_size:(i + 1) * batch_size]
        y_test = y[i * batch_size:(i + 1) * batch_size]
        y_p0 = session.run(predict_y, feed_dict={X_holder: X_test, y_holder: y_test, learning_rate: learning_rate_})
        y_p.append(y_p0)
        i += 1
    y_p = np.concatenate(y_p)
    return user,y_p
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
    test(path_global,path_user,path_session_test,resultpath,model,path_ckpt,path_userData=path_userData)
