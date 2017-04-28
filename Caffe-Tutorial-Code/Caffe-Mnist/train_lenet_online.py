'''
Created on 28 Apr 2017

@author: mozat
'''
import caffe
from caffe.proto import caffe_pb2
from caffe import layers as L, params as P
import os
train_net_path = os.path.join(os.getcwd(), 'network_synthesized/custom_auto_train.prototxt')
test_net_path = os.path.join(os.getcwd(), 'network_synthesized/custom_auto_test.prototxt')
solver_config_path = os.path.join(os.getcwd(), 'network_synthesized/custom_auto_solver.prototxt')

def custom_net(lmdb, batch_size):
    n = caffe.NetSpec()
    n.data, n.label = L.Data(batch_size = batch_size, backend=P.Data.LMDB, 
                             source = lmdb, transform_param = dict(scale=1./255.0),
                             ntop = 2)
    n.conv1 = L.Convolution(n.data, kernel_size = 5, num_output=20, weight_filler=dict(type='xavier'))
    n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    n.score = L.InnerProduct(n.pool1, num_output = 10, weight_filler = dict(type='xavier'))
    n.loss = L.SoftmaxWithLoss(n.score, n.label)
    return n.to_proto()

with open(train_net_path, 'w') as f:
    f.write(str(custom_net('/home/mozat/caffe-study/Caffe-Tutorial-Code/Caffe-Mnist/mnist-data/train_lmdb', 64)))    
with open(test_net_path, 'w') as f:
    f.write(str(custom_net('/home/mozat/caffe-study/Caffe-Tutorial-Code/Caffe-Mnist/mnist-data/test_lmdb', 1000)))
    
s = caffe_pb2.SolverParameter()
s.random_seed = 0xCAFFE
s.train_net = train_net_path
s.test_net.append(test_net_path)
s.test_interval = 500
s.test_iter.append(100)
s.max_iter = 10000
s.type = "SGD"
s.base_lr = 0.01
s.momentum = 0.9
s.weight_decay = 5e-4
s.lr_policy = 'inv'
s.gamma = 0.0001
s.power = 0.75
s.display = 1000
s.snapshot = 5000
s.snapshot_prefix = "lenet_train/lenet_train"
s.solver_mode = caffe_pb2.SolverParameter.GPU
with open(solver_config_path, 'w') as f:
    f.write(str(s))

###load the solver and create train and test nets
from numpy import *
import numpy as np
from matplotlib.pyplot import *
solver = None
solver = caffe.get_solver(solver_config_path)
niter = 50
test_interval = niter / 10
train_loss = zeros(niter+1)
test_acc = zeros(int(np.ceil(niter / test_interval))+1)
for it in range(niter+1):
    solver.step(1)  # SGD by Caffe
    train_loss[it] = solver.net.blobs['loss'].data
    if it % test_interval == 0:
        print 'Iteration', it, 'testing...'
        correct = 0
        total_label = []
        for test_it in range(1):
            total_label.extend(list(solver.test_nets[0].blobs['label'].data.flatten()))
            solver.test_nets[0].forward()
            correct += sum(solver.test_nets[0].blobs['score'].data.argmax(1)
                           == solver.test_nets[0].blobs['label'].data)
        hist(total_label, range(10))
        show()
        test_acc[it // test_interval] = correct / 1e3

_, ax1 = subplots()
ax2 = ax1.twinx()
ax1.plot(arange(niter+1), train_loss)
ax2.plot(test_interval * arange(len(test_acc)), test_acc, 'r')
ax1.set_xlabel('iteration')
ax1.set_ylabel('train loss')
ax2.set_ylabel('test accuracy')
ax2.set_title('Custom Test Accuracy: {:.2f}'.format(test_acc[-1]))
show()



