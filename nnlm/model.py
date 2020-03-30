import json
import os
def removepunc(s,punc=u' \u3000 ,\uff0c.\u3002\u3001!\uff01?\uff1f;\uff1b~\uff5e\xb7\xb7.\u2026-#_\u2014+=\'"\u2018\u2019\u201c\u201d*&^%$/\\@'):
    for p in punc:
        s = s.replace(p,'')
    return s
def getModel(path_data):
    L = ['怎么样啊','吐血了','想你了']
    D = {}
    n = 0
    for i in range(5):
        f = open(os.path.join(path_data,'part-0000'+str(i)),'r')
        for line in f:
            n+=1
            line = line.strip()
            s = line.split('\t')
            t = []
            for i in range(1,len(s)):
                k,v = s[i].split('#')
                if len(k.decode('utf-8'))>2 and int(v)>10:
                    t.append(k+'#'+v)
            if len(t)>0:
                D[s[0]] = t
                if s[0] in L:
                    print(s[0]+'\t'+'\t'.join(t))
                if len(D)%10000==0:
                    print(len(D),n)
    S = [k+'\t'+'\t'.join(D[k]) for k in D]
    with open('result.txt','w') as f:
        f.write('\n'.join(S))

    R = []
    for d in D:
        s = D[d][0].split('#')
        if int(s[1])<100:
            continue
        R.append([d]+D[d])
    R = ['\t'.join(r) for r in R]
    with open('result1.txt','w') as f:
        f.write('\n'.join(R))

T = []
for r in R:
    s = r.split('\t')
    k = s[0]
    t = []
    for j in range(1,len(s)):
        if s[j].split('#')[0]!=k and s[j].split('#')[0]!='哈哈哈':
            t.append(s[j])
    if len(t)>0:
        T.append(k+'\t'+'\t'.join(t))

with open('model.json','w') as f:
    json.dump(D,f,ensure_ascii=False)
def modelPredict(inputStr,path_model='data/model.json'):
    s = removepunc(inputStr.strip().decode('utf-8')).encode('utf-8')
    with open(path_model,'r') as f:
        D = json.load(f)
    if s in D:
        print(D[s])