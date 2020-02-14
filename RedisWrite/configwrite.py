import redis
import json
import xlrd
import jieba
import numpy as np
redis_list= [["b.redis.sogou", 2971, "sogouvpaintention"],["b.redis.sogou", 2972, "sogouvpaintention"], ["b.redis.sogou", 2973, "sogouvpaintention"], ["b.redis.sogou", 2974, "sogouvpaintention"], ["b.redis.sogou", 2981, "sogouvpaintention"], ["b.redis.sogou", 2982 ,"sogouvpaintention"] , ["b.redis.sogou", 2983, "sogouvpaintention"], ["b.redis.sogou", 2984, "sogouvpaintention"]]
def SynonymWordsWrite(path_synwords='RedisWrite/synwords.txt',key='textsearch_synwords',k=0,expire=7*24*60*60):
    host = redis_list[k][0]
    passwd = redis_list[k][2]
    port = redis_list[k][1]
    with open(path_synwords,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    D = {}
    for w in s:
        words = w.split('#')
        for i in range(len(words)):
            D[words[i]]=[words[j] for j in range(len(words)) if j!=i]
    Str = json.dumps(D)
    r=redis.Redis(host=host,password=passwd,port=port,db=1) #默认端口号如果不修改就是6379，db指定用哪个数据库
    #增删改查，这些操作都是针对string类型的
    r.set(key,Str) #数据库里面新增一个值,修改也是set
    r.expire(key,expire)
    r=redis.Redis(host=host,password=passwd,port=port,db=1) #默认端口号如果不修改就是6379，db指定用哪个数据库
    S = r.get(key)
    D = json.loads(S)
    return S,D
class TFIDF(object):
    """
    手写一个TFIDF统计类,只写最简单的一个实现
    """
    def __init__(self, corpus):
        """
        初始化
        self.vob:词汇个数统计，dict格式
        self.word_id:词汇编码id，dict格式
        self.smooth_idf：平滑系数，关于平滑不多解释了
        :param corpus:输入的语料
        """
        self.word_id = {}
        self.vob = {}
        self.inv_id_word = {}
        self.corpus = corpus
        self.smooth_idf = 0.01

    def fit_transform(self, corpus):
        pass
    def get_vob_fre(self):
        """
        计算文本特特征的出现次数，也就是文本频率term frequency，但是没有除token总数，因为后面bincount计算不支持float
        :return: 修改self.vob也就是修改词频统计字典
        """
        # 统计各词出现个数
        id = 0
        for single_corpus in self.corpus:
            if isinstance(single_corpus, list):
                pass
            if isinstance(single_corpus, str):
                single_corpus = single_corpus.strip("\n").split(" ")
            for word in single_corpus:
                if word not in self.vob:
                    self.vob[word] = 1
                    self.word_id[word] = id
                    self.inv_id_word[id] = word
                    id += 1
                else:
                    self.vob[word] += 1
        # 生成矩阵
        X = np.zeros((len(self.corpus), len(self.vob)))
        for i in range(len(self.corpus)):
            if isinstance(self.corpus[i], str):
                single_corpus = self.corpus[i].strip("\n").split(" ")
            else:
                single_corpus = self.corpus[i]
            for j in range(len(single_corpus)):
                feature = single_corpus[j]
                feature_id = self.word_id[feature]
                X[i, feature_id] = self.vob[feature]
        return X.astype(int)  # 需要转化成int
    def get_tf_idf(self):
        """
        计算idf并生成最后的TFIDF矩阵
        :return:
        """
        X = self.get_vob_fre()
        n_samples, n_features = X.shape
        df = []
        for i in range(n_features):
            """
            这里是统计每个特征的非0的数量，也就是逆文档频率指数的分式中的分母，是为了计算idf
            """
            df.append(n_samples - np.bincount(X[:,i])[0])
        df = np.array(df)
        # perform idf smoothing if required
        df += int(self.smooth_idf)
        n_samples += int(self.smooth_idf)
        idf = np.log(n_samples / df)  # 核心公式
        # print(self.vob)
        # print(self.word_id)
        return X*idf/len(self.vob)
def model_tfidf(corpus):
    words = {}
    N = 0
    TF = []
    for corp in corpus:
        tf = {}
        n = 0
        for w in corp:
            if w in words:
                words[w]+=1
            else:
                words[w] = 0
            N+=1
            if w in tf:
                tf[w]+=1
            else:
                tf[w] = 1
            n+=1
        TF.append({w:tf[w]/n for w in tf})
    keys = list(words.keys())
    id2word = {i:keys[i] for i in range(len(keys))}
    word2id = {keys[i]:i for i in range(len(keys))}
    X = np.zeros((len(corpus),len(words)))
    for i in range(len(corpus)):
        for j in range(len(corpus[i])):
            X[i][word2id[corpus[i][j]]] = 1
    M = np.sum(X,axis=0)
    tfidf = [{c:TF[i][c]*np.log(len(corpus)/M[word2id[c]]) for c in corpus[i]} for i in range(len(corpus))]
    return tfidf
def get_idf(corpus):
    words = {}
    N = 0
    TF = []
    for corp in corpus:
        tf = {}
        n = 0
        for w in corp:
            if w in words:
                words[w] += 1
            else:
                words[w] = 0
            N += 1
            if w in tf:
                tf[w] += 1
            else:
                tf[w] = 1
            n += 1
        TF.append({w: tf[w] / n for w in tf})
    keys = list(words.keys())
    id2word = {i: keys[i] for i in range(len(keys))}
    word2id = {keys[i]: i for i in range(len(keys))}
    X = np.zeros((len(corpus), len(words)))
    for i in range(len(corpus)):
        for j in range(len(corpus[i])):
            X[i][word2id[corpus[i][j]]] = 1
    M = np.sum(X, axis=0)
    idf = {c: np.log(len(corpus) / M[word2id[c]]) for c in words}
    return idf
def keywords(path_content="D:\\项目\\输入法\\神配文数据\\祝福语MVP文件.xlsx"):
    # 读取excel表格
    workbook = xlrd.open_workbook(path_content)  # 打开excel文件
    table = workbook.sheet_by_name('Sheet1')  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列

    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    Labels_1 = {}
    Labels_2 = {}
    popul = {}
    style = {}
    corpus0 = []
    for i in range(1,len(res)):
        str0 = list(jieba.cut(res[i][0].lower()))
        corpus0.append(str0)
        if res[i][2]!='':
            if res[i][2] in Labels_1:
                Labels_1[res[i][2]] = Labels_1[res[i][2]]+str0
            else:
                Labels_1[res[i][2]] = str0
        if res[i][3]!='':
            if res[i][3] in Labels_2:
                Labels_2[res[i][3]] = Labels_2[res[i][3]]+str0
            else:
                Labels_2[res[i][3]] = str0
        for j in range(4,9):
            if res[i][j]=='':
                continue
            if res[i][j] in popul:
                popul[res[i][j]] = popul[res[i][j]] + str0
            else:
                popul[res[i][j]] = str0
        for j in range(9,14):
            if res[i][j]=='':
                continue
            if res[i][j] in style:
                style[res[i][j]] = style[res[i][j]] + str0
            else:
                style[res[i][j]] = str0
    D = {}
    keys = list(Labels_1.keys())
    corpus = [Labels_1[key] for key in keys]
    tfidf = model_tfidf(corpus)
    d = {}
    for i in range(len(keys)):
        t = [(key, tfidf[i][key]) for key in tfidf[i]]
        t = sorted(t, key=lambda x: -x[-1])
        keywords = [t[k][0] for k in range(10)]
        d[keys[i]] = keywords
    D['一级标签'] = d

    keys = list(Labels_2.keys())
    corpus = [Labels_2[key] for key in keys]
    tfidf = model_tfidf(corpus)
    d = {}
    for i in range(len(keys)):
        t = [(key, tfidf[i][key]) for key in tfidf[i]]
        t = sorted(t, key=lambda x: -x[-1])
        keywords = [t[k][0] for k in range(10)]
        d[keys[i]] = keywords
    D['二级标签'] = d

    keys = list(popul.keys())
    corpus = [popul[key] for key in keys]
    tfidf = model_tfidf(corpus)
    d = {}
    for i in range(len(keys)):
        t = [(key, tfidf[i][key]) for key in tfidf[i]]
        t = sorted(t, key=lambda x: -x[-1])
        keywords = [t[k][0] for k in range(10)]
        d[keys[i]] = keywords
    D['人群'] = d

    keys = list(style.keys())
    corpus = [style[key] for key in keys]
    tfidf = model_tfidf(corpus)
    d = {}
    for i in range(len(keys)):
        t = [(key, tfidf[i][key]) for key in tfidf[i]]
        t = sorted(t, key=lambda x: -x[-1])
        keywords = [t[k][0] for k in range(10)]
        d[keys[i]] = keywords
    D['风格'] = d

    with open('contentProcess/keywords.json','w',encoding='utf-8') as f:
        json.dump(D,f,ensure_ascii=False,sort_keys=True, indent=4)

    IDF = get_idf(corpus0)
    idx = 0
    key = 'text_search_wordIDF'
    #host = redis_list[idx][0]
    #passwd = redis_list[idx][2]
    #port = redis_list[idx][1]
    host = "d.redis.sogou"
    port = 2333
    passwd = "yxkZErk1td3idmO3"
    db = 0
    expire = 7*24*60*60
    r = redis.Redis(host=host, password=passwd, port=port, db=0)
    S = json.dumps(IDF, ensure_ascii=False)
    r.set(key,S)
    r.expire(key, expire)