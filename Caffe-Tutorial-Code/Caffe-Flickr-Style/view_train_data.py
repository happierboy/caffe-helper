'''
Created on 9 May 2017

@author: mozat
'''
import os
import csv
import shutil
current_dir = os.getcwd()
in_txt = os.path.join(current_dir, 'filter_data/train.txt')
out_dir = os.path.join(current_dir, 'filter_data/experiment')

with open(in_txt, 'r') as csvfile:
    reader = csv.reader(csvfile,  delimiter=' ')
    for idx, line in enumerate(reader):
        label = line[1]
        img = line[0]
        if not os.path.exists(os.path.join(out_dir, label)):
            os.makedirs(os.path.join(out_dir, label))
        shutil.copyfile(img, os.path.join(os.path.join(out_dir, label), os.path.basename(img)))
        if idx>=1000:
            break