#!/usr/bin/env python
"""
Draw a graph of the net architecture.
"""
from google.protobuf import text_format

import caffe.draw
from caffe.proto import caffe_pb2
import gflags
import sys
import os
cwd = os.getcwd()
Flags = gflags.FLAGS
gflags.DEFINE_string('input_net_proto_file', os.path.join(cwd, 'network/cifar10_quick_train_test.prototxt'), 'define input net proto file')
gflags.DEFINE_string('output_image_file', os.path.join(cwd, 'network/cifar10_quick_train_test.png'), 'define output png file')
gflags.DEFINE_string('phase', 'TRAIN',('Which network phase to draw: can be TRAIN, '
                              'TEST, or ALL.  If ALL, then all layers are drawn '
                              'regardless of phase.'))
gflags.DEFINE_string('rankdir', 'LR', 'define rank dir')

def main():
    Flags(sys.argv)
    #read NetParamemters only
    net = caffe_pb2.NetParameter()
    text_format.Merge(open(Flags.input_net_proto_file).read(), net)
    #to initialize network
    #net = caffe.Net(proto_name, phase)
    #net = caffe.Net(proto_name, model_name, phase)
    #net.params['conv1'] 0:weight, 1:bias,
    #net.params['ip'] 0: weight, 1: bias
    print('Drawing net to %s' % Flags.output_image_file)
    phase=None;
    if Flags.phase == "TRAIN":
        phase = caffe.TRAIN
    elif Flags.phase == "TEST":
        phase = caffe.TEST
    elif Flags.phase != "ALL":
        raise ValueError("Unknown phase: " + Flags.phase)
    caffe.draw.draw_net_to_file(net, Flags.output_image_file, Flags.rankdir, phase)

if __name__ == '__main__':
#     sys.argv.append('--input_net_proto_file=network/cifar10_quick.prototxt')
#     sys.argv.append('--output_image_file=network/cifar10_quick.png')
    sys.argv.append('--phase=TEST')
    main()
