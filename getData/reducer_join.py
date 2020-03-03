#output:[session_id,is_ac1,is_ac6,is_ac78,CI,iC,userid,flags,query,sc,post,request_class]
import sys
last_session_id = '*****'
AC = []
CI = '-1'
iC = '-1'
Time = ''
userid = ''
F = ''
rc = ''
query = ''
Post = ''
tag = []
Dialogue0 = 'null#null#null'
Dialogue = Dialogue0
# [sessid, '1', Time, ac, userid, ci, innerClick, flags]
# [sessid, '0', request_class,query,Post]
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    session_id = fields[0].strip()
    if len(fields) != 4 and len(fields) != 5 and len(fields) != 8:
        continue
    if session_id != last_session_id:
        if last_session_id != '*****':
            if '0' in tag and '1' in tag:
                S = [last_session_id,Time,userid,rc,'#'.join(AC),query,CI,iC,Post,F,Dialogue]
                S = '\t'.join(S)
                sys.stdout.write("%s\n" % S)
        AC = []
        tag = []
        Dialogue = Dialogue0
    last_session_id = session_id
    if len(fields)==8:
        [_, tt, Time, ac, userid, CI, iC, F] = fields
        AC.append(ac)
        tag.append(tt)
    if  len(fields) == 5:
        [_, tt, rc, query, Post] = fields
        tag.append(tt)
    if len(fields) == 4:
        [_,tt,_,Dialogue] = fields
        tag.append(tt)
if '0' in tag and '1' in tag:
    S = [last_session_id, Time, userid, rc, '#'.join(AC), query, CI, iC, Post, F,Dialogue]
    S = '\t'.join(S)
    sys.stdout.write("%s\n" % S)

