'''
Created on 10 Feb 2017

@author: mozat
'''

import threading
import time
import random

class  ThreadFunc(threading.Thread):
    def __init__(self, num):
        self.num = num
        super(ThreadFunc, self).__init__()
    
    def run(self):
        time.sleep(self.num)
        print 'time sleeped: ', self.num


if __name__ == '__main__':
    thread_num = 5
    thread_pool = []
    for idx in range(thread_num):
        p = ThreadFunc(random.randint(10,30))
        thread_pool.append(p)
        p.start()
    print 'active',  threading.activeCount()
    p1 = threading.currentThread()
    print 'this thread', p1.num
    for p in thread_pool:
        p.join()
    print 'threading finished'
    
                       
    