import sys
import time
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 11:
        continue
    [_, Time, userid, rc, AC, query, CI, iC, Post, _, dialogue] = fields
    if userid[-1]!='f':
        continue
    if rc == 'imagemix':
        try:
            t1 = time.strptime(Time[:20], '%d/%b/%Y:%H:%M:%S')
            Time = time.strftime('%Y-%m-%d %H:%M:%S',t1)
            # idx = Post.find('[seq]')
            # sc = Post[:idx]
            sc = Post.split('[seq]')[0]
            S = [userid,Time,AC,query,sc]
            S = '\t'.join(S)
            sys.stdout.write("%s\n" % S)
        except:
            continue