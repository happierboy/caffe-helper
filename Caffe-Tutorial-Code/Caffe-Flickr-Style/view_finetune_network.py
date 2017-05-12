'''
Created on 11 May 2017

@author: mozat
'''
import numpy as np
import caffe
from caffe.proto import caffe_pb2
from google.protobuf import text_format

def load_img(img_name):
    img = caffe.io.load_image(img_name)
    return img
    
def load_mean(binary_mean_file):
    data = caffe_pb2.BlobProto()
    mean_data = open(binary_mean_file, 'rb').read()
    data.ParseFromString(mean_data)
    data_array = caffe.io.blobproto_to_array(data)
    return data_array[0]
    
def test():
    #test deploy protocol
    net_param_file = './model/deploy-zl.prototxt'
    net_param = caffe_pb2.NetParameter()
    text_format.Merge(open(net_param_file, 'r').read(), net_param)
    print net_param.name
    
    #init Solver
    caffe.set_device(0)
    caffe.set_mode_gpu()
    net = caffe.Net('./model/deploy-zl.prototxt',
                    './snapshot/finetune_flickr_style_iter_10000.caffemodel',
                    caffe.TEST)
    mean_file = './mean_data/ilsvrc_imagenet_mean.binaryproto'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_raw_scale('data', 255)
    transformer.set_mean('data', load_mean(mean_file).mean(1).mean(1))
    transformer.set_transpose('data', (2,0,1))
    img_name = './filter_data/train/13046406493_ceaff2892f.jpg'
    img = load_img(img_name)
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
#     inputData=net.blobs['data'].data
#     img = transformer.deprocess('data', inputData)
    net.forward()
    feat = net.blobs['prob'].data
    print feat.shape
    print feat, feat.argmax()
    


if __name__ == '__main__':
    test()
