'''
Created on 16 May 2017

@author: mozat
'''
import labelmap_pb2
import sys
from google.protobuf import text_format

#https://developers.google.com/protocol-buffers/docs/reference/python/google.protobuf.text_format-module

labelmap = labelmap_pb2.LabelMap()
item = labelmap.item.add()
item.name = 'none_of_the_above'
item.label = 0
item.display_name = 'background'
item = labelmap.item.add()
item.name = 'aeroplane'
item.label = 1
item.display_name = 'aeroplane'

f = open('labelmap_zl.prototxt', "wt")
text_format.PrintMessage(labelmap, f)
f.close()