from modules import getFeature,calAUC
from train import Config_train
from modeling import simple_lr,simple_lr_dense
import tensorflow as tf
import numpy as np
import os
import json
import sys
from train import getW2V
def testing(path_test,config_feature,path_ckpt,config_train,ckpt_file='',mode='lr',name=''):
    with open(path_test, 'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    XTst = [getFeature(s[0], config_feature) for s in S]
    yTst = [int(s[1]) for s in S]
    print('number of positive/negative samples of testSet is {}/{}'.format(sum(yTst), len(yTst) - sum(yTst)))
    feature_dim = len(XTst[0])
    print('feature dim is %d'%feature_dim)
    config_train.feature_dim =feature_dim
    if 'dense' in mode:
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(
            config_train)
    else:
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(feature_dim)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    if len(ckpt_file)==0:
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
    with open('data/test_predict_'+mode+name+'.txt','w') as f:
        f.write('\n'.join(X))
    thr0 = [0.1*i for i in range(10)]
    thr0 += [0.91+0.01*i for i in range(9)]
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
        R.append('\t'.join(['%0.2f'%thr,'%0.4f'%acc,'%0.4f'%pre,'%0.4f'%rec]))
        print('\n'.join(R))
    print('auc=%0.4f'%auc)
    R.append('auc=%0.4f'%auc)
    with open('data/test_result-'+mode+name+'.txt','w') as f:
        f.write('\n'.join(R))
def modelStack(models):
    S = []
    L = []
    T = []
    for model in models:
        with open('data/test_predict_'+model+'.txt','r') as f:
            s = f.read().strip().split('\n')[1:]
            s = [ss.split('\t') for ss in s]
            scores = [float(ss[0]) for ss in s]
            labels = [int(ss[1]) for ss in s]
            texts = [ss[2] for ss in s]
        S.append(scores)
        L = labels
        T = texts
    S = np.array(S)
    S = np.mean(S, axis=0)
    A = ['预测值\t实际值\t文本']
    for i in range(len(S)):
        A.append('\t'.join(['%0.4f'%S[i],str(L[i]),texts[i]]))
    with open('data/test_predict_'+'all'+'.txt','w') as f:
        f.write('\n'.join(A))
    y_p = S
    yTst = L
    auc = calAUC(y_p, yTst)
    thr0 = [0.1 * i for i in range(10)]
    R = ['\t'.join(['阈值', '准确率', '精度', '召回率'])]
    for thr in thr0:
        yp = [int(t > thr) for t in y_p]
        TP = sum([yp[i] == yTst[i] for i in range(len(yp)) if yp[i] == 1])
        TN = sum([yp[i] == yTst[i] for i in range(len(yp)) if yp[i] == 0])
        FP = sum([yp[i] != yTst[i] for i in range(len(yp)) if yp[i] == 1])
        FN = sum([yp[i] != yTst[i] for i in range(len(yp)) if yp[i] == 0])
        acc = float(TP + TN) / len(yp)
        pre = float(TP) / (TP + FP)
        rec = float(TP) / (TP + FN)
        R.append('\t'.join(['%0.2f' % thr, '%0.4f' % acc, '%0.4f' % pre, '%0.4f' % rec]))
        print([thr, acc, pre, rec])
    R.append('%0.4f' % auc)
    with open('data/test_result-' + 'all' + '.txt', 'w') as f:
        f.write('\n'.join(R))
def main(mode,path_test,name,ckpt_file=''):
    if mode=='all':
        modelStack(['lr','lr-word','lr-w2v-word','word','lr-w2v'])
        return
    path_train = 'data/train.txt'
    #path_test = 'data/test.txt'
    path_idf = 'data/idf_char.json'
    path_vocab = 'data/vocab.txt'
    path_idf_word = 'data/idf_word.json'
    path_vocab_word = 'data/vocab_word.txt'
    path_w2v = '/search/odin/guobk/streaming/vpa/word2vec128/model-mean'
    path_ckpt = mode + '-ckpt'+'-used'
    config_feature = {}
    config_feature['use_sentLen'] = True
    config_feature['use_puncExist'] = True
    if 'lr' in mode:
        config_feature['use_charIdf'] = True
        config_feature['use_char'] = True
        with open(path_idf, 'r') as f:
            idf = json.load(f)
        with open(path_vocab, 'r') as f:
            vocab = f.read().strip().split('\n')
        config_feature['idf'] = idf
        config_feature['charList'] = vocab
    if 'w2v' in mode:
        config_feature['use_w2v'] = True
        config_feature['w2v'] = getW2V(path_w2v)
        config_feature['dim_v'] = 128
    if 'word' in mode:
        config_feature['use_wordIdf'] = True
        config_feature['use_word'] = True
        with open(path_idf_word, 'r') as f:
            idf = json.load(f)
        with open(path_vocab_word, 'r') as f:
            vocab = f.read().strip().split('\n')
        config_feature['idf_word'] = idf
        config_feature['wordList'] = vocab
    config_train = Config_train()
    config_train.keep_prob = 1.0
    testing(path_test, config_feature, path_ckpt, config_train,ckpt_file=ckpt_file,mode=mode,name=name)
if __name__=='__main__':
    mode,path_test,name,ckpt_file = sys.argv[1:]
    main(mode,path_test,name,ckpt_file=ckpt_file)