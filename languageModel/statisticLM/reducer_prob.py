#output:[session_id,is_ac1,is_ac6,is_ac78,CI,iC,userid,flags,query,sc,post,request_class]
import sys
last_key = 'null'
nb = 0
S = []
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)!=2:
        continue
    t = fields[0].split(',')
    if len(t)!=3:
        continue
    key = ','.join(t[:2])
    if last_key!= key:
        if last_key != 'null':
            for s in S:
                t = s[1]/(nb+0.0)
                t = '\t'.join([s[0],str(s[1]),str(t)])
                sys.stdout.write("%s\n" % t)
        nb = 0
        S = []
    last_key = key
    nb += int(fields[1])
    S.append([fields[0],int(fields[1])])
for s in S:
    t = s[1]/(nb+0.0)
    t = '\t'.join([t[0],str(t[1]),str(t[2])])
    sys.stdout.write("%s\n" % t)
