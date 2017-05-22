'''
Created on 16 May 2017

@author: mozat
'''


import os
import cv2
root_dir = '/home/mozat/caffe-study/Detection/SSD/caffe/SSD-VOC2007/data/VOCdevkit/'
sub_dir = 'ImageSets/Main'

all_dirs = ['trainval', 'test']
names = ['VOC2007', 'VOC2012']
for a_dir in all_dirs:
    dst_file = os.path.join(os.getcwd(), '{}.txt'.format(a_dir))
    with open(dst_file, 'w') as ofp:
        for name in names:
            dataset_file = os.path.join(os.path.join(root_dir, name), '{0}/{1}.txt'.format(sub_dir, a_dir))
            if not os.path.exists(dataset_file):
                continue
            
            with open(dataset_file, 'r') as in_fp:
                for line in in_fp:
                    line = line.strip()
                    img_name = '{0}/JPEGImages/{1}.jpg'.format(name, line)
                    label_name = '{0}/Annotations/{1}.xml'.format(name, line)
                    ofp.write('{0} {1}\n'.format(img_name, label_name))
    if a_dir is 'trainval':
        lines = []
        with open(dst_file, 'r') as in_fp:
            for line in in_fp:
                lines.append(line)
        import random
        random.shuffle(lines)
        with open(dst_file, 'w') as ofp:
            for line in lines:
                ofp.write(line)
    if a_dir is 'test':
        new_dst_file = os.path.join(os.getcwd(), '{0}_name_size.txt'.format(a_dir))
        with open(new_dst_file, 'w') as ofp:
            with open(dst_file, 'r') as in_fp:
                for line in in_fp:
                    img_name = line.split(' ')[0]
                    shape = cv2.imread(os.path.join(root_dir, img_name)).shape
                    img_idx = img_name.split('JPEGImages/')[1].replace('.jpg', '')
                    ofp.write('{0} {1} {2}\n'.format(img_idx, shape[0], shape[1]))    