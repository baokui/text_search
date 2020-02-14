import numpy as np
def getSynonym(topn=5,path_mutiReplace='../data/beauty.table.txt',path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'):
    with open(path_mutiReplace,'r') as f:
        S = f.read().strip().split('\n')
    with open(path_w2v,'r') as f:
        s = f.read().strip().split('\n')
    Words = []
    Vectors = []
    for t in s:
        a = t.split(' ')
        Words.append(a)
        Vectors.append([float(a[i]) for i in range(1,len(a))])
    Vectors = np.array(Vectors)
    T = []
    for t in S:
        a = t.split('\t')
        w = a[3].strip()
        syn = []
        if w in Words:
            v0 = Vectors[Words.index(w)]
            sim = np.dot(v0,Vectors)
            x = [[Words[i],sim[i]] for i in range(len(Words))]
            x = sorted(x,key=lambda x:-x[1])
            syn = [x[i][1] for i in range(1,topn+1)]
        a = a+syn
        T.append(a)
    with open('../data/beauty.table1.txt','w') as f:
        f.write('\n'.join(T))