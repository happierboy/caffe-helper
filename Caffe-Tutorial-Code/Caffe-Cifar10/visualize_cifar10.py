'''
Created on 3 May 2017

@author: mozat
'''
import numpy as np
import sys
sys.path.append('/home/mozat/git/python')

import caffe
from caffe.proto import caffe_pb2
from google.protobuf import text_format
import matplotlib.pyplot as plt
import cv2

#http://blog.csdn.net/u010417185/article/details/52137825
def show_data(data, padsize=1,padval=0, title_name = ''):#tuple multiplcation is to multiply the tuple element by time
    data -= data.min()
    data /= data.max()
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n**2 -data.shape[0]), (0, padsize), (0,padsize))+ ((0, 0),) * (data.ndim - 3) #+ operator is to concatenate the tuple
    data = np.pad(data, padding, mode='constant', constant_values = (padval, padval)) #((before_1, after_1), ... (before_N, after_N)) unique end values
    data = data.reshape((n,n)+data.shape[1:]).transpose((0,2,1,3) + tuple(range(4, data.ndim + 1))) 
    data = data.reshape((n*data.shape[1], n*data.shape[3]) + data.shape[4:])
    plt.figure()
    plt.imshow(data,cmap='gray')
    plt.axis('off')
    plt.title(title_name)
    plt.show()

def read_image_rgb(im_name, show_bit):
#     img = cv2.imread(im_name)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = np.asarray(img, dtype=np.float32)/255
    img = caffe.io.load_image(im_name) 
    if show_bit:
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    return img

def load_mean_binary(mean_file):
    blob = caffe_pb2.BlobProto()
    bin_mean = open(mean_file, 'rb').read()#proto file
    blob.ParseFromString(bin_mean)
    arr_mean = caffe.io.blobproto_to_array(blob)
    return arr_mean[0] 

def load_mean_npy(mean_file):
    npy_mean = np.load(mean_file) #npy file
    return npy_mean[0] #n*c*H*W

def print_net_info(net):
    print "net blobs items: "
    for k, v in net.blobs.items():
        print (k,v.data.shape)
    print "net params items: "
    for k,v in net.params.items():
        print k, "W Shape", v[0].diff.shape, "B Shape", v[1].diff.shape
     
def read_net(net_file):
    net_param = caffe_pb2.NetParameter()
    text_format.Merge(open(net_file, 'r').read(), net_param)
    print net_param #as a struct, visit is by net_param.layer[0] etc
    return net_param

def read_solver(solver_file):
    solver = caffe.SGDSolver(solver_file)
    print solver.net.blobs.items()
    print len(solver.test_nets)
    return solver

# #init network
caffe.set_mode_gpu()
net = caffe.Net('./network/cifar10_quick_deploy.prototxt',
                './snapshot/cifar10_quick_iter_5000.caffemodel',
                caffe.TEST)
img = read_image_rgb('cat.jpg', show_bit=False)
npy_mean = load_mean_npy('mean.npy')
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1)) #change axis to C*H*W
transformer.set_mean('data', npy_mean.mean(1).mean(1)) #R, G, B mean value 1*C
transformer.set_raw_scale('data', 255)  #blob_value = input_data * scale
transformer.set_channel_swap('data', (2,1,0)) #from RGB to BGR, as orginal mean is BGR
net.blobs['data'].data[...] = transformer.preprocess('data', img)
inputData=net.blobs['data'].data

net.forward()
print "visualize the prob"
feat = net.blobs['prob'].data[0]
print feat.argmax(), feat.max(), feat


print "visualize the blob data"
print 'blob conv1', net.blobs['conv1'].data[0].shape
show_data(net.blobs['conv1'].data[0],1,0,'conv1')
print "blob pool1", net.blobs['pool1'].data.shape
show_data(net.blobs['pool1'].data[0],1,0,'pool1')
print "blob conv2", net.blobs['conv2'].data.shape
show_data(net.blobs['conv2'].data[0],1, 0.5, 'conv2')
print "blob pool2", net.blobs['pool2'].data.shape
show_data(net.blobs['pool2'].data[0],1,0.5, 'pool2')
print "blob conv3", net.blobs['conv3'].data.shape
show_data(net.blobs['conv3'].data[0],1, 0.5, 'conv3')
print "blob pool3", net.blobs['pool3'].data.shape
show_data(net.blobs['pool3'].data[0],1, 0.2, 'pool3')
print "visulize the param data"
print "conv1 param weight", net.params['conv1'][0].data.shape
show_data(net.params['conv1'][0].data.reshape(32*3, 5, 5), 1,0,'conv1_data')
print "conv2 param weight", net.params['conv2'][0].data.shape
show_data(net.params['conv2'][0].data.reshape(32**2,5,5), 1,0,'conv2 params')
print "conv3 param weight", net.params['conv3'][0].data.shape
show_data(net.params['conv3'][0].data.reshape(64*32,5,5)[:1024], 1,0, 'conv3 params')

