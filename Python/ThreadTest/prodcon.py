'''
Created on 10 Feb 2017

@author: mozat
'''
from random import randint
from time import sleep
from Queue import Queue



def writeQ(queue):
    queue.put('zhangli',1)
    print 'size now', queue.qsize()
    
def readQ(queue):
    val = queue.get(1)
    print 'consumed object from Q..., size now', queue.qsize()
    
def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))
def reader(queue, loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer, reader]
nfuncs = range(len(funcs))

threads = []
for i in nfuncs:
    t = MyThread(funcs[i], (q, nloops), funcs[i].__name__())
    threads.append(t)

for i in nfuncs:
    threads[i].start()
    
for i in nfuncs:
    threads[i].join()

print "all done"

