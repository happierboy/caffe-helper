'''
Created on 11 May 2017

@author: mozat
'''
import caffe
import numpy as np
import cv2

#all in RGB colorspace
blob = caffe.proto.caffe_pb2.BlobProto()
data = open('ilsvrc_imagenet_mean.binaryproto', 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
out = arr[0]
np.save('ilsvrc_imagenet_mean.npy', out )
cv2.imwrite('ilsvrc_imagenet_mean.png', cv2.cvtColor(np.asarray(out.transpose(1,2,0), dtype=np.uint8), cv2.COLOR_RGB2BGR))