'''
Created on 8 May 2017

@author: mozat
'''
import sys, os
import csv
import caffe
import lmdb
import numpy as np
from caffe.proto import caffe_pb2
import gflags

#not feasible for very large data

DBTYPE='lmdb'
Flags = gflags.FLAGS
gflags.DEFINE_string('input_dir', './filter_data', 'input data dir')
gflags.DEFINE_string('output_dir', './lmdb', 'output dir')
def make_datum(img, label):
    datum = caffe_pb2.Datum()
    datum.channels = img.shape[2]
    datum.height = img.shape[0]
    datum.width = img.shape[1]
    datum.label = label
    datum.data = np.rollaxis(img, 2).tostring()
    return datum

def main(argv):
    Flags(argv)
    folders = ['train', 'test']
    for dir_name in folders:
        output_dir = os.path.join(Flags.output_dir, dir_name)
        os.system('rm -rf '+output_dir)
    
    for phase in folders:
        input_txt = os.path.join(Flags.input_dir, '%s.txt'%phase)
        lmdb_db = os.path.join(Flags.output_dir, phase)
        in_db = lmdb.open(lmdb_db, map_size = int(1e12))
        with in_db.begin(write=True) as in_txt:
            with open(input_txt, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter = ' ')
                for idx, (img_path, label) in enumerate(reader):
                    img = caffe.io.load_image(img_path)
                    label = int(label)
                    datum = make_datum(img, label)
                    new_key = '{:0>7d}'.format(idx)
                    in_txt.put(new_key, datum.SerializeToString())
                    if idx>=2000:
                        break
                    print new_key
        in_db.close()
    
if __name__ == '__main__':
    main(sys.argv)


