import jieba
def condition_prob():
    f_w = open('ngram_all3/part-00000-prob','w')
    f_r = open('ngram_all3/part-00000','r')
    for line in f_r:
        t = line.split('\t')
        if len(t)!=2:
            continue

    f_r.close()
    f_w.close()