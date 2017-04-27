'''
Created on 24 Apr 2017

@author: mozat
'''

import os
import sys
dir_name = [
    'train-images-idx3-ubyte',
    'train-labels-idx1-ubyte',
    't10k-images-idx3-ubyte',
    't10k-labels-idx1-ubyte'
    ]
for fname in dir_name:
    os.system("wget --no-check-certificate http://yann.lecun.com/exdb/mnist/{fname}.gz".format(fname=fname))
    os.system("gunzip {fname}.gz".format(fname=fname))
    