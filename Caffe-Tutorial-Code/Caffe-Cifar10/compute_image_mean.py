'''
Created on 2 May 2017

@author: mozat
'''
import sys
sys.path.append('/home/mozat/git/caffe/python')

import caffe
from caffe.proto import caffe_pb2
import cv2
import numpy as np
import lmdb
import os

import gflags
Flags = gflags.FLAGS
DBTYPE = 'lmdb'
train_dir = 'cifar10_train_%s'%DBTYPE

def read_lmdb(train_dir):
    in_db = lmdb.open(train_dir, readonly = True)
    idx = 1
    with in_db.begin() as in_txt:
        cursor = in_txt.cursor() #a cursor to index
        datum = caffe_pb2.Datum()
        for key, value in cursor:
            datum.ParseFromString(value)
            data= caffe.io.datum_to_array(datum)
            data = np.rollaxis(data, 0, 3)
            new_data = cv2.resize(data, (0,0), fx=4,fy=4)
            if idx%500==0:
                cv2.imwrite('./img/{label}_{:0>5d}.png'.format(idx, label=datum.label), new_data)
            idx=idx+1
    in_db.close()
    pass

def convert_mean(train_dir):
    in_db = lmdb.open(train_dir, readonly=True)
    with in_db.begin() as in_txt:
        cursor = in_txt.cursor()
        datum = caffe_pb2.Datum()
        for key, value in cursor:
            datum.ParseFromString(value)
            data = caffe.io.datum_to_array(datum)
            channels, width, height = datum.channels, datum.width, datum.height
            mean_im = np.zeros((1, channels, height, width), dtype=np.float32)
            break
    in_db.close()
    in_db = lmdb.open(train_dir, readonly=True)
    N = 0
    with in_db.begin() as in_txt:
        cursor = in_txt.cursor()
        datum = caffe_pb2.Datum()
        for key, value in cursor:
            datum.ParseFromString(value)
            data = caffe.io.datum_to_array(datum)
            channels, width, height = datum.channels, datum.width, datum.height
            mean_im[0,:] = mean_im[0,:] + data
            N = N + 1
    in_db.close()
    mean_im = mean_im / N
    print mean_im[0]
    meanImg = np.transpose(mean_im.astype(np.uint8), (2, 3, 1, 0))
    print meanImg.shape
    cv2.imwrite("mean.png", meanImg[:,:,:,0])
    #write blobproto to file
    blob = caffe.io.array_to_blobproto(mean_im)
    with open("mean.binaryproto", "wb") as f:
        f.write(blob.SerializeToString())
    np.save("mean.npy", mean_im)

if __name__ == '__main__':
    ch = os.getcwd()
    convert_mean(os.path.join(ch, train_dir))
