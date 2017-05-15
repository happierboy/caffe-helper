'''
Created on 15 May 2017

@author: mozat
'''

import caffe
import numpy as np
import matplotlib.pyplot as plt

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

depreciated_net_file = './models/VGG_16_reduced/VGG_ILSVRC_16_layers_fc_reduced_deploy_depreciated.prototxt'
deperated_net_param = './models/VGG_16_reduced/VGG_ILSVRC_16_layers_fc_reduced_depreciated.caffemodel'


depreciated_net = caffe.Net(depreciated_net_file, deperated_net_param, caffe.TEST)
params = depreciated_net.params.copy()
del depreciated_net


new_net_file = './models/VGG_16_reduced/VGG_ILSVRC_16_layers_fc_reduced_deploy.prototxt'
out_net_param = './models/VGG_16_reduced/VGG_ILSVRC_16_layers_fc_reduced.caffemodel'
net = caffe.Net(new_net_file, caffe.TEST)
for key, value in net.params.iteritems():
    net.params[key][0].data[...] = params[key][0].data[...]
    net.params[key][0].diff[...] = params[key][0].diff[...]
    net.params[key][1].data[...] = params[key][1].data[...]
    net.params[key][1].diff[...] = params[key][1].diff[...]
    show_data(net.params[key].data[0],1, 0.5, 'conv3')
net.save(out_net_param)