import xlrd
import numpy as np
import random
from modules import getFeature,calAUC
from modeling import simple_lr,simple_lr_dense
import tensorflow as tf
import os
import json
import sys
class Config_train(object):
    def __init__(self):
        self.batch_size = 128
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
        self.epochs = 3000
        self.step_saveckpt = 100
        self.step_printlog = 50
        self.testlines = 1000000
def dataSplit(path_data,config,rate_test=0.25):
    workbook = xlrd.open_workbook(path_data)  # 打开excel文件
    table = workbook.sheet_by_name('Sheet1')  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列
    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    res = res[1:]
    random.shuffle(res)
    S = []
    y = []
    for i in range(len(res)):
        if isinstance(res[i][1],str):
            S.append(res[i][1])
            y.append(res[i][2])
    X = [getFeature(s,config) for s in S]
    XTst = X[:int(len(S)*rate_test)]
    XTrn = X[int(len(S)*rate_test):]
    yTst = y[:int(len(S)*rate_test)]
    yTrn = y[int(len(S)*rate_test):]
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
def training(path_data,config_feature,path_ckpt,config_train,mode='lr'):
    XTrn, XTst, yTrn, yTst = dataSplit(path_data,config_feature)
    feature_dim = len(XTrn[0])
    config_train.feature_dim =feature_dim
    if mode=='lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(feature_dim)
    if mode=='lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(config_train)
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
    data = next(iter)
    step = 0
    yTst1 = np.reshape(yTst,(len(yTst),1))
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
            y_p0 = session.run(predict_y,
                               feed_dict={X_holder: XTst, y_holder: yTst1, learning_rate: learning_rate_})
            y_p = [tmp[0] for tmp in y_p0]
            auc = calAUC(y_p,yTst)
            print('epoch:{}-step:{}-auc_test:{}-loss_trn:{}'.format(epoch,step,'%0.3f'%auc,'%0.4f'%loss_))
        session.run(train_op,feed_dict={X_holder:x0, y_holder:y0, learning_rate:learning_rate_})
        step += 1
        data = next(iter)
    print('training over!')
def main(mode):
    path_data = 'data/data.xlsx'
    path_idf = 'data/idf_char.json'
    path_ckpt = mode+'-ckpt'
    config_feature = {}
    config_feature['use_charIdf'] = True
    config_feature['use_sentLen'] = True
    config_feature['use_puncExist'] = True
    config_feature['use_char'] = True
    config_train = Config_train()
    with open(path_idf,'r') as f:
        idf = json.load(f)
    config_feature['idf'] = idf
    charList = [w for w in idf]
    config_feature['charList'] = charList
    training(path_data, config_feature, path_ckpt, config_train,mode=mode)
if __name__=='__main__':
    mode = sys.argv[1]
    main(mode)