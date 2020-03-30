# -*- coding:utf-8 -*-
import unicodedata
stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
punc_zh = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟‧﹏.…"
punc_en = unicodedata.normalize('NFKC', punc_zh[:-1])+unicodedata.normalize('NFKC', punc_zh[-1])[-1]
punc_zh = punc_zh+'。'
punc_en = punc_en+'｡'
map_e2z = {punc_en[i]:punc_zh[i] for i in range(len(punc_en))}
stopwords = stopwords+list(punc_zh)+list(punc_en)
stopwords = list(set(stopwords))
remove_words = ['"']
def remove_stopwords(s0,stopwords0=stopwords):
    sn = s0
    for t in stopwords0:
        sn = sn.replace(t,'')
    return sn
def postprocess(S,prefix='',removeWords = True, transfer = True,sentEndcontent=False,removeSpecial=False):
    R = []
    for s0 in S:
        if removeWords:
            s0 = remove_stopwords(s0,remove_words)
        if transfer:
            s0 = prefix+Transfer(s0[len(prefix):])
        if sentEndcontent:
            s0 = sent_endcontent(s0)
        if removeSpecial:
            s0 = remove_special(s0)
        R.append(s0)
    return R
def Transfer(s0):
    s0 = strQ2B(s0)
    for t in map_e2z:
        if t in s0:
            s0 = s0.replace(t,map_e2z[t])
    return s0
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring
def remove_special(s0):
    spe = blackwords
    for s in spe:
        if s in s0:
            return ''
    return s0
def sent_endcontent(tmptext):
    punc_end = '.?!。？！'
    ii =  0
    for ii in range(len(tmptext)):
        if tmptext[len(tmptext) - ii - 1] in punc_end:
            break
    if ii != len(tmptext) - 1:
        tmptext = tmptext[:len(tmptext) - ii]
    return tmptext
def getdata():
    path1 = 'D:\\项目\\NLP-Corpus\\中文歌词\\趣味联想-新增歌词913首'
    path2 = 'D:\\项目\\NLP-Corpus\\中文歌词\\歌词.txt'
    with open(path1,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    corpus0 = s

    with open(path2,'r') as f:
        s = f.read().strip().split('\n')
    corpus1 = []
    for i in range(len(s)):
        if '-' not in s[i]:
            print(i)
            continue
        idx = s[i].index('-')
        t = s[i][:idx]
        t = t.replace('\t','，')
        corpus1.append(t)
    c = []
    for t in corpus1:
        tt = t.split('，')
        T = [ttt for ttt in tt if len(ttt)>0]
        c.append('，'.join(T))
    C = []
    s = c[0].split('，')
    for i in range(1,len(c)):
        t = c[i].split('，')
        if s[-1] in t:
            idx = t.index(s[-1])+1
            s.extend(t[idx:])
        else:
            x = '，'.join(s).replace('。','')
            if x[-1] == '，':
                x = x[:-1]
            C.append(x)
            s = c[i].split('，')
    x = '，'.join(s).replace('。','')
    if x[-1] == '，':
        x = x[:-1]
    C.append(x)

    corpus = C+corpus0
