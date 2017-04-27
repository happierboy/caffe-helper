'''
Created on 13 Apr 2017

@author: mozat
'''
import os
print "downloading"
os.system("wget -c http://dl.caffe.berkeleyvision.org/caffe_ilsvrc12.tar.gz")
print "unzipping"
os.system("tar -xf caffe_ilsvrc12.tar.gz && rm -f caffe_ilsvrc12.tar.gz")
print "done"