'''
Created on 10 Feb 2017

@author: mozat
'''
from random import randint
from time import sleep, ctime
from Queue import Queue
import threading

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    def getResult(self):
        return self.res
    def run(self):
        print 'starting ', self.name, ' at:', ctime()
        self.res  = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()

def writeQ(queue):
    queue.put('zhangli',1)
    print 'procuced object to Q..., size now', queue.qsize()
    
def readQ(queue):
    val = queue.get(1)
    print 'consumed object from Q..., size now', queue.qsize()
    
def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))
def reader(queue, loops):
    for i in range(loops*2):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer, reader]
nfuncs = range(len(funcs))

q = Queue(32)
nloops = randint(2,5)

threads = []
for i in nfuncs:
    t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
    threads.append(t)
for i in nfuncs:
    threads[i].start()    
for i in nfuncs:
    threads[i].join()

print "all done"