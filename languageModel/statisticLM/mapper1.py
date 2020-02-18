import sys
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if int(fields[1])>2:
        sys.stdout.write("%s\n" % data)