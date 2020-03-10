import sys
last_session_id = '*****'
user_history = []
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 3:
        continue
    session_id = fields[0].strip()
    if session_id != last_session_id:
        if last_session_id != '*****':
            T = sorted(user_history,key=lambda x:x[1])
            user_history = [t[0] for t in T]
            user_history = '[->]'.join(user_history)
            S = [last_session_id, user_history]
            S = '\t'.join(S)
            sys.stdout.write("%s\n" % S)
        user_history = [[fields[1],int(fields[2])]]
        last_session_id = session_id
        continue
    user_history.append([fields[1],int(fields[2])])
T = sorted(user_history,key=lambda x:x[1])
user_history = [t[0] for t in T]
user_history = '[->]'.join(user_history)
S = [last_session_id, user_history]
S = '\t'.join(S)
sys.stdout.write("%s\n" % S)