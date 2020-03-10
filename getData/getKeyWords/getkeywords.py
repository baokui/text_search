import os
import sys
def main(path_keywords,max_nb=10000):
    files = os.listdir(path_keywords)
    D = {}
    for file in files:
        if 'part' not in file:
            continue
        f = open(os.path.join(path_keywords,file))
        for line in f:
            line = line.strip().split('\t')
            if len(line)!=2:
                continue
            if line[0] not in D:
                D[line[0]] = int(line[1])
            else:
                D[line[0]] += int(line[1])
        f.close()
    R = [(k,D[k]) for k in D]
    R = sorted(R,key=lambda x:-x[1])
    S = [R[i][0] for i in range(min(len(R),max_nb))]
    with open('keywords.txt','w') as f:
        f.write('\n'.join(S))
if __name__=='__main__':
    path_data = sys.argv[1]
    main(path_data)

