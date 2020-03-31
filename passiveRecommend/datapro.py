import xlrd
import jieba
import numpy as np
import json
import random
def getdata_labeled():
    path_data = 'D:\\项目\\输入法\\神配文数据\\召回标注\\大白狗语料1-10w召回标注327.xlsx'
    workbook = xlrd.open_workbook(path_data)  # 打开excel文件
    table = workbook.sheet_by_name('Sheet1')  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列
    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    res = res[1:]
    S = []
    for i in range(len(res)):
        if isinstance(res[i][1], str):
            y = res[i][2]
            if int(y)!=1:
                y = '0'
            else:
                y = '1'
            S.append(res[i][1].replace('\t','')+'\t'+y)
    return S
def getdata_labeled_original():
    path_data = 'D:\\项目\\输入法\\神配文数据\\召回标注\\往期被动评测数据\\beidong(3-31).label'
    with open(path_data,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    return s
def getdata_labeled_last2():
    path_data = 'D:\\项目\\输入法\\神配文数据\\召回标注\\往期被动评测数据\\前两次被动评测汇总结果.xlsx'
    workbook = xlrd.open_workbook(path_data)  # 打开excel文件
    table = workbook.sheet_by_name('Sheet1')  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列
    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    res = res[1:]
    S = []
    for i in range(len(res)):
        y = res[i][1]
        if int(y)!=1:
            y = '0'
        else:
            y = '1'
        S.append(res[i][0].replace('\t','')+'\t'+y)
    return S
def getdata(path_data = 'D:\\项目\\输入法\\神配文数据\\召回标注\\大白狗语料1-10w召回标注327.xlsx'):
    res = []
    res.extend(getdata_labeled())
    res.extend(getdata_labeled_original())
    res.extend(getdata_labeled_last2())
    res = list(set(res))
    C = {}
    N = len(res)
    for i in range(len(res)):
        r = res[i].split('\t')
        if len(r)!=2:
            print(r)
            continue
        try:
            t = set(r[0])
            for s in t:
                if s in C:
                    C[s] += 1
                else:
                    C[s] = 1
        except:
            print(r)
    idf = {d:np.log(N/C[d]) for d in C}
    W = [(d,idf[d]) for d in idf]
    W = sorted(W,key=lambda x:-x[-1])
    W.append(['<UNK>',W[0][1]])
    idf['<UNK>']=W[0][1]
    W = [w[0] for w in W]
    with open('passiveRecommend/data/idf_char.json','w',encoding='utf-8') as f:
        json.dump(idf,f)
    with open('passiveRecommend/data/vocab.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(W))
    random.shuffle(res)
    dataTrn = res[:int(len(res)*0.8)]
    dataTst = res[int(len(res)*0.8):]
    with open('passiveRecommend/data/train.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(dataTrn))
    with open('passiveRecommend/data/test.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(dataTst))