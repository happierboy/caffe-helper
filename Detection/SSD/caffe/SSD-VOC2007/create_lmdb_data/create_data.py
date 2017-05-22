import os
import cv2
from caffe.proto import caffe_pb2
from google.protobuf import text_format
import lmdb
import random
import numpy as np
import xml.etree.ElementTree as ET


def ReadImageToCVMat(img_name, is_color=True):
    if is_color:
        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    return img

def ReadFileToBuffer(img_name):
    with open(img_name, 'rb') as fp:
        img_buffer = fp.read()
    return img_buffer

def ReadXMLToDict(labelfile_name):
    anno_data = {}
    xml = ET.ElementTree(file=labelfile_name)
    root = xml.getroot()
    anno_data['width'] = int(root.findall('./size/width')[0].text)
    anno_data['height'] = int(root.findall('./size/height')[0].text)
    anno_data['objects'] = []
    objects = root.findall('./object')
    for annotated_object in objects:
        bbxd_obj = {}
        bbxd_obj['name'] = annotated_object.find('name').text
        bbxd_obj['difficult'] = True if annotated_object.find('./difficult').text=="1" else False
        bbxd_obj['bbnd'] = {'xmin':int(annotated_object.find('./bndbox/xmin').text),
                          'ymin':int(annotated_object.find('./bndbox/ymin').text),
                          'xmax':int(annotated_object.find('./bndbox/xmax').text),
                          'ymax':int(annotated_object.find('./bndbox/ymax').text)
                          }
        anno_data['objects'].append(bbxd_obj)
    return anno_data

def make_datum(img_name, labelfile_name, name_to_label, is_encoded, encode_type, label_type):
    img = ReadImageToCVMat(img_name)
    height, width, channels = img.shape
    anno_datum = caffe_pb2.AnnotatedDatum()
    anno_datum.datum.height = height
    anno_datum.datum.width = width
    anno_datum.datum.channels = channels
    file_type = os.path.splitext(img_name)[1][1:]
    if is_encoded and encode_type==file_type:
        im_buffer = ReadFileToBuffer(img_name)
        anno_datum.datum.data = im_buffer
        anno_datum.datum.encoded = is_encoded
    elif is_encoded and encode_type!=file_type:
        im_buffer = cv2.imencode('.{encoded_type}'.format(encoded_tyep=encode_type), img)[1].tostring()
        anno_datum.datum.data = im_buffer
        anno_datum.datum.encoded = is_encoded
    else:
        anno_datum.datum.data = np.rollaxis(img, 2).tostring()
        anno_datum.encoded = is_encoded
    anno_datum.type = caffe_pb2.AnnotatedDatum.AnnotationType.Value('BBOX')
    if label_type =='xml':
        anno_data = ReadXMLToDict(labelfile_name)
        if anno_data['width']!=width or anno_data['height']!=height:
            raise Exception("img size not equal, {0}".format(img_name))
        all_labels = [name_to_label[bbxd_obj['name']] for bbxd_obj in anno_data['objects']]
        for label in set(all_labels):
            indexes = filter(lambda x: all_labels[x]==label, range(len(all_labels)))
            annotation_group = anno_datum.annotation_group.add()
            annotation_group.group_label = label
            for instance_id, index in enumerate(indexes):
                anno = annotation_group.annotation.add()
                anno.instance_id = instance_id
                anno.bbox.xmin = anno_data['objects'][index]['bbnd']['xmin']*1.0/width
                anno.bbox.xmax = anno_data['objects'][index]['bbnd']['xmax']*1.0/width
                anno.bbox.ymin = anno_data['objects'][index]['bbnd']['ymin']*1.0/height
                anno.bbox.ymax = anno_data['objects'][index]['bbnd']['ymax']*1.0/height
                anno.bbox.difficult = anno_data['objects'][index]['difficult']        
    else:
        raise NotImplementedError
    return anno_datum
    
def create_lmdb(phase, out_dir, data_root_dir, list_file, name_to_label, is_encoded, encode_type, label_type):
    with open(list_file, 'r') as lf:
        lines = []
        for line in lf.readlines():
            img_file, anno = line.strip('\n').split(' ')
            lines.append([img_file, anno])
        random.shuffle(lines)
        in_db = lmdb.open(out_dir, map_size = int(1e12))
        with in_db.begin(write=True) as in_txt:
            for idx, line in enumerate(lines):
                filename, labelname = os.path.join(data_root_dir, line[0]), os.path.join(data_root_dir, line[1])
                anno_datum = make_datum(filename, labelname, name_to_label, is_encoded, encode_type, label_type)
                new_key = '{:0>7d}_{}'.format(idx, line[0])
                in_txt.put(new_key, anno_datum.SerializeToString())
        in_db.close()
        
def read_labelmap(label_mapfile):
    label_map = caffe_pb2.LabelMap()
    with open(label_mapfile, 'r') as lmp:
        text_format.Merge(lmp.read(), label_map)
    name_to_label = dict()
    for item in label_map.item:
        name_to_label[item.name] = item.label
    return name_to_label

def create_dir(out_dir):
    if os.path.exists(out_dir):
        os.system("rm -rf {0}".format(out_dir))
    os.makedirs(out_dir)

def main():
    phases = ['test', 'trainval']
    root_dir = os.path.abspath(os.path.join(__file__, "../../"))
    labelmap_file = os.path.join(root_dir, 'create_lmdb_data/labelmap_voc.prototxt')
    name_to_label = read_labelmap(labelmap_file)
    data_root_dir = os.path.join(root_dir, 'data/VOCdevkit')
    is_encoded = True
    encode_type = 'jpg'
    label_type = 'xml'
    for phase in phases:
        out_dir = os.path.join(root_dir, 'lmdb/{0}'.format(phase))
        create_dir(out_dir)
        list_file = os.path.join(root_dir, 'create_lmdb_data/{0}.txt'.format(phase))
        create_lmdb(phase, out_dir, data_root_dir, list_file, name_to_label, is_encoded, encode_type, label_type)

if __name__ == '__main__':
    main()
