#output:[session_id,is_ac1,is_ac6,is_ac78,CI,iC,userid,flags,query,sc,post,request_class]
import sys
last_key = 'null'
nb = 0
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)!=2:
        continue
    key = fields[0]
    if last_key!= key:
        if last_key != 'null':
            S = [last_key,str(nb)]
            S = '\t'.join(S)
            sys.stdout.write("%s\n" % S)
        nb = 0
    last_key = key
    nb += int(fields[1])
S = [key,str(nb)]
S = '\t'.join(S)
sys.stdout.write("%s\n" % S)
