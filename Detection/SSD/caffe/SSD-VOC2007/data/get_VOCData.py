'''
Created on 16 May 2017

@author: mozat
'''
import os
os.system('wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar')
os.system('wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar')
os.system('wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar')
# Extract the data.
os.system('tar -xvf VOCtrainval_11-May-2012.tar')
os.system('tar -xvf VOCtrainval_06-Nov-2007.tar')
os.system('tar -xvf VOCtest_06-Nov-2007.tar')