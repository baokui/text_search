import numpy as np
def getSynonym(topn=10,path_mutiReplace='../data/beauty.table.txt',path_w2v = '/search/odin/guobk/streaming/vpa/vpa-data-process/UserInput/word2vec128/model-mean'):
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
        syn = []
        if w in Words:
            v0 = Vectors[:,Words.index(w)]
            v0 = v0.reshape((1,len(v0)))
            sim = np.dot(v0,Vectors)
            x = [[Words[i],sim[0][i]] for i in range(len(Words))]
            x = sorted(x,key=lambda x:-x[1])
            syn = [x[i][0]+'/'+'%0.4f'%x[i][1] for i in range(1,topn+1)]
            print('\t'.join([x[i][0] for i in range(topn+1)]))
        a = a+syn
        T.append(a)
    T = ['\t'.join(t) for t in T]
    with open('../data/beauty.table1.txt','w') as f:
        f.write('\n'.join(T))
    print('re-sort for symwords....')
    scId = ''
    sc0 = ''
    sc1 = ''
    S = []
    words_origin = []
    words_new = []
    for t in T:
        s = t.split('\t')
        if s[0]!=scId and scId!='':
            if len(words_new)>0:
                words_new1 = [w for w in words_new if w.split('/')[0] not in words_origin]
                if len(words_new1)>0:
                    D = {}
                    for w in words_new1:
                        x = w.split('/')
                        if x[0] in D:
                            D[x[0]] = min(D[x[0]], float(x[1]))
                        else:
                            D[x[0]] = float(x[1])
                    D = [(k, D[k]) for k in D]
                    D = sorted(D, key=lambda x: -x[1])
                    words_new1 = [k[0] + '/' + str(k[1]) for k in D]
                    S.append(scId+'\t'+sc0+'\t'+sc1+'\t'+'#'.join(words_origin)+'\n'+scId+'\t'+sc0+'\t'+sc1+'\t'+'#'.join(words_new1)+'\n')
            words_origin = []
            words_new = []
        scId = s[0]
        sc0 = s[1]
        sc1 = s[2]
        words_origin.append(s[3])
        words_new.extend(s[4:])
    if s[0] != scId and scId != '' and len(words_new) > 0:
        S.append(scId + '\t' + sc0 + '\t' + sc1 + '\t' + '#'.join(words_origin) + '\n' + '#'.join(words_new))
    with open('../data/beauty.table2.txt','w') as f:
        f.write('\n'.join(S))
def main():
    getSynonym(topn=10)
if __name__=="__main__":
    main()