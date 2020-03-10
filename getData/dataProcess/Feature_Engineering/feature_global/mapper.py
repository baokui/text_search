import sys
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)!=2:
        continue
    sys.stdout.write("%s\n" % data)
    continue