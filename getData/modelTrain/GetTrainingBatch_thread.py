#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import sys
import os
import GetTrainingBatch
exitFlag = 0
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, user):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.user = user
    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("\nStarting " + self.name+'\n')
        GetTrainingBatch.main(path_global,path_user,path_session,self.user, path_tmpfile,epoch,Date_sess, path_userData,joining=joining)
        print("\nExiting " + self.name+'\n')

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def main(path_session,epoch,Date_sess):
    # 创建新线程
    users = os.listdir(path_session)
    Date_sess = Date_sess.replace('/', '')
    threads = []
    for user in users:
        str1 = ['thread','epoch='+str(epoch),'Date='+Date_sess,'user='+user]
        threads.append(myThread(user, '-'.join(str1),user))
    # 开启线程
    for thr in threads:
        thr.start()
    print("Exiting Main Thread")
if __name__=='__main__':
    path_global = sys.argv[1]
    path_user = sys.argv[2]
    path_session = sys.argv[3]
    path_tmpfile = sys.argv[4]
    epoch = sys.argv[5]
    Date_sess = sys.argv[6]
    path_userData = sys.argv[7]
    joining=False
    if len(sys.argv) > 8:
        joining = bool(int(sys.argv[8]))
    main(path_session, epoch,Date_sess)
