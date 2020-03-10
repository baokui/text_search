import json
d = json.load(open('image.json','r',encoding='utf-8'))
keys=[k for k in d]
data = d[keys[0]]
triggerW= [data[i]['triggerWord'] for i in range(len(data))]
searchW = [data[i]['searchWord'] for i in range(len(data))]
t = list(set(triggerW))
s = list(set(searchW))
with open('table-trigger.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(t))
with open('table-search.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(s))