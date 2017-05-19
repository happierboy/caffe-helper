'''
Created on 16 May 2017

@author: mozat
'''
import os
import cv2
import xml.etree.ElementTree as ET
from xml.dom import minidom

def write_dict2xml(xml_info):
    xmlFile = xml_info['xmlFile']
    root = ET.Element('annotation')
    for item_key in ['total_num', 'foldername', 'filename', 'segmented']:
        ele = ET.SubElement(root, item_key)
        ele.text = str(xml_info[item_key])
    size = ET.SubElement(root, 'size')
    for idx, item_key in enumerate(['height', 'width', 'channel']):
        ele = ET.SubElement(size, item_key)
        ele.text = str(xml_info['img_size'][idx])
    owner = ET.SubElement(root, 'owner')
    for item_key, item_value in xml_info['owner'].iteritems():
        ele = ET.SubElement(owner, item_key)
        ele.text = str(item_value)
    source = ET.SubElement(root, 'source')
    for item_key, item_value in xml_info['source'].iteritems():
        ele = ET.SubElement(source, item_key)
        ele.text = str(item_value)
    for anno_object in xml_info['object']:
        xml_object = ET.SubElement(root, 'object')
        for item_key in ['name', 'pose', 'truncated','difficult']:
            ele = ET.SubElement(xml_object, item_key)
            ele.text = str(anno_object[item_key])
        bndbox = ET.SubElement(xml_object, 'bndbox')
        for item_key in ['xmin', 'ymin', 'xmax', 'ymax']:
            ele = ET.SubElement(bndbox, item_key)
            ele.text = str(anno_object['bndbox'][item_key])
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent = "   ")
    with open(xmlFile, 'w') as f:
        f.write(xmlstr)
    pass

def create_dict(label_file, label_dir, img_dir, xml_dir, base_dir):
    xml_info = {}
    with open(os.path.join(label_dir, label_file), 'r') as fidin:
        xml_info['total_num'] = fidin.readline().strip('\n')
        xml_info['xmlFile'] = os.path.join(xml_dir, label_file.replace('.txt', '.xml'))
        xml_info['foldername'] = base_dir
        imageFile = os.path.join(img_dir, label_file.replace('.txt', '.JPEG'))
        xml_info['filename'] = imageFile
        xml_info['img_size'] = cv2.imread(imageFile).shape
        xml_info['segmented'] = 0
        xml_info['source'] = {'database': 'Fashion', 'annotation':base_dir}
        xml_info['owner'] = {'flickrid': 'happierboy', 'name': 'zhangli'}
        xml_info['object'] = []
        for line in fidin:
            data = line.strip('\n')
            datas = data.split(' ')
            anno_object = {}
            anno_object['name'] = datas[0]
            anno_object['pose'] = 'Unspecified'
            anno_object['truncated'] = 0
            anno_object['difficult'] = 0
            anno_object['bndbox'] = {'xmin': int(datas[1]), 'ymin': int(datas[2]),
                                'xmax': int(datas[3]), 'ymax': int(datas[4])}
            xml_info['object'].append(anno_object)
    return xml_info
            

def create():
    label_dir = './BBox-Label-Tool/Labels/1'
    img_dir = './BBox-Label-Tool/Images/1' 
    xml_dir = './BBox-Label-Tool/Annotations/1'
    base_dir = './BBox-Label-Tool'
    for label_file in os.listdir(label_dir):
        xml_info = create_dict(label_file, label_dir, img_dir, xml_dir, base_dir)
        write_dict2xml(xml_info)
            
if __name__ == '__main__':
    create()
