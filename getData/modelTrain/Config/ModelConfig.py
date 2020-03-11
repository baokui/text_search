#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
class modelconfig(object):
    def __init__(self):
        self.redis_list= [["b.redis.sogou", 2971, "sogouvpaintention"],["b.redis.sogou", 2972, "sogouvpaintention"], ["b.redis.sogou", 2973, "sogouvpaintention"], ["b.redis.sogou", 2974, "sogouvpaintention"], ["b.redis.sogou", 2981, "sogouvpaintention"], ["b.redis.sogou", 2982 ,"sogouvpaintention"] , ["b.redis.sogou", 2983, "sogouvpaintention"], ["b.redis.sogou", 2984, "sogouvpaintention"]]
        self.model_version = '2019111401'
        self.nb_redisCards = 8
        self.sc = []
        self.sym_personalization = 'pers_'
        self.sym_prefix_userfeature = 'imageFeature_'
        self.threshold = 0.62
        self.threshold_ios = 0.62
        self.path_keywords = 'keywords.txt'
        self.path_modelConfig = ""
        self.path_lrmodel = ""
        self.path_userdata = ''
        self.TimeSeg = [i for i in range(25)]
        self.T = [str(i) for i in range(24)]
        self.punc = ['?', '!', '.', ',', '？', '！', '。', '，']
        self.map_user2redis = {'0':0,'1':0,'2':1,'3':1,'4':2,'5':2,'6':3,'7':3,'8':4,'9':4,'a':5,'b':5,
                      'c':6,'d':6,'e':7,'f':7}
    def get_nb_features(self):
        #[hour, last_click]+[sc+out_of_sc]+[timeseg]+[stringlen,punExist]
        nb_features_session = 2+len(self.get_sc())+len(self.T)+2
        nb_features_user = 1+len(self.get_sc())+len(self.T)
        nb_features_global = 2
        nb_features = nb_features_global+nb_features_user+nb_features_session
        return nb_features, nb_features_session, nb_features_user, nb_features_global
    def get_threshold_predict(self):
        threshold_predict = -np.log(1/self.threshold-1)
        return threshold_predict,-np.log(1/self.threshold_ios-1)
    def get_sc(self):
        with open(self.path_keywords,'r') as f:
            keywords = f.read().strip().split('\n')
        keywords.append('otherwords')
        return keywords
