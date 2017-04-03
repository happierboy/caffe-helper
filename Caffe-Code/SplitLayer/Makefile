CC=g++

all:
	$(CC) -I/home/mozat/git/caffe/include -I/home/mozat/git/caffe/build/src -I/usr/local/cuda/include \
	test_net_init.cpp \
    -L/usr/local/lib/ -lprotobuf \
    -L/usr/local/cuda/lib64 -lcudart -lcublas -lcurand -lboost_system -lboost_filesystem\
    -L/home/mozat/git/caffe/build/lib/ -lcaffe \
    -o test_net_init
