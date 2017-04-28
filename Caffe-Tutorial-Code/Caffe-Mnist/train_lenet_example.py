'''
Created on 26 Apr 2017

@author: mozat
'''
import caffe
from matplotlib import pyplot
import numpy as np

def train_play():
    caffe.set_device(0)
    caffe.set_mode_gpu()
    solver = caffe.SGDSolver('./network/lenet_solver.prototxt')
    for k, v in solver.net.blobs.items():
        print k, v.data.shape
    solver.net.forward()
    solver.test_nets[0].forward()
    pyplot.imshow(solver.net.blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28), cmap='gray')
    pyplot.axis('off')
    pyplot.show()
    solver.step(1) #one step will compute iter_size*batch_size
    pyplot.figure()
    pyplot.imshow(solver.net.params['conv1'][0].diff[:,0].reshape(4,5,5,5).transpose(0,2,1,3).reshape(4*5,5*5), cmap='gray')
    #net.params['conv']: the 0th is the weight, the 1st is the bias 
    pyplot.axis('off')
    solver.net.backward()
    solver.solve()

def train():
    caffe.set_device(0)
    caffe.set_mode_gpu()
    solver = caffe.SGDSolver('./network/lenet_single_solver.prototxt')
    niter = 500
    test_interval = 25
    train_loss = np.zeros(niter)
    test_acc = np.zeros(int(np.ceil(niter/test_interval)))
    output = np.zeros((niter, 8, 10))
    for it in range(niter):
        solver.step(1) #SGD by Caffe
        train_loss[it] = solver.net.blobs['loss'].data
        # (start the forward pass at conv1 to avoid loading new data)
        solver.test_nets[0].forward(start='conv1')
        output[it] = solver.test_nets[0].blobs['ip2'].data[:8]
        if it%test_interval ==0:
            print "Iteration", it, 'testing...'
            correct = 0
            for test_it in range(100):
                solver.test_nets[0].forward()
                correct += sum(solver.test_nets[0].blobs['ip2'].data.argmax(1)==solver.test_nets[0].blobs['label'].data)
            test_acc[it/test_interval] = correct / 1e4
    _, ax1 = pyplot.subplots()
    ax2 = ax1.twinx()
    ax1.plot(np.arange(niter), train_loss)
    ax2.plot(test_interval*np.arange(len(test_acc)), test_acc, 'r')
    ax1.set_xlabel('iteration')
    ax1.set_ylabel('train loss')
    ax2.set_ylabel('test accuracy')
    ax2.set_title('Test Accuracy: {:.2f}'.format(test_acc[-1]))
    pyplot.show()
#     for i in range(8):
#         pyplot.figure(figsize=(2, 2))
#         pyplot.imshow(solver.test_nets[0].blobs['data'].data[i, 0], cmap='gray')
#         pyplot.figure(figsize=(10, 2))
#         pyplot.imshow(output[:50, i].T, interpolation='nearest', cmap='gray')
#         pyplot.xlabel('iteration')
#         pyplot.ylabel('label')
#         pyplot.show()


if __name__ == '__main__':
    train()