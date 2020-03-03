import sys
import os
def parse_result(Str):
    pr = 0
    idx = Str[pr:].find('{"request_class":"') + 18
    if idx == 17:
        return []
    idx_end = Str[pr + idx:].find('","')
    request_class = Str[pr + idx:pr + idx + idx_end]
    if request_class!='godText':
        return []
    pr = pr + idx + idx_end
    idx = Str[pr:].find('vpaRequestedText":"') + 19
    if idx == 18:
        return []
    idx_end = Str[pr + idx:].find('"')
    query = Str[pr + idx:pr + idx + idx_end]
    pr = pr + idx + idx_end
    idx = Str[pr:].find('"session_id":"') + 14
    if idx == 13:
        return []
    sessid = Str[pr + idx:pr + idx + 19]
    pr = pr + idx + 19
    Post = 'null'
    if request_class=='multiReplace' or request_class=='godText':
        post = []
        summary = '"summary":"'
        while summary in Str[pr:]:
            idx = Str[pr:].find(summary) + 11
            idx_end = Str[pr + idx:].find('","template_height"')
            post.append(Str[pr + idx:pr + idx + idx_end])
            pr = pr + idx + idx_end
        post = '[seq]'.join(post)
        '''
        idx = Str[pr:].find('display_tips":"') + 15
        if idx == 14:
            return []
        idx_end = Str[pr + idx:].find(',"id"')
        if idx_end == -1:
            idx_end = Str[pr + idx:].find('","stype"')
            if idx_end == -1:
                return []
            sc_id = "-1"
        else:
            idx_b = pr+idx+idx_end+len(',"id":"')
            idx_e = idx_b+4
            sc_id = Str[idx_b:idx_e]
        sc = Str[pr + idx:pr + idx + idx_end]
        '''
        sc = 'sc_null'
        sc_id = 'scId_null'
        Post = sc+'[seq]'+sc_id+'[seq]'+post
    elif request_class=='imagemix':
        sc_id = '-1'
        idx = Str[pr:].find('display_tips":"') + 15
        if idx == 14:
            return []
        idx_end = Str[pr + idx:].find('","stype"')
        if idx_end == -1:
            return []
        sc = Str[pr + idx:pr + idx + idx_end]
        Post = sc +'[seq]'+sc_id+ '[seq]' + 'null'
    S = [sessid,'0',request_class,query,Post]
    # S = '\t'.join(S)
    return S
def parse_android(data, set_ac={'1', '6','76', '78'}):
    if 'godText' not in data:
        return []
    pr = 0
    idx0 = data[pr:].find('[')
    idx1 = data[pr:].find(']')
    if idx0==-1 or idx1==-1:
        return []
    Time = data[pr+idx0+1:pr+idx1]
    pr = pr+idx1
    idx = data[pr:].find('sessionId=')
    if idx == -1:
        return []
    sess_id = data[pr + idx + 10:pr + idx + 10 + 19]
    pr = pr + idx + 10 + 19
    #
    ci = '-1'
    idx = data[pr:].find('&ci=')
    if idx != -1:
        if data[pr + idx + 4:pr + idx + 4 + 2].isdigit():
            ci = data[pr + idx + 4:pr + idx + 4 + 2]
        else:
            ci = data[pr + idx + 4:pr + idx + 4 + 1]
    #
    flags = 'null'
    idx = data[pr:].find('flags=') + 6
    if idx != 5:
        idx_end = data[pr + idx:].find('&')
        if idx_end!=-1:
            flags = data[pr + idx:pr + idx + idx_end]
    #
    innerClick = '-1'
    idx = data[pr:].find('innerClick=')
    if idx != -1:
        if data[pr + idx + 11:pr + idx + 11 + 2].isdigit():
            innerClick = data[pr + idx + 11:pr + idx + 11 + 2]
        else:
            innerClick = data[pr + idx + 11:pr + idx + 11 + 1]
    #
    idx = data[pr:].find('userid=')
    if idx == -1:
        return []
    userid = data[pr + idx + 7:pr + idx + 7 + 16]
    pr = pr + idx + 7 + 16
    #
    idx = data[pr:].find('&ac=') + 4
    if idx == 3:
        return []
    if data[pr + idx:pr + idx + 2].isdigit():
        ac = data[pr + idx:pr + idx + 2]
    else:
        ac = data[pr + idx:pr + idx + 1]
    if ac not in set_ac:
        return []
    pr = pr + idx + 1
    return [sess_id, '1', Time, ac, userid, ci, innerClick, flags]
def parse_dialogue(data):
    #data = json.loads(data)
    data = data.replace('\\','')
    S = []
    s0 = '"timestamp":"'
    s1 = '","sentence":"'
    s2 = '","user":"'
    p = 0
    Str = data[p:]
    while len(Str)>2:
        idx0 = Str.find(s0)
        idx1 = Str.find(s1)
        idx2 = Str.find(s2)
        if idx0==-1 or idx1==-1 or idx2==-1:
            break
        timestamp = Str[idx0+len(s0):idx1]
        sentence = Str[idx1+len(s1):idx2]
        user = Str[idx2+len(s2)]
        p = p + idx2+len(s2)+1
        if p>=len(data):
            break
        Str = data[p:]
        #timestamp = Str["timestamp"]
        #sentence = Str["sentence"]
        #user = Str["user"]
        S.append(timestamp+'#'+user+'#'+sentence)
    return S
def parse_serve(Str):
    idx = Str.find('"dialogues":"') + len('"dialogues":"')
    if idx == len('"dialogues":"')-1:
        return []
    idx_end = Str[idx:].find('","')
    dialogue = Str[idx:idx + idx_end]
    Sent = parse_dialogue(dialogue)
    if len(Sent)==0:
        return []
    idx = Str.find('"UserID":"') + len('"UserID":"')
    if idx == len('"UserID":"') - 1:
        return []
    idx_end = Str[idx:].find('","')
    userid = Str[idx:idx + idx_end]
    idx = Str.find('"SessionID":') + 12
    if idx == 11:
        return []
    sessid = Str[idx:idx + 19]
    return [sessid,'2',userid,'[dialogue]'.join(Sent)]
filepath = os.environ.get('mapreduce_map_input_file')
filename = os.path.split(filepath)[0].strip()
for data in sys.stdin:
    # if filename == 'viewfs://marsX/storage/sogou/desktop/imeservice/vpare/201908/20190830':
    if 'desktop/imeservice/vpare/' in filename:
        data = data.strip()
        data = data.replace('\t', '[tab]')
        try:
            x = parse_result(data)
            if x:
                s = '\t'.join(x)
                sys.stdout.write(s + '\n')
        except:
            continue
    # if filename == 'viewfs://marsX/cloud/dt/pingback/ping/djt-pb-log/vpapb_android_shouji/201908/20190830':
    if 'vpapb_android_shouji' in filename:
        data = data.strip()
        # data = data.replace('\t','[seq]')
        try:
            x = parse_android(data,{'1', '6','76', '78'})
            if x:
                s = '\t'.join(x)
                sys.stdout.write(s + '\n')
        except:
            continue