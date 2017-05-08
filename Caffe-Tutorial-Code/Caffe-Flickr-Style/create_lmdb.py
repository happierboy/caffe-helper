'''
Created on 8 May 2017

@author: mozat
'''
import sys
import caffe
import lmdb
from caffe.proto import caffe_pb2

def make_datum(img, label):
    caffe_pb2.Datum()