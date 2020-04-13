# coding=utf-8
import json
def getW2V(path_w2v):
    print('reading w2v file...')
    f = open(path_w2v,'r')
    D = {}
    for line in f:
        s = line.strip().split(' ')
        D[s[0]] = [float(t) for t in s[1:]]
    f.close()
    print('complete w2v reading')
    return D
class config_predict(object):
    # 定义构造方法
    def __init__(self,model_config=None):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        self.rootpath='/search/odin/guobk/streaming/vpa/text_search/passiveRecommend/'
        self.path_ckpt = self.rootpath+'lr-w2v-word-ckpt-used'
        self.mode = 'lr-w2v-word-ckpt'
        self.path_idf = self.rootpath+'data/idf_char.json'
        self.path_vocab = self.rootpath+'data/vocab.txt'
        self.path_idf_word = self.rootpath+'data/idf_word.json'
        self.path_vocab_word = self.rootpath+'data/vocab_word.txt'
        self.path_w2v = '/search/odin/guobk/streaming/vpa/word2vec128/model-mean'
        self.thr = 0.8
        self.feature_dim = 8085
class Config_train(object):
    def __init__(self):
        self.batch_size = 128
        self.feature_dim = None
        self.hiddenSize = 256
        self.skip_rate = 0.0
        self.train_batch_size = 1024
        self.test_batch_size = 10000
        self.init_learning_rate = 0.1
        self.end_learning_rate = 0.01
        self.learning_rate = 0.5
        self.keep_prob = 1.0
        self.nb_examples = 100000
        self.epochs = 3000
        self.step_saveckpt = 100
        self.step_printlog = 50
        self.testlines = 1000000
def getConfig_feature(ConfigPredict):
    mode = ConfigPredict.mode
    config_feature = {}
    config_feature['use_sentLen'] = True
    config_feature['use_puncExist'] = True
    if 'lr' in mode:
        config_feature['use_charIdf'] = True
        config_feature['use_char'] = True
        with open(ConfigPredict.path_idf, 'r') as f:
            idf = json.load(f)
        with open(ConfigPredict.path_vocab, 'r') as f:
            vocab = f.read().strip().split('\n')
        config_feature['idf'] = idf
        config_feature['charList'] = vocab
    if 'w2v' in mode:
        config_feature['use_w2v'] = True
        config_feature['w2v'] = getW2V(ConfigPredict.path_w2v)
        config_feature['dim_v'] = 128
    if 'word' in mode:
        config_feature['use_wordIdf'] = True
        config_feature['use_word'] = True
        with open(ConfigPredict.path_idf_word, 'r') as f:
            idf = json.load(f)
        with open(ConfigPredict.path_vocab_word, 'r') as f:
            vocab = f.read().strip().split('\n')
        config_feature['idf_word'] = idf
        config_feature['wordList'] = vocab
    return config_feature