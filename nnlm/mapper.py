#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
def removepunc(s,punc=u' \u3000 ,\uff0c.\u3002\u3001!\uff01?\uff1f;\uff1b~\uff5e\xb7\xb7.\u2026-#_\u2014+=\'"\u2018\u2019\u201c\u201d*&^%$/\\@'):
    for p in punc:
        s = s.replace(p,'')
    return s
for line in sys.stdin:
    fields = line.strip().split('，')
    if len(fields)<2:
        continue
    R = [fields[i].strip().decode('utf-8') for i in range(len(fields))]
    R = [removepunc(r) for r in R]
    for i in range(len(fields)-1):
        if len(R[i])<2 or len(R[i])>8:
            continue
        S = R[i].encode('utf-8')+'\t'+R[i+1].encode('utf-8')
        sys.stdout.write("%s\n" % S)