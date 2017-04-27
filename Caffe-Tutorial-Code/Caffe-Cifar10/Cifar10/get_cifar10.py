'''
Created on 13 Apr 2017

@author: mozat
'''

import os
print "start downloading"
os.system("wget --no-check-certificate http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz")
print "unzip started"
os.system("tar -xf cifar-10-python.tar.gz && rm -f cifar-10-python.tar.gz")
print "unzip finished"
os.system("mv cifar-10-batches-py/* ./data && rm -rf cifar-10-batches-py")
print "clean file finish"