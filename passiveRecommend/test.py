from modules import getFeature,calAUC
from train import Config_train
from modeling import simple_lr,simple_lr_dense
import tensorflow as tf
import numpy as np
import os
import json
import sys
def testing(path_test,config_feature,path_ckpt,config_train,mode='lr'):
    with open(path_test, 'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    XTst = [getFeature(s[0], config_feature) for s in S]
    yTst = [int(s[1]) for s in S]
    print('number of positive/negative samples of testSet is {}/{}'.format(sum(yTst), len(yTst) - sum(yTst)))
    feature_dim = len(XTst[0])
    config_train.feature_dim =feature_dim
    if mode=='lr':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(feature_dim)
    if mode=='lr-dense':
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(config_train)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    saver.restore(session, ckpt_file)
    print('restore model from %s'%ckpt_file)
    learning_rate_ = config_train.learning_rate
    x0_test,y0_test = XTst,yTst
    y0_test = np.array(y0_test)
    y0_test = np.reshape(y0_test, (len(y0_test), 1))
    y_p0 = session.run(predict_y,
                       feed_dict={X_holder: x0_test, y_holder: y0_test, learning_rate: learning_rate_})
    y_p = [tmp[0] for tmp in y_p0]
    auc = calAUC(y_p,y0_test)
    X = ['\t'.join(['预测值','实际值','文本'])]
    for i in range(len(S)):
        X.append('%0.4f'%y_p[i]+'\t'+S[i][1]+'\t'+S[i][0])
    with open('data/test_predict.txt','w') as f:
        f.write('\n'.join(X))
    thr0 = [0.1*i for i in range(10)]
    R = ['\t'.join(['阈值','准确率','精度','召回率'])]
    for thr in thr0:
        yp = [int(t>thr) for t in y_p]
        TP = sum([yp[i]==yTst[i] for i in range(len(yp)) if yp[i]==1])
        TN = sum([yp[i]==yTst[i] for i in range(len(yp)) if yp[i]==0])
        FP = sum([yp[i]!=yTst[i] for i in range(len(yp)) if yp[i]==1])
        FN = sum([yp[i]!=yTst[i] for i in range(len(yp)) if yp[i]==0])
        acc = float(TP+TN)/len(yp)
        pre = float(TP)/(TP+FP)
        rec = float(TP)/(TP+FN)
        R.append('\t'.join(['%0.1f'%thr,'%0.4f'%acc,'%0.4f'%pre,'%0.4f'%rec]))
        print([thr,acc,pre,rec])
    with open('data/test_result.txt','w') as f:
        f.write('\n'.join(R))
def main(mode):
    path_test = 'data/test.txt'
    path_idf = 'data/idf_char.json'
    path_vocab = 'data/vocab.txt'
    path_ckpt = mode+'-ckpt'
    config_feature = {}
    config_feature['use_charIdf'] = True
    config_feature['use_sentLen'] = True
    config_feature['use_puncExist'] = True
    config_feature['use_char'] = True
    config_train = Config_train()
    with open(path_idf,'r') as f:
        idf = json.load(f)
    with open(path_vocab,'r') as f:
        vocab = f.read().strip().split('\n')
    config_feature['idf'] = idf
    config_feature['charList'] = vocab
    testing(path_test, config_feature, path_ckpt, config_train,mode=mode)
if __name__=='__main__':
    mode = sys.argv[1]
    main(mode)