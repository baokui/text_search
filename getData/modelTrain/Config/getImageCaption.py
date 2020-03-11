import json
d = json.load(open('LRmodel-imagemix/Config/table-imagemix-caption.txt','r',encoding='utf-8'))
data = d['data']
s = [dd['word'] for dd in data]
with open('LRmodel-imagemix/Config/table-search-caption.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(s))


import json
d = json.load(open('LRmodel-imagemix/Config/table-imagemix0.txt','r',encoding='utf-8'))
data = d['data']
S = [d['triggerWord']+'\t'+d['searchWord'] for d in data]
with open('LRmodel-imagemix/Config/table-trigger.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(S))