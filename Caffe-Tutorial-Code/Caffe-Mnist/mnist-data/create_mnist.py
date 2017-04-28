'''
Created on 24 Apr 2017

@author: mozat
'''
import os, sys
import numpy as np
import lmdb
import struct
import caffe
from caffe.proto import caffe_pb2
import logging
import gflags
from matplotlib import pyplot

DBTYPE = 'lmdb'
Flags = gflags.FLAGS
gflags.DEFINE_string('train_dir', './train_{backend}'.format(backend=DBTYPE), 'THIS IS TO SET TRAIN DIR')
gflags.DEFINE_string('test_dir', './test_{backend}'.format(backend=DBTYPE), 'THIS IS TO SET VALIDATE DIR')
gflags.DEFINE_string('log_name', 'test.log', 'THIS IS TO SET LOG FILE')

def read(dataset = "training", path = "."):
    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError, "dataset must be 'testing' or 'training'"
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)
    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16)) #28 by 28
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)
    
    get_img = lambda idx: (lbl[idx], img[idx])
    data = []
    for i in xrange(len(lbl)):
        data.append(get_img(i))
    return data
        
def show(image):
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap = 'gray')
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    pyplot.show()

def write_lmdb():
    if os.path.exists(Flags.train_dir):
        os.system("rm -rf {dir}".format(dir = Flags.train_dir))
    in_db = lmdb.open(Flags.train_dir, map_size = int(1e12))
    train_data = read(dataset = 'training')
    with in_db.begin(write=True) as in_txt:
        in_idx = 0
        for in_idx, img in enumerate(train_data):
            label, image = img[0], img[1]
            datum = caffe_pb2.Datum(channels = 1, width = image.shape[1], height = image.shape[0], 
                                    label = int(label),
                                    data = image.tobytes())
            in_txt.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
            logging.info('writing {in_idx} image'.format(in_idx = in_idx))
    in_db.close()
    print 'finishing processing mnist training dataset'
    
    if os.path.exists(Flags.test_dir):
        os.system("rm -rf {dir}".format(dir = Flags.test_dir))
    in_db = lmdb.open(Flags.test_dir, map_size = int(1e12))
    test_data = read(dataset = 'testing')
    with in_db.begin(write=True) as in_txt:
        for in_idx, img in enumerate(test_data):
            label, image = img[0], img[1]
            datum = caffe_pb2.Datum(channels = 1, width = image.shape[1], height = image.shape[0],
                                    label = int(label),
                                    data = image.tobytes())
            in_txt.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
            logging.info('writeing {in_idx} image'.format(in_idx = in_idx))
    in_db.close()
    print 'finishing processing mnist validation dataset'
    

def read_lmdb():
    in_db = lmdb.open(Flags.validate_dir, readonly = True)
    with in_db.begin() as in_txt:
        cursor = in_txt.cursor() #a cursor to index
        datum = caffe_pb2.Datum()
        for key, value in cursor:
            datum.ParseFromString(value)
            data= caffe.io.datum_to_array(datum)
            print data.shape
            label = datum.label
            image = np.fromstring(datum.data, dtype=np.uint8)
#             x = image.reshape(datum.height, datum.width)
#             print x.shape
#             pyplot.imshow(x, cmap = 'gray')
#             pyplot.show()
            print key, label, datum.channels, datum.height, datum.width
    pass

def main(argv):
    Flags(argv)
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename=Flags.log_name,  
                    filemode='w')
    write_lmdb()
#     read_lmdb()
    
if __name__ == '__main__':
    sys.argv.append('--log_name=minst.create.log')
    main(sys.argv)


