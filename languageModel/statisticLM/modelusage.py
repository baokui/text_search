import jieba
import json
import numpy as np
def condition_prob():
    f_w = open('ngram_all3/part-00000-prob','w')
    f_r = open('ngram_all3/part-00000','r')
    for line in f_r:
        t = line.split('\t')
        if len(t)!=2:
            continue

    f_r.close()
    f_w.close()
def modelDict():
    f = open('ngram_all_prob/part-00000', 'r')
    D = {}
    k = 0
    for line in f:
        t = line.strip().split('\t')
        D[t[0]] = float(t[-1])
        if len(D)==5000000:
            json.dump(D,open('ngram_all_prob/'+str(k)+'.json','w'))
            k = k+1
            print(k)
            D = {}
    json.dump(D, open('ngram_all_prob/' + str(k) + '.json', 'w'))
def predict(T):
    f = open('ngram_all_prob/part-00000','r')
    D = {}
    k = 0
    for line in f:
        t = line.strip().split('\t')
        if t[0] in T:
            D[t[0]] = t[-1]
            T.remove(t[0])
            print(D)
        if k%10000000==0:
            print(k/352178780.0)
        k += 1
    f.close()
    return D
def predict1(T):
    R = {}
    for i in range(71):
        D0 = json.load(open('ngram_all_prob/' + str(i) + '.json', 'r'))
        D = {k.encode('utf-8'):D0[k] for k in D0}
        for t in T:
            if t in D and t not in R:
                R[t] = D[t]
        print(R)
        print(i)
    return R
def computePro(T,D):
    r = 1
    for t in T:
        r = r*D[t]
    if r==0:
        R = 100000
    else:
        R = pow(r,-1.0/len(T))
    return r,R
def test1():
if 1:
    n = 3
    s = "我今天不用去上班啦"
    s1 = "我今天不用去上啦"
    s = list(jieba.cut(s))
    s1 = list(jieba.cut(s1))
    T = []
    for i in range(len(s)-n+1):
        T.append('('+','.join(s[i:i+3])+')')
    T1 = []
    for i in range(len(s1) - n + 1):
        T1.append('(' + ','.join(s1[i:i + 3]) + ')')

    TT = [t for t in T] + [t for t in T1 if t not in T]
    D = predict1(TT)
    k = [D[t] for t in T]
    k1 = [D[t] for t in T1]
    computePro(T, D)
    computePro(T1, D)
def test2():
    with open('data/test_6.txt','r') as f:
        s = f.read().strip().split('\n')
    s = s[:10000]
    S = []
    G = {}
    for i in range(10000):
        t = s[i].split('\t')[0].split(' ')
        ngram = []
        for j in range(len(t) - 2):
            k = '(' + ','.join(t[j:j + 3]) + ')'
            if k not in G:
                G[k] = 0
            ngram.append(k)
        S.append([ngram,int(s[i].split('\t')[1])])
        if i%100==0:
            print(i)
    R = predict1(G)
    p = [R[k] for k in R]
    pm = min(p)*0.1
    R1 = {k:pm for k in G if k not in R}
    R.update(R1)
    A = []
    for i in range(len(S)):
        T = S[i][0]
        p,q = computePro(T, R)
        A.append([s[i],p,q])
        if i%100==0:
            print(i)
    B = []
    for a in A:
        if a[-1]>100000:
            a[-1] = 100000
        B.append(a)
    labels = []
    probs = []
    for b in B:
        labels.append(int(b[0].split('\t')[-1]))
        probs.append(1-b[-1]/100000)