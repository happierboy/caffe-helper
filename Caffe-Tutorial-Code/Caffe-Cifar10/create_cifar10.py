'''
Created on 13 Apr 2017

@author: mozat
'''
import os, sys
import numpy as np
import lmdb
import caffe
from caffe.proto import caffe_pb2
import cv2
import gflags
import logging

DBTYPE = 'lmdb'
Flags = gflags.FLAGS
gflags.DEFINE_string("input_dir", './Cifar10/data/', "input data dir")
gflags.DEFINE_string("output_dir", './Cifar10/data/', "output data dir")
gflags.DEFINE_string("log_name", 'test.log', "log filename")

def unpickle(filename):
    import cPickle
    with open(filename, 'rb') as fo:
        data = cPickle.load(fo)
    return data

def read_python_data(filename):
    kCIFARSize = 32
    data = unpickle(filename)
    for idx in range(0, len(data['filenames'])):
        filename = data['filenames'][idx]
        R = data['data'][idx][0:kCIFARSize*kCIFARSize]
        G = data['data'][idx][kCIFARSize*kCIFARSize:kCIFARSize*kCIFARSize*2]
        B = data['data'][idx][kCIFARSize*kCIFARSize*2:]
        img = np.dstack(map(lambda x: np.reshape(x, (kCIFARSize, kCIFARSize)), [B, G, R]))
        cv2.imwrite('./data/%03d_'%(data['labels'][idx])+filename, np.asarray(img, dtype = np.uint8))
        datum = make_datum(img, data['labels'][idx])
    pass

def make_datum(img, label):
    datum= caffe_pb2.Datum()
    datum.channels = img.shape[2]
    datum.height = img.shape[0]
    datum.width = img.shape[1]
    datum.label = label
    #RGB TO BGR
    datum.data = np.rollaxis(img, 2).tostring()
    return datum

def main(argv):
    Flags(argv)
    logging.basicConfig(level=logging.DEBUG,  
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                datefmt='%a, %d %b %Y %H:%M:%S',  
                filename=Flags.log_name,  
                filemode='w')  
        
    #remove all directory
    train_dir = 'cifar10_train_%s'%DBTYPE
    test_dir = 'cifar10_test_%s'%DBTYPE
    for data_dir in [train_dir, test_dir]:
        os.system('rm -rf ' + data_dir)

    #add all
    kCIFARTrainBatches = 5
    kCIFARSize = 32
    kCIFARBatchSize = 10000
    in_db = lmdb.open(train_dir, map_size = int(1e12))
    with in_db.begin(write=True) as in_txt:
        for field in range(0,kCIFARTrainBatches):
            batch_filename = Flags.input_dir+"/data_batch_"+ '%s'%(field+1)
    #         read_python_data(batch_filename)
            data = unpickle(batch_filename)
            for idx, filename in enumerate(data['filenames']):
                R = data['data'][idx][0:kCIFARSize*kCIFARSize]
                G = data['data'][idx][kCIFARSize*kCIFARSize:kCIFARSize*kCIFARSize*2]
                B = data['data'][idx][kCIFARSize*kCIFARSize*2:]
                img = np.dstack(map(lambda x: np.reshape(x, (kCIFARSize, kCIFARSize)), [B, G, R]))
        #         cv2.imwrite('./data/%03d_'%(data['labels'][idx])+filename, np.asarray(img, dtype = np.uint8))
                datum = make_datum(img, data['labels'][idx])
                new_key = '{:0>5d}'.format(field*kCIFARBatchSize+idx)
                in_txt.put(new_key, datum.SerializeToString())
    in_db.close()
    
    
    in_db = lmdb.open(test_dir, map_size = int(1e12))
    batch_filename = Flags.input_dir+"/test_batch"
#         read_python_data(batch_filename)
    data = unpickle(batch_filename)
    with in_db.begin(write=True) as in_txt:
        for idx, _ in enumerate(data['filenames']):
            R = data['data'][idx][0:kCIFARSize*kCIFARSize]
            G = data['data'][idx][kCIFARSize*kCIFARSize:kCIFARSize*kCIFARSize*2]
            B = data['data'][idx][kCIFARSize*kCIFARSize*2:]
            img = np.dstack(map(lambda x: np.reshape(x, (kCIFARSize, kCIFARSize)), [B, G, R]))
            datum = make_datum(img, data['labels'][idx])
            new_key = '{:0>5d}'.format(idx)
            in_txt.put(new_key, datum.SerializeToString())
    in_db.close()
    
if __name__ == '__main__':
    main(sys.argv)
    