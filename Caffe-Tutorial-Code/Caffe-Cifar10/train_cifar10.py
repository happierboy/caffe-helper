'''
Created on 3 May 2017

@author: mozat
'''
import caffe
from caffe.proto import caffe_pb2
import lmdb
import numpy as np
from google.protobuf import text_format
import matplotlib.pyplot as plt 

#open train lmdb
train_lmdb = './cifar10_train_lmdb'
test_lmdb = './cifar10_test_lmdb'
in_db = lmdb.open(train_lmdb, readonly=True)
total_train_size = in_db.stat()['entries']
in_db.close()
print 'total_train_size', total_train_size
#open test lmdb
in_db = lmdb.open(test_lmdb, readonly=True)
total_test_size = in_db.stat()['entries']
in_db.close()
print 'total_test_size', total_test_size

#open NetParamters and get batch_size
net_param = caffe_pb2.NetParameter()
text_format.Merge(open('./network/cifar10_quick_train_test.prototxt', 'rb').read(), net_param)
test_batch_size = net_param.layer[1].data_param.batch_size
print test_batch_size


#start to train  at the first stage
caffe.set_device(0)
caffe.set_mode_gpu()
solver = caffe.SGDSolver('./network/cifar10_quick_solver.prototxt')
niter = 10000
test_interval = 500
train_loss = np.zeros(niter)
test_acc = np.zeros(int(np.ceil(niter/test_interval)))

output = np.zeros((niter, 8, 10)) #see solver.net.blobs['ip2'].data.shape
for it in range(niter):
    if it == 4000:
        del solver
        solver = caffe.SGDSolver('./network/cifar10_quick_solver_lr1.prototxt')
        solver.net.copy_from('./snapshot/cifar10_quick_iter_4000.caffemodel')
        pass
    solver.step(1) #SGD by caffe
    train_loss[it] = solver.net.blobs['loss'].data
    solver.test_nets[0].forward(start='conv1')
    output[it] = solver.test_nets[0].blobs['ip2'].data[:8]
    if it%test_interval == 0:
        print "Iterating", it, 'testing'
        correct = 0
        for test_it in range(total_test_size/test_batch_size):#total test size over batch size
            solver.test_nets[0].forward()
            correct += sum(solver.test_nets[0].blobs['ip2'].data.argmax(1)==solver.test_nets[0].blobs['label'].data)
        test_acc[it/test_interval] = correct*1.0 / total_test_size
        
_, ax1 = plt.subplots()
ax2= ax1.twinx()
ax1.plot(np.arange(niter), train_loss)
ax1.set_xlabel('iteration')
ax1.set_ylabel('train loss')
ax2.plot(test_interval*np.arange(len(test_acc)), test_acc, 'r')
ax2.set_ylabel('test loss')
ax2.set_title('test accuracy, {:.2f}'.format(test_acc[-1]))
plt.show()




