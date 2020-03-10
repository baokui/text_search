#output:[session_id,is_ac1,is_ac6,is_ac78,CI,iC,userid,flags,query,sc,post,request_class]
import sys
last_session_id = '*****'
nb = 0
#[sess_id,'1',ac,userid,ci,innerClick,flags]
#[sessid]+['0']+[query]+[sc]+[post]+[request_class]
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields)<2:
        continue
    session_id = fields[0]
    if not session_id:
        continue
    if session_id != last_session_id:
        if last_session_id != '*****':
            S = '\t'.join([last_session_id,str(nb)])
            sys.stdout.write("%s\n" % S)
        nb = 0
    last_session_id = session_id
    nb += int(fields[1])
S = '\t'.join([last_session_id,str(nb)])
sys.stdout.write("%s\n" % S)