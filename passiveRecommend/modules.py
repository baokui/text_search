import jieba
import numpy as np
def getFeature(Str,config):
    x = []
    if config['use_charIdf']:
        t = getCharIdf(Str,config['idf'])
        x.extend(t)
    if config['use_sentLen']:
        x.extend([len(Str)])
    if config['use_puncExist']:
        t = getPunExist(Str)
        x.extend(t)
    if config['use_char']:
        t = getCharFeature(Str,config['charList'])
        x.extend(t)
    if 'use_w2v' in config and config['use_w2v']:
        t = getSentV(Str,config['w2v'],config['dim_v'])
        x.extend(t)
    return x
def getSentV(Str,D,dim):
    s = list(jieba.cut(Str))
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
def calAUC(prob, labels):
    f = list(zip(prob, labels))
    rank = [values2 for values1, values2 in sorted(f, key=lambda x: x[0])]
    rankList = [i + 1 for i in range(len(rank)) if rank[i] == 1]
    posNum = 0.0
    negNum = 0.0
    for i in range(len(labels)):
        if (labels[i] == 1):
            posNum += 1
        else:
            negNum += 1
    auc = (sum(rankList) - (posNum * (posNum + 1)) / 2) / (posNum * negNum)
    # print(auc)
    return auc

