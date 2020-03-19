#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
lastKey='NULL0000'
lastValues = {}
nb_min_key = 2
for line in sys.stdin:
    fields = line.strip().split('\t')
    if len(fields)!=2:
        continue
    Key = fields[0]
    if Key!=lastKey:
        if lastKey!='NULL0000':
            if len(lastValues)>=nb_min_key:
                value = [[k,lastValues[k]] for k in lastValues]
                value = sorted(value,key=lambda x:-x[-1])
                value_s = '\t'.join([k[0]+'#'+str(k[1]) for k in value])
                S = lastKey+'\t'+value_s
                sys.stdout.write("%s\n" % S)
        lastValues = {}
    lastKey=Key
    if fields[1] not in lastValues:
        lastValues[fields[1]] = 1
    else:
        lastValues[fields[1]] += 1
if len(lastValues) >= nb_min_key:
    value = [[k, lastValues[k]] for k in lastValues]
    value = sorted(value, key=lambda x: -x[-1])
    value_s = '\t'.join([k[0] + '#' + str(k[1]) for k in value])
    S = lastKey + '\t' + value_s
    sys.stdout.write("%s\n" % S)