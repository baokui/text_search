import jieba
import numpy as np
def getSynonym(path_mutiReplace='../data/beauty.table.txt',path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'):
    with open(path_mutiReplace,'r') as f:
        S = f.read().strip().split('\n')
    with open(path_w2v,'r') as f:
        s = f.read().strip().split('\n')
    Words = []
    Vectors = []
    for t in s:
        a = t.split(' ')
        Words.append(a[0])
        Vectors.append([float(a[i]) for i in range(1,len(a))])
    Vectors = np.array(Vectors)
    T = []
    Vectors = Vectors.transpose()
    for t in S:
        a = t.split('\t')
        w = a[3].strip()
        w = w.replace('\\n','')
        syn = []
        if w in Words:
            v0 = Vectors[:,Words.index(w)]
            v0 = v0.reshape((1,len(v0)))
        else:
            ws = list(jieba.cut(w))
            v0 = np.zeros((1,128))
            vv = []
            for ww in ws:
                if ww in Words:
                    vv0 = Vectors[:, Words.index(ww)]
                    vv.append(v0.reshape((1, len(vv0))))
            if len(vv)>0:
                v0 = np.mean(np.array(vv),axis=0)
                v0 = v0.reshape((1, len(v0)))
                v0 = v0/np.linalg.norm(v0)
        str_v = ['%0.4f'%tt for tt in v0]
        T.append(t+'\t'+' '.join(str_v))
    with open('../data/beauty.table_vector.txt','w') as f:
        f.write('\n'.join(T))
