import os
import xlrd
import string
def str_count(str):
    '''找出字符串中的中英文、空格、数字、标点符号个数'''
    count_en = count_dg = count_sp = count_zh = count_pu = 0
    for s in str:
        # 英文
        if s in string.ascii_letters:
            count_en += 1
        # 数字
        elif s.isdigit():
            count_dg += 1
        # 空格
        elif s.isspace():
            count_sp += 1
        # 中文
        elif s.isalpha():
            count_zh += 1
            print('zh-%s'%s)
        # 特殊字符
        else:
            count_pu += 1
            print('other-%s'%s)
    print('英文字符：', count_en)
    print('数字：', count_dg)
    print('空格：', count_sp)
    print('中文：', count_zh)
    print('特殊字符：', count_pu)
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
def zh_count(S):
    n = [int(is_Chinese(s)) for s in S]
    return sum(n)
def getdata(filepath):
    min_length = 8
    filepath = 'D:\\项目\\输入法\\神配文数据\\神配文原始语料'
    files = os.listdir(filepath)
    S = []
    for file in files:
        if 'xlsx' not in file:
            continue
        workbook = xlrd.open_workbook(os.path.join(filepath,file))  # 打开excel文件
        table = workbook.sheet_by_index(0)  # 将文件内容表格化
        rows_num = table.nrows  # 获取行
        cols_num = table.ncols  # 获取列
        res = []  # 定义一个数组
        for rows in range(rows_num):
            r = []
            for cols in range(cols_num):
                r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
            res.append(r)
        idx = -1
        for i in range(cols_num):
            if res[0][i].lower()=='content':
                idx = i
        if idx!=-1:
            corpus0 = []
            for i in range(1, len(res)):
                str0 = str(res[i][idx]).lower()
                if len(str0)<min_length:
                    continue
                if file=='vpa_szf_135203.xlsx':
                    if str0[1]=='.' or str0[1]=='、':
                        str0 = str0[2:]
                    if str0[2]=='.' or str0[2]=='、':
                        str0 = str0[3:]
                    corpus0.append(str0)
                else:
                    corpus0.append(str0)
            S.extend(corpus0)
            print("file-%s: %s"%(file,corpus0[0]))
        else:
            print('error with %s'%file)
def getdata2(filepath):
    min_length = 8
    filepath = 'D:\\项目\\输入法\\神配文数据\\语料2'
    files = os.listdir(filepath)
    S = []
    for file in files:
        if 'xlsx' not in file:
            continue
        workbook = xlrd.open_workbook(os.path.join(filepath,file))  # 打开excel文件
        table = workbook.sheet_by_index(0)  # 将文件内容表格化
        rows_num = table.nrows  # 获取行
        cols_num = table.ncols  # 获取列
        res = []  # 定义一个数组
        for rows in range(rows_num):
            r = []
            for cols in range(cols_num):
                r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
            res.append(r)
        idx = -1
        if idx!=0:
            corpus0 = []
            for i in range(1, len(res)):
                str0 = str(res[i][idx]).lower()
                if len(str0)<min_length:
                    continue
                if file=='vpa_szf_135203.xlsx':
                    if str0[1]=='.' or str0[1]=='、':
                        str0 = str0[2:]
                    if str0[2]=='.' or str0[2]=='、':
                        str0 = str0[3:]
                    corpus0.append(str0)
                else:
                    corpus0.append(str0)
            S.extend(corpus0)
            print("file-%s: %s"%(file,corpus0[0]))
        else:
            print('error with %s'%file)
def getdata3(filepath):
    min_length = 8
    filepath = 'D:\\项目\\输入法\\神配文数据\\归档'
    files = os.listdir(filepath)
    S = []
    n_out = 0
    for file in files:
        if 'txt' not in file:
            continue
        f = open(os.path.join(filepath,file),'r',encoding='utf-8')
        s = []
        while True:
            try:
                line = f.readline().strip().split('\t')[0]
                if not line:
                    break
                if file=='16.txt':
                    if line[1]=='、':
                        line = line[2:]
                    elif line[2]=='、':
                        line = line[3:]
                    elif line[1]=='.':
                        line = line[2:]
                    elif line[2]=='.':
                        line = line[3:]
                if len(line)>=min_length:
                    s.append(line)
            except:
                n_out += 1
        f.close()
        print(file)
        print(s[0])
        S.extend(s)
def getdata4():
    import json
    with open('D:\\项目\\输入法\\神配文数据\\guidang_all.json','r',encoding='utf-8') as f:
        S0 = json.load(f)
    with open('D:\\项目\\输入法\数据处理\\text_search\\data\\raw_multiReplace_all.json','r',encoding='utf-8') as f:
        S1 = json.load(f)
    S0 = S0+S1*3
    nb_min = 6
    S = []
    R = []
    for i in range(len(S0)):
        S0[i] = S0[i].replace('\t','')
        n = zh_count(S0[i])
        if n<nb_min or n/float(len(S0[i]))<0.5:
            R.append(S0[i])
        else:
            S.append(S0[i])
        if i%10000==0:
            print(i,len(S),len(R))
    import random
    random.shuffle(S)
    with open('D:\\项目\\输入法\\神配文数据\\godText_all1.json','w',encoding='utf-8') as f:
        json.dump(S,f,ensure_ascii=False,indent=4)