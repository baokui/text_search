import jieba
import numpy as np
import json
def getFeature(Str,words,config,w2v):
    x = np.zeros((config['len_feature'],))
    idx = 0

    #提取基于字符的IDF特征
    x[idx] = getCharIdf(Str,config['idf_char'])
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
    t = getSentV(words,w2v,config['dim_v'])
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
    return r
def getCharIdf(Str,idf):
    r = 0
    for s in Str:
        if s in idf:
            r+=idf[s]
        else:
            r+=idf['<UNK>']
    r = r/float(len(Str))
    return r
def getCharFeature(Str,charList):
    r = [0 for _ in range(len(charList))]
    for s in Str:
        if s in charList:
            r[charList.index(s)] = 1.0
        else:
            r[charList.index('<UNK>')] = 1.0
    return r
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
def getConfig(path_target,path_ckpt):
    config = {}
    config['len_feature'] = 8085
    with open('./data/idf_char.json','r') as f:
        config['idf_char'] = json.load(f)
    with open('./data/vocab.txt', 'r') as f:
        config['charList'] = f.read().strip().split('\n')
    with open('./data/vocab_word.txt', 'r') as f:
        config['wordList'] = f.read().strip().split('\n')
    with open('./data/idf_word.json','r') as f:
        config['idf_word'] = json.load(f)
    config['w2v'] = './data/model-mean'
    config['dim_v'] = 128
    from modeling import simple_lr,simple_lr_dense
    import tensorflow as tf
    if 'dense' in path_ckpt:
        from train import Config_train
        config_train = Config_train()
        config_train.feature_dim = config['len_feature']
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(
            config_train)
    else:
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(config['len_feature'])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    saver.restore(session, ckpt_file)
    reader = tf.train.NewCheckpointReader(ckpt_file)
    all_variables = reader.get_variable_to_shape_map()
    if 'dense' in path_ckpt:
        w0 = reader.get_tensor('dense/kernel')
        w0 = reader.get_tensor("parameters/Variable")
    else:
        w0 = reader.get_tensor("parameters/Variable")
        b0 = reader.get_tensor("parameters/Variable_1")
        w = list(w0[:,0])
        b = b0[0][0]
        config['weight_w'] = ['%0.8f'%t for t in w]
        config['weight_b'] = '%0.8f'%b
        config['threshold'] = '0.5'
    with open(path_target,'w') as f:
        json.dump(config,f,ensure_ascii=False,indent=4)
def predict(inputStr,words,config,w2v):
    x = getFeature(inputStr, words, config,w2v)
    w = config['weight_w']
    b = config['weight_b']
    logits = sum([w[i]*x[i] for i in range(len(w))])+b
    p = 1/(1+np.exp(-logits))
    return p
def main(inputStr,path_config='ModelConfig.json',path_w2v='w2v.file'):
    # 导入模型各参赛
    with open(path_config,'r') as f:
        config = json.load(f)
    config['weight_w'] = [float(t) for t in config['weight_w']]
    config['weight_b'] = float(config['weight_b'])
    config['threshold'] = float(config['threshold'])
    # 导入词向量
    w2v = getW2V(path_w2v)
    # 对输入字符串分词，这个intention里应该有分词结果
    words = list(jieba.cut(inputStr))
    # 预测
    y = predict(inputStr,words,config,w2v)
    r = int(y>config['threshold'])
    print('input string:%s\npredict value:%0.4f\nresult:%d'%(inputStr,y,r))
    # demo结果：
    # input string:你怎么一回事
    # predict value:0.7924
    # result:1
if __name__=='__main__':
    main('你怎么一回事', path_config='ModelConfig.json', path_w2v='w2v.file')