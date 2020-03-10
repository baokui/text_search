import os
import xlrd
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
def getdata(filepath):
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