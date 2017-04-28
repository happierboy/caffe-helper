'''
Created on 28 Apr 2017

@author: mozat
'''

caffe_root = '/home/mozat/git/'
import sys
sys.path.insert(0, caffe_root+'python')
import caffe
from caffe import layers as L, params as P
from caffe.proto import caffe_pb2
import os

def generate_lenet(lmdb, batch_size):
    n = caffe.NetSpec()
    n.data, n.label = L.Data(batch_size = batch_size, backend = P.Data.LMDB, source = lmdb, 
                             transform_param=dict(scale=1./255), ntop=2)
    n.conv1 = L.Convolution(n.data, kernel_size = 5, num_output = 20, weight_filler=dict(type='xavier'))
    n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=50, weight_filler=dict(type='xavier'))
    n.pool2 = L.Pooling(n.conv2, kernel_size = 2, stride=2, pool=P.Pooling.MAX)
    n.fc1 = L.InnerProduct(n.pool2, num_output=500, weight_filler=dict(type='xavier'))
    n.relu1 = L.ReLU(n.fc1, in_place = True)
    n.score = L.InnerProduct(n.relu1, num_output = 10, weight_filler=dict(type='xavier'))
    n.loss =  L.SoftmaxWithLoss(n.score, n.label)
    return n

def lenet(lmdb, batch_size):
    n = generate_lenet(lmdb, batch_size)
    return n.to_proto()

def write_net():
    with open(train_net_file, 'w') as f:
        f.write(str(lenet(train_net_lmdb, 64)))
    with open(test_net_file, 'w') as f:
        f.write(str(lenet(test_net_lmdb, 64)))
        
def generate_solver():
    s = caffe_pb2.SolverParameter()
    path = os.path.dirname(os.path.abspath('.'))
    s.train_net = os.path.join(path, train_net_file)
    s.test_net.append(os.path.join(path, test_net_file))
    s.test_interval = 500
    s.test_iter.append(100)
    s.max_iter = 5000
    s.base_lr = 0.001 
    s.momentum = 0.9
    s.weight_decay = 0.0005
    s.lr_policy = "inv"
    s.display = 100
    s.snapshot = 5000
    s.snapshot_prefix = "lenet_train/lenet_train"
    s.type = "SGD"
    s.solver_mode = caffe_pb2.SolverParameter.GPU
    return s

def write_solver():
    s = generate_solver()
    with open(solver_file, 'w') as f:
        f.write(str(s))

if __name__ == '__main__':
    train_net_file = 'network_synthesized/lenet_train_py.prototxt'
    test_net_file = 'network_synthesized/lenet_test_py.prototxt'
    train_net_lmdb = '/home/mozat/caffe-study/Caffe-Tutorial-Code/Caffe-Mnist/mnist-data/train_lmdb'
    test_net_lmdb = '/home/mozat/caffe-study/Caffe-Tutorial-Code/Caffe-Mnist/mnist-data/test_lmdb'
    solver_file = './network_synthesized/lenet_generated_solver.prototxt'
    write_net()
    write_solver()