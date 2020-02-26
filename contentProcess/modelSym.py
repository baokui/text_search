import jieba
import numpy as np
import os
def getSynonym(path_mutiReplace='../data/beauty.table.txt',path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'):
    #path_mutiReplace = '../data/beauty.table.txt'
    #path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'
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
    n = 0
    for t in S:
        if n%1000==0:
            print('get-word-%d'%n)
        n+=1
        a = t.split('\t')
        w = a[3].strip()
        w = w.replace('\\n','')
        syn = []
        if w in Words:
            v0 = Vectors[:,Words.index(w)]
        else:
            ws = list(jieba.cut(w))
            v0 = np.zeros((128,))
            vv = []
            for ww in ws:
                if ww.encode('utf-8') in Words:
                    vv0 = Vectors[:, Words.index(ww.encode('utf-8'))]
                    vv.append(vv0)
            if len(vv)>0:
                v0 = np.mean(np.array(vv),axis=0)
                v0 = v0/np.linalg.norm(v0)
        str_v = ['%0.4f'%v0[i] for i in range(len(v0))]
        T.append(t+'\t'+' '.join(str_v))
    with open('../data/beauty.table_vector.txt','w') as f:
        f.write('\n'.join(T))
def symInput():
    def simCompute(s):
        ws = list(jieba.cut(s))
        v0 = np.zeros((128,))
        vv = []
        for ww in ws:
            if ww.encode('utf-8') in w2v:
                vv0 = w2v[ww.encode('utf-8')]
                vv.append(vv0)
        if len(vv) > 0:
            v0 = np.mean(np.array(vv), axis=0)
            v0 = v0 / np.linalg.norm(v0)
        v0 = v0.reshape((1, 128))
        sim = np.dot(v0, Vectors)
        sim = sim.reshape((len(Words),))
        idx = np.argmax(sim)
        w = Words[idx]
        r = max(sim)
        return w,r
    path_mutiReplace = '../data/beauty.table_vector.txt'
    path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'
    with open(path_mutiReplace, 'r') as f:
        S = f.read().strip().split('\n')
    with open(path_w2v, 'r') as f:
        s = f.read().strip().split('\n')
    w2v = {}
    for t in s:
        a = t.split(' ')
        w2v[a[0]] = [float(a[i]) for i in range(1, len(a))]
    Words = []
    Vectors = []
    for s in S:
        t = s.split('\t')
        Words.append(t[-2])
        Vectors.append(np.array([float(tt) for tt in  t[-1].split(' ')]).reshape((128,)))
    Vectors = np.array(Vectors)
    Vectors = Vectors.transpose()

    f = open('result.txt','w')
    path0 = "data/20200220"
    files = os.listdir(path0)
    N = 0
    n = 0
    thr = 0.95
    for file in files:
        for p in range(5):
            print(os.path.join(path0,file,'part-0000'+str(p)))
            f_r = open(os.path.join(path0,file,'part-0000'+str(p)),'r')
            for line in f_r:
                s = line.strip()
                N+=1
                if N%10000==0:
                    print("read %d lines and extracted %d sentences"%(N,n))
                if s in Words:
                    continue
                w,sim = simCompute(s)
                if sim>thr:
                    f.write(w+'\t'+s+'\n')
                    n+=1
            f_r.close()
    f.close()
if __name__=='__main__':
    symInput()