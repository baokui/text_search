import redis
import json
import random
def word_trim(s0):
    stopwords = [" ","　"," ",",","，",".","。","、","!","！","?","？",";","；","~","～","·","·",".","…","-","#_","—","+","=","'","\"","‘","’","“","”","*","&","^","%","$","/","\\","@"]
    sn = s0
    for t in stopwords:
        sn = sn.replace(t,'')
    return sn
def computeDis(s,keys,set_keys):
    words = []
    if s in keys:
        words = [s]
        t = [1]
    else:
        t = []
        s = set(s)
        for i in range(len(keys)):
            d = 2*len(s & set_keys[i])/(len(s)+len(set_keys[i]))
            if d>0.6:
                words.append(keys[i])
                t.append(d)
    if len(words)==0:
        return [],[]
    m = float(sum(t))
    probs = ['%0.6f'%(tt/m) for tt in t]
    return words,probs


def createModel(path_data='D:\\项目\\输入法\\数据处理\\text_search\\nnlm\\result-snnlm.txt'):
    with open(path_data,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    S = [ss.split('\t') for ss in s]
    D0 = {}
    for s in S:
        t = [ss.split('#') for ss in s[1:]]
        t = [(tt[0],int(tt[1])) for tt in t]
        m = float(sum([tt[1] for tt in t]))
        words = [tt[0] for tt in t]
        probs = ['%0.6f'%(tt[1]/m) for tt in t]
        D0[s[0]] = json.dumps({'words':words,'probs':probs})
    keys = list(D0.keys())
    set_keys = [set(k) for k in keys]
    D1 = {}
    n = 0
    for s in S:
        if n%1000==0:
            print(n,len(S),len(D1))
        n+=1
        words, probs = computeDis(s[0], keys,set_keys)
        D1[s[0]] = json.dumps({'words':words,'probs':probs})
        t = [ss.split('#')[0] for ss in s[1:]]
        for i in range(min(5,len(t))):
            tt = t[i]
            if tt in D1:
                continue
            words,probs = computeDis(tt,keys,set_keys)
            if words:
                D1[tt] = json.dumps({'words': words, 'probs': probs})
    json.dump(D1, open('D_simi.json', 'w', encoding='utf-8'))
    json.dump(D0, open('D_next.json', 'w', encoding='utf-8'))

def modelWrite(host,port,password):
    conn = redis.Redis(host=host, port=port,password=password)
    pipe = conn.pipeline()
    key = 'test0323_guo'
    value = 'abc'
    pipe.set(key,value)
    pipe.expire(key,7 * 24 * 60 * 60)
def modelpredict(D_simi,D_next,inputStr=['怎么了','你好','讨厌'],maxNext=5,maxChoice=10):
    output = []
    for s in inputStr:
        S = []
        s0 = s
        S.append(s0)
        for i in range(maxNext):
            if s0 in D_next:
                p = [float(tt) for tt in D_next[s0]['probs']]
                w = D_next[s0]['words']
                t = random.choices(w[:maxChoice],p[:maxChoice])[0]
                S.append(t)
            elif s0 in D_simi:
                p = [float(tt) for tt in D_simi[s0]['probs']]
                w = D_simi[s0]['words']
                t0 = random.choices(w, p)[0]
                p = [float(tt) for tt in D_next[t0]['probs']]
                w = D_next[t0]['words']
                t = random.choice(w[maxChoice], p[:maxChoice])[0]
                S.append(t)
            else:
                break
        output.append('，'.join(S))
    return output
def demo():
    inputStr = ['怎么了', '你好', '讨厌']
    path_next = 'D_next.json'
    path_simi = 'D_simi.json'
    D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
    D_next = json.load(open(path_next,'r',encoding='utf-8'))
    D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
    D_next = {k:json.loads(D_next[k]) for k in D_next}
    output = modelpredict(D_simi,D_next,inputStr)