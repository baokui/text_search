#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("jieba")
import jieba
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 11:
        continue
    Input = fields[5]
    sent = jieba.cut(Input)
    words = [ele.encode("utf-8") for ele in sent]
    for word in words:
        sys.stdout.write('\t'.join([word,'1']) + '\n')


