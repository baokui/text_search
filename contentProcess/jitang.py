import xlrd
import random
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
def getCorpus():
    path = "D:\项目\输入法\神配文数据\鸡汤-0206.csv"
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    S = [ss.split(',')[0].lower() for ss in s]

    path_content="D:\\项目\\输入法\\神配文数据\\祝福语MVP文件.xlsx"
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
    for i in range(1, len(res)):
        str0 = res[i][0].lower()
        corpus0.append(str0)

    S = S+corpus0
    random.shuffle(S)
    Tst = S[-10000:]
    Trn = S[:-10000]
    with open('data/train.txt','w',encoding='utf-8') as f:
        f.write('\n\n'.join(Trn))
    with open('data/valid.txt','w',encoding='utf-8') as f:
        f.write('\n\n'.join(Tst))
def get_godText():
    path_content = "D:\\项目\\输入法\\神配文数据\\ns_flx_wisdom_words.xlsx"
    # 读取excel表格
    workbook = xlrd.open_workbook(path_content)  # 打开excel文件
    table = workbook.sheet_by_name('ns_flx_wisdom_words')  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列

    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    corpus0 = []
    for i in range(0, len(res)):
        str0 = res[i][1].lower()
        corpus0.append(str0)