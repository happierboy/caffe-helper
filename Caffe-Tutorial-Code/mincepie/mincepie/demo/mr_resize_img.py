'''
Created on 13 Apr 2017

@author: mozat
'''
import gflags
import glob
import numpy as np
import os
from PIL import Image
import cv2
import uuid
import sys
from mincepie import mapreducer
from mincepie import launcher

# gflags
gflags.DEFINE_string("input_folder", "",
                     "The folder that contains all input images, organized in synsets.")
gflags.DEFINE_string("output_folder", "",
                     "The folder that we write output features to")
FLAGS = gflags.FLAGS
FEA_DIM = 32*32
FEA_TYPE = np.float32

def process_image(filename, max_size=32):
    """Takes an image name and computes the gist feature
    """
    im = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_RGB2GRAY)
    im = cv2.resize(im, (max_size, max_size), cv2.INTER_CUBIC)
    return im.flatten()

class PygistMapper(mapreducer.BasicMapper):
    """The ImageNet Compute mapper. The input value would be a synset name.
    """
    def map(self, key, value):
        if type(value) is not str:
            value = str(value)
        files = glob.glob(os.path.join(FLAGS.input_folder, value, '*.jpg'))
        files.sort()
        features = np.zeros((len(files), FEA_DIM), dtype = FEA_TYPE)
        for i, f in enumerate(files):
            try:
                feat = process_image(f)
                features[i] = feat
            except Exception, e:
                print f, Exception, e
        outname = str(uuid.uuid4()) + '.npy'
        np.save(os.path.join(FLAGS.output_folder, outname), features)
        yield value, outname
# mapreducer.REGISTER_DEFAULT_MAPPER(PygistMapper)
mapreducer.REGISTER_MAPPER(PygistMapper)

class PygistReducer(mapreducer.BasicReducer):
    def reduce(self, key, values):
        """The Reducer basically renames the numpy file to the synset name
        Input:
            key: the synset name
            value: the temporary name from map
        """
        os.rename(os.path.join(FLAGS.output_folder, values[0]),
                os.path.join(FLAGS.output_folder, key + '.npy'))
        return key
# mapreducer.REGISTER_DEFAULT_REDUCER(PygistReducer)
mapreducer.REGISTER_REDUCER(PygistReducer)
mapreducer.REGISTER_DEFAULT_READER(mapreducer.FileReader)
mapreducer.REGISTER_DEFAULT_WRITER(mapreducer.FileWriter)

if __name__ == "__main__":
    import time
    sys.argv.append('--input=in.txt')
    sys.argv.append('--output=out.txt')
    sys.argv.append('--input_folder=./input')
    sys.argv.append('--output_folder=./output')
    sys.argv.append('--mapper=PygistMapper')
    sys.argv.append('--reducer=PygistReducer')
    sys.argv.append('--num_clients=3')
    start_time = time.time()
    launcher.launch(sys.argv)
    print time.time()-start_time
    
    start_time = time.time()
    dirs = ['./input/cat', './input/dog', './input/human']
    for ddir in dirs:
        files = glob.glob(os.path.join(ddir, '*.jpg'))
        files.sort()
        features = np.zeros((len(files), FEA_DIM), dtype = FEA_TYPE)
        for i, f in enumerate(files):
            feat = process_image(f)
            features[i] = feat
        outname = str(uuid.uuid4()) + '.npy'
        np.save(os.path.join('./output', outname), features)
    print time.time()-start_time
    
