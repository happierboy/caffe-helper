'''
Created on 26 Apr 2017

@author: mozat
'''
from caffe import layers as L, params as P
import caffe

def lenet(lmdb, batch_size):
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
    return n.to_proto()


def write_proto():
    with open('./network/lenet_train_py.prototxt', 'w') as f:
        f.write(str(lenet('/home/mozat/workspace/Caffe-Mnist/mnist-data/train_lmdb', 64)))
    with open('./network/lenet_test_py.prototxt', 'w') as f:
        f.write(str(lenet('/home/mozat/workspace/Caffe-Mnist/mnist-data/validate_lmdb', 64)))

def train():
    caffe.set_device(0)
    caffe.set_mode_gpu()
    solver = caffe.SGDSolver('./network/lenet_solver.prototxt')
    for k, v in solver.net.blobs.items():
        print k, v.data.shape
    solver.net.forward()
    solver.test_nets[0].forward()
    print len(solver.test_nets)
    solver.net.backward()
    solver.step(1)
    solver.solve()
        
if __name__ == '__main__':
#     write_proto()
    train()