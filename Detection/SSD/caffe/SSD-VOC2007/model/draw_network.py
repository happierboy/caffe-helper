'''
Created on 12 May 2017

@author: mozat
'''
from google.protobuf import text_format
import caffe.draw
from caffe.proto import caffe_pb2
import gflags, sys

Flags = gflags.FLAGS

gflags.DEFINE_string('filename', 'VGG16_reduced.png;VGG16.png;VGG19.png', 'output filename')

models = ('VGG_ILSVRC_16_layers_fc_reduced_deploy.prototxt',
          'VGG_ILSVRC_16_layers_deploy.prototxt',
          'VGG_ILSVRC_19_layers_deploy.prototxt'
          )

def draw_model(model_name, output_name):
    #read NetParamemters only
    net = caffe_pb2.NetParameter()
    text_format.Merge(open(model_name).read(), net)
    caffe.draw.draw_net_to_file(net, output_name, 'LR', caffe.TEST)
    pass

if __name__ == '__main__':
    Flags(sys.argv)
    outputnames = Flags.filename.split(';')
    for (model_name, outputname) in zip(models, outputnames):
        draw_model(model_name, outputname)
    pass
    