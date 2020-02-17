import sys
n = 3
for data in sys.stdin:
    s = data.split(' ')
    if len(s)<n:
        continue
    for i in range(len(s)-n+1):
        key = '('+','.join([s[j] for j in range(i,i+n)])+')'
        t = key+'\t'+'1'
        sys.stdout.write("%s\n" % t)