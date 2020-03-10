import sys
last_session_id = '*****'
user_history = []
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 5:
        continue
    session_id = fields[0].strip()
    if session_id != last_session_id:
        if last_session_id != '*****':
            x = user_history
            T = []
            for xx in x:
                idx = xx.find('[&]')
                T.append([xx[:idx], xx])
            T = sorted(T, key=lambda x: x[0])
            user_history = '[->]'.join([tt[1] for tt in T])
            S = [last_session_id, user_history]
            S = '\t'.join(S)
            sys.stdout.write("%s\n" % S)
        user_history = []
    last_session_id = session_id
    user_history.append('[&]'.join(fields[1:]))
if session_id==last_session_id:
    x = user_history
    T = []
    for xx in x:
        idx = xx.find('[&]')
        T.append([xx[:idx], xx])
    T = sorted(T, key=lambda x: x[0])
    user_history = '[->]'.join([tt[1] for tt in T])
    S = [last_session_id, user_history]
    S = '\t'.join(S)
    sys.stdout.write("%s\n" % S)