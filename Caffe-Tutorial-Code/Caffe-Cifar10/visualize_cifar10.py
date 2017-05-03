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


# #init network
caffe.set_mode_gpu()
net = caffe.Net('./network/cifar10_quick_train_test.prototxt', caffe.TRAIN)
#  
# blobs_shape = [(k,v.data.shape) for k, v in net.blobs.items()]
# print blobs_shape
#  
# netparam_shape = [(k, v[0].diff.shape, v[1].diff.shape) for k,v in net.params.items()]
# print netparam_shape
# 
# #init netparameters
# net_param = caffe_pb2.NetParameter()
# text_format.Merge(open('./network/cifar10_quick_train_test.prototxt', 'r').read(), net_param)
# print net_param
# 
# #init solver
# solver = caffe.SGDSolver('./network/cifar10_quick_solver.prototxt')
# print solver.net.blobs.items()
# print len(solver.test_nets)

#read image
# img = cv2.imread('cat1.jpg')
# cv2.imshow("cat.jpg", img)
# cv2.waitKey()
# img = caffe.io.load_image('cat1.jpg') #This will directly read to RGB colorspace
img = cv2.imread('cat1.jpg') #read to BGR colorspace
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.asarray(img, dtype=np.float32)/255
plt.imshow(img)
plt.axis('off')
plt.show()


#read binary bin file
binMean = './mean.binaryproto'
blob = caffe_pb2.BlobProto()
bin_mean = open(binMean, 'rb').read()
blob.ParseFromString(bin_mean)
arr = caffe.io.blobproto_to_array(blob)
print arr.shape
npy_mean = np.load('mean.npy')
print npy_mean.shape
print np.array_equal(arr, npy_mean)


#convert img and subtract mean
print net.blobs['data'].data.shape
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1)) #change axis to C*H*W
transformer.set_mean('data', npy_mean[0].mean(1).mean(1))
transformer.set_raw_scale('data', 255)  
transformer.set_channel_swap('data', (2,1,0)) #from RGB to BGR, as orginal mean is BGR
net.blobs['data'].data[...] = transformer.preprocess('data', img)
net.blobs['data'].reshape(1,3,32,32)
inputData=net.blobs['data'].data

plt.figure()
plt.subplot(1,2,1),plt.title("origin")
plt.imshow(img)
plt.axis('off')
plt.subplot(1,2,2),plt.title("subtract mean")
plt.imshow(transformer.deprocess('data', inputData[0]))
plt.axis('off')
plt.show()

