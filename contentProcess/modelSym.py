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
    path0 = "data"
    files = os.listdir(path0)
    N = 0
    n = 0
    thr = 0.6
    for file in files:
        print(os.path.join(path0,file))
        f_r = open(os.path.join(path0,file),'r')
        for line in f_r:
            s = line.strip().split('\t')[3]
            N+=1
            if N%10000==0:
                print("read %d lines and extracted %d sentences"%(N,n))
            if s in Words:
                continue
            if len(s.decode('utf-8'))>10:
                continue
            w,sim = simCompute(s)
            if sim>thr:
                f.write(w+'\t'+s+'\t'+str(sim)+'\n')
                n+=1
        f_r.close()
    f.close()
def sim_edit(s1, s2):
    # 矩阵的下标得多一个
    len_str1 = len(s1) + 1
    len_str2 = len(s2) + 1
    # 初始化了一半  剩下一半在下面初始化
    matrix = [[0] * (len_str2) for i in range(len_str1)]
    for i in range(len_str1):
        for j in range(len_str2):
            if i == 0 and j == 0:
                matrix[i][j] = 0
            # 初始化矩阵
            elif i == 0 and j > 0:
                matrix[0][j] = j
            elif i > 0 and j == 0:
                matrix[i][0] = i
            # flag
            elif s1[i - 1] == s2[j - 1]:
                matrix[i][j] = min(matrix[i - 1][j - 1], matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
            else:
                matrix[i][j] = min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
    return 1 - matrix[len_str1 - 1][len_str2 - 1]/float(max(len(s1),len(s2)))
def sim_jacard(s1,s2):
    v1 = set(list(s1))
    v2 = set(list(s2))
    r = len(v1 & v2)/float(len(v1 | v2))
    return r
def simlar(s0,s1):
    s0 = s0.decode('utf-8')
    s1 = s1.decode('utf-8')
    d = [sim_edit(s0,s1),sim_jacard(s0,s1)]
    r = np.mean(d)
    return r
def wash_stringDis():
    with open('result.txt','r') as f:
        s = f.read().strip().split('\n')
    S = [t.split('\t') for t in s]
    T = []
    for i in range(len(S)):
        t = S[i]
        T.append([t[0],t[1],t[2],simlar(t[0],t[1])])
        if i%1000==0:
            print(i,len(S))
    T = sorted(T,key=lambda x:-x[-1])
    L = {}
    S = []
    i=0
    for t in T:
        i+=1
        if t[1] in L:
            continue
        S.append('\t'.join([t[0],t[1],'%0.6f'%float(t[2]),'%0.6f'%(t[3])]))
        L[t[1]]=0
        if i%10000==0:
            print(i,len(L))
    with open('result1.txt','w') as f:
        f.write('\n'.join(S))
def txt2excel():
    path_result='D:\\项目\\输入法\\神配文数据\\result_all_100.txt'
    path_mutiReplace = 'data/beauty.table.txt'
    with open(path_mutiReplace,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    D = {}
    for ss in s:
        t = ss.split('\t')
        D[t[-1]] = t[0]
    with open(path_result,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')[2:]
    S = []
    for ss in s:
        S.append(D[ss.split('\t')[0]]+'\t'+ss)
    S = ['Id\t原触发词\t近义词/句\t词/句向量相似度\t字符串相似度\t累计出现频数']+S
    import xlwt
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('sheet1')
    # 写入excel
    # 参数对应 行, 列, 值
    for i in range(len(S)):
        s = S[i].split('\t')
        for j in range(len(s)):
            worksheet.write(i, j, label=s[j])
    # 保存
    workbook.save('data/symResult.xlsx')

if __name__=='__main__':
    symInput()