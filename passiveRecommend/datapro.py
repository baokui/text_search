import xlrd
import jieba
import numpy as np
import json
def getdata(path_data = 'D:\\项目\\输入法\\神配文数据\\召回标注\\大白狗语料1-10w召回标注327.xlsx'):
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
    C = {}
    N = 0
    for i in range(1,len(res)):
        r = res[i]
        if len(r)!=3:
            print(r)
            continue
        try:
            float(r[0])
            t = set(r[1])
            for s in t:
                if s in C:
                    C[s] += r[0]
                else:
                    C[s] = r[0]
            N = N+r[0]
        except:
            print(r)
    idf = {}
    idf = {d:np.log(N/C[d]) for d in C}
    with open('passiveRecommend/idf_char.json','w') as f:
        json.dump(idf,f)