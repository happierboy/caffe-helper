'''
Created on 11 May 2017

@author: mozat
'''
import caffe
import numpy as np
import matplotlib.pyplot as plt

#init caffe
caffe.set_device(0)
caffe.set_mode_gpu()
#initialize solver
solver = caffe.SGDSolver('./model/solver.prototxt')
solver.net.copy_from('./model/bvlc_reference_caffenet.caffemodel')

#train model
niter = 10000
test_interval = 1000
train_loss = np.zeros(niter)
test_acc = np.zeros(int(np.ceil(niter/test_interval)))
total_test_size = 14043
test_batch_size = 50

for it in range(niter):
    solver.step(1) #SGD by caffe
    train_loss[it] = solver.net.blobs['loss'].data
    solver.test_nets[0].forward(start='conv1')
    if it%test_interval == 0:
        print "Iterating", it, 'testing'
        correct = 0
        for test_it in range(total_test_size/test_batch_size):#total test size over batch size
            solver.test_nets[0].forward()
            correct += sum(solver.test_nets[0].blobs['fc8_flickr'].data.argmax(1)==solver.test_nets[0].blobs['label'].data)
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


