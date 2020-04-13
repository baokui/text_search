import jieba
import numpy as np
def getFeature(Str,words,config):
    x = np.zeros((config['len_feature'],))
    idx = 0

    #提取基于字符的IDF特征
    x[idx] = getCharIdf(Str,config['idf'])
    idx += 1

    #提取字符串长度特征
    x[idx] = len(Str)
    idx += 1

    #判断字符串中是否存在标点
    t = getPunExist(Str)
    x[idx] = t
    idx += 1

    #提取字符特征，以0-1形式表示
    t = getCharFeature(Str,config['charList'])
    x[idx:idx+len(t)]=t
    idx += len(t)

    #提取中文词特征，以0-1形式表示
    t = getCharFeature(words,config['wordList'])
    x[idx:idx + len(t)] = t
    idx += len(t)

    #提取基于词的IDF特征
    x[idx] = getCharIdf(words,config['idf_word'])
    idx += 1

    #提取word2vector特征，dim=128
    t = getSentV(words,config['w2v'],config['dim_v'])
    x[idx:idx + len(t)] = t
    idx += len(t)

    return x
def getSentV(Str,D,dim):
    s = Str
    v = []
    for t in s:
        if t in D:
            v.append(D[t])
    if len(v)==0:
        return [0 for i in range(dim)]
    v = np.array(v)
    v = np.mean(v,axis=0)
    return list(v)
def getPunExist(Str,punc=[]):
    if len(punc)==0:
        punc = '.,?!。，？！'
    r = 0
    for s in Str:
        if s in punc:
            r = 1
            break
    return [r]
def getCharIdf(Str,idf):
    r = 0
    for s in Str:
        if s in idf:
            r+=idf[s]
        else:
            r+=idf['<UNK>']
    r = r/float(len(Str))
    return [r]
def getCharFeature(Str,charList):
    r = [0 for _ in range(len(charList))]
    for s in Str:
        if s in charList:
            r[charList.index(s)] = 1.0
        else:
            r[charList.index('<UNK>')] = 1.0
    return r
def predict(inputStr):
    x = getFeature(inputStr, config_feature)
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
    with open('data/test_predict_'+mode+'.txt','w') as f:
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
    R.append('%0.4f'%auc)
    with open('data/test_result-'+mode+'.txt','w') as f:
        f.write('\n'.join(R))