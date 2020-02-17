def dataPro(path=""):
path = "D:\项目\输入法\神配文数据\鸡汤-0206.csv"
with open(path,'r',encoding='utf-8') as f:
    s = f.read().strip().split('\n')
S = [ss.split(',') for ss in s]
x = [len(ss) for ss in S]
for s in S:
    if len(s)!=4:
        print(len(s),s)
sc = [ss[1] for ss in S]
sc = list(set(sc))