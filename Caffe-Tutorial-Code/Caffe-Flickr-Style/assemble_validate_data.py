'''
Created on 9 May 2017

@author: mozat
'''

import shutil
import os, csv
import cv2
import numpy as np

current_dir = os.getcwd()
train_dir = os.path.join(current_dir, 'data/flickr_style/images')
txt_dir = os.path.join(current_dir, 'data/flickr_style')
out_dir = os.path.join(current_dir, 'filter_data/')

invalidate_img = cv2.imread('/home/mozat/caffe-study/Caffe-Tutorial-Code/Caffe-Flickr-Style/data/flickr_style/experiment/0/9164102573_eb24fe482b.jpg')


def filter_data(phase='training'):
    if phase == 'training':
        txt_file = os.path.join(txt_dir, 'train.txt')
        new_txt = os.path.join(out_dir, 'train.txt')
        new_out_dir = os.path.join(out_dir, 'train')
    if phase == 'testing':
        txt_file = os.path.join(txt_dir, 'test.txt')
        new_txt = os.path.join(out_dir, 'test.txt')
        new_out_dir = os.path.join(out_dir, 'test')
    with open(txt_file, 'r') as fp:
        with open(new_txt, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = ['img_name', 'label'], delimiter = ' ')
            for line in fp:
                fields = line.strip().split(' ')
                label = fields[1]
                img = cv2.imread(fields[0])
                if np.array_equal(img, invalidate_img):
                    continue
                else:
                    new_img_name = os.path.join(new_out_dir, os.path.basename(fields[0]))
                    shutil.copy(fields[0], new_img_name)
                    writer.writerow({'img_name': new_img_name, 'label': int(label)})
                
if __name__ == '__main__':
    filter_data('training')
    filter_data('testing')    
