import xlrd
import numpy as np
import random
from modules import getFeature,calAUC
from modeling import simple_lr,simple_lr_dense
import tensorflow as tf
import os
import json
import sys
def getW2V(path_w2v):
    print('reading w2v file...')
    f = open(path_w2v,'r')
    D = {}
    for line in f:
        s = line.strip().split(' ')
        D[s[0]] = [float(t) for t in s[1:]]
    f.close()
    print('complete w2v reading')
    return D
class Config_train(object):
    def __init__(self):
        self.batch_size = 128
        self.feature_dim = None
        self.hiddenSize = 256
        self.skip_rate = 0.0
        self.train_batch_size = 1024
        self.test_batch_size = 10000
        self.init_learning_rate = 0.1
        self.end_learning_rate = 0.01
        self.learning_rate = 0.5
        self.keep_prob = 0.8
        self.nb_examples = 100000
        self.epochs = 3000
        self.step_saveckpt = 100
        self.step_printlog = 50
        self.testlines = 1000000
def dataSplit(path_train,path_test,config):
    with open(path_train,'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    XTrn = []
    for i in range(len(S)):
        s = S[i]
        XTrn.append(getFeature(s[0],config))
        if i%1000==0:
            print('get trainset feature %d lines from %d lines'%(i,len(S)))
    yTrn = [int(s[1]) for s in S]
    with open(path_test, 'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    XTst = []
    for i in range(len(S)):
        s = S[i]
        XTst.append(getFeature(s[0],config))
        if i%1000==0:
            print('get trainset feature %d lines from %d lines'%(i,len(S)))
    yTst = [int(s[1]) for s in S]
    print('number of train/test samples is {}/{}'.format(len(XTrn),len(XTst)))
    print('number of positive/negative samples of trainSet is {}/{}'.format(sum(yTrn),len(yTrn)-sum(yTrn)))
    print('number of positive/negative samples of testSet is {}/{}'.format(sum(yTst), len(yTst) - sum(yTst)))
    return XTrn,XTst,yTrn,yTst
def iterData(X,y,batch_size,epoch=20):
    L = [i for i in range(len(X))]
    for _ in range(epoch):
        random.shuffle(L)
        Xr = []
        yr = []
        for i in range(len(L)):
            Xr.append(X[L[i]])
            yr.append(y[L[i]])
            if len(Xr)==batch_size:
                yield Xr,yr
                Xr,yr = [],[]
        yield '__STOP__'
    yield '__RETURN__'
def iterData_test(X,y,batch_size):
    L = [i for i in range(len(X))]
    while True:
        random.shuffle(L)
        Xr = []
        yr = []
        for i in range(len(L)):
            Xr.append(X[L[i]])
            yr.append(y[L[i]])
            if len(Xr)==batch_size:
                yield Xr,yr
                Xr,yr = [],[]
def training(path_train,path_test,config_feature,path_ckpt,config_train,mode='lr'):
    XTrn, XTst, yTrn, yTst = dataSplit(path_train,path_test,config_feature)
    feature_dim = len(XTrn[0])
    config_train.feature_dim =feature_dim
    if mode=='lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(feature_dim)
    if mode=='lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(config_train)
    if mode=='lr-w2v':
        W_lr = np.load('lr-ckpt/W.npy')
        b = np.load('lr-ckpt/b.npy')
        W_w2v = np.zeros((feature_dim-W_lr.shape[0],1))
        W = np.concatenate((W_lr,W_w2v),axis=0)
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(
            feature_dim,W=W,b=b)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    if not os.path.exists(path_ckpt):
        os.mkdir(path_ckpt)
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    if ckpt_file:
        saver.restore(session, ckpt_file)
        print('restore model from %s'%ckpt_file)
    else:
        init = tf.global_variables_initializer()
        session.run(init)
    learning_rate_ = config_train.learning_rate
    iter = iterData(XTrn,yTrn,batch_size=config_train.train_batch_size,epoch=config_train.epochs)
    iter_test = iterData_test(XTst, yTst, batch_size=config_train.test_batch_size)
    data = next(iter)
    step = 0
    epoch = 0
    print('training begin')
    while data!='__RETURN__':
        if data=='__STOP__':
            data = next(iter)
            epoch += 1
            continue
        x0, y0 = data
        y0 = np.array(y0)
        y0 = np.reshape(y0,(len(y0),1))
        if step%config_train.step_saveckpt==0:
            saver.save(session, os.path.join(path_ckpt, 'model.ckpt'), global_step=global_step)
        if step%config_train.step_printlog==0:
            loss_ = session.run(loss, feed_dict={X_holder: x0, y_holder: y0, learning_rate: learning_rate_})
            datatest = next(iter_test)
            x0_test,y0_test = datatest
            y0_test = np.array(y0_test)
            y0_test = np.reshape(y0_test, (len(y0_test), 1))
            y_p0 = session.run(predict_y,
                               feed_dict={X_holder: x0_test, y_holder: y0_test, learning_rate: learning_rate_})
            y_p = [tmp[0] for tmp in y_p0]
            auc = calAUC(y_p,y0_test)
            print('epoch:{}-step:{}-auc_test:{}-loss_trn:{}'.format(epoch,step,'%0.3f'%auc,'%0.4f'%loss_))
        session.run(train_op,feed_dict={X_holder:x0, y_holder:y0, learning_rate:learning_rate_})
        step += 1
        data = next(iter)
    print('training over!')
def main(mode):
    path_train = 'data/train.txt'
    path_test = 'data/test.txt'
    path_idf = 'data/idf_char.json'
    path_vocab = 'data/vocab.txt'
    path_w2v = '/search/odin/guobk/streaming/vpa/word2vec128/model-mean'
    path_ckpt = mode+'-ckpt'
    config_feature = {}
    config_feature['use_charIdf'] = True
    config_feature['use_sentLen'] = True
    config_feature['use_puncExist'] = True
    config_feature['use_char'] = True
    if mode=='lr-w2v':
        config_feature['use_w2v'] = True
        config_feature['w2v'] = getW2V(path_w2v)
        config_feature['dim_v'] = 128
    config_train = Config_train()
    with open(path_idf,'r') as f:
        idf = json.load(f)
    with open(path_vocab,'r') as f:
        vocab = f.read().strip().split('\n')
    config_feature['idf'] = idf
    config_feature['charList'] = vocab
    training(path_train,path_test, config_feature, path_ckpt, config_train,mode=mode)
if __name__=='__main__':
    mode = sys.argv[1]
    main(mode)