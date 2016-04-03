#__author__ = 'Administrator'
# -*- coding: utf-8 -*-

import threading
import time
import local_2_chinese

def threadFunc(index):
    global mutex

    # 打印线程名

    print threading.currentThread().getName()

    local_2_chinese.get_list(index)

    # for x in xrange(0, int(num)):
    #     # 取得锁
    #     mutex.acquire()
    #     total = total + 1
    #     # 释放锁
    #     mutex.release()

def addThread(num):
    #定义全局变量
    global mutex
    # 创建锁
    mutex = threading.Lock()

    #定义线程池
    threads = []
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=threadFunc, args=(x,)))
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()

    # 打印执行结果



if __name__ == '__main__':
    # 创建n个线程
    start = time.time()
    addThread(3)
    end = time.time()
    print u'测试数量: ',local_2_chinese.NUMTEST
    print u'翻译结果数量: ',local_2_chinese.COUNT
    print 'time:',end-start

    # for key,value in local_2_chinese.ufi_name.items():
    #     print key
    #     for k,v in value.items():
    #         print k,v
    #     print'________'
