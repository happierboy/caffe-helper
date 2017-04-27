'''
Created on 13 Apr 2017

@author: mozat
'''
from mincepie import mapreducer
from mincepie import launcher
class WordCountMapper(mapreducer.BasicMapper):
    """The wordcount mapper"""
    def map(self, key, value):
#         print key, value
        with open(value,'r') as fid:
            for line in fid:
                for word in line.split():
                    yield word, 1
mapreducer.REGISTER_DEFAULT_MAPPER(WordCountMapper)

class WordCountReducer(mapreducer.BasicReducer):
    """The wordcount reducer"""
    def reduce(self, key, value):
        return sum(value)
mapreducer.REGISTER_DEFAULT_REDUCER(WordCountReducer)

import sys
sys.argv.append('--input=zen.txt')
launcher.launch(sys.argv)