'''
Created on 16 May 2017

@author: mozat
'''
import os
import sys
import cv2
from itertools import islice
from xml.dom.minidom import Document, parse
from xml.etree.ElementTree import ElementTree as ET

labels = './BBox-Label-Tool/Labels/1'
imgpath = './BBox-Label-Tool/Images/1' 
xmlpath_new = './BBox-Label-Tool/Annotations/1'
foldername='./BBox-Label-Tool'

def insert_object(doc, datas):
    obj = doc.createElement('object')
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode(datas[0]))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    
    # insert bndbox
    bndbox = doc.createElement('bndbox')
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(datas[1])))
    bndbox.appendChild(xmin)
    ymin = doc.createElement('ymin')                
    ymin.appendChild(doc.createTextNode(str(datas[2])))
    bndbox.appendChild(ymin)                
    xmax = doc.createElement('xmax')                
    xmax.appendChild(doc.createTextNode(str(datas[3])))
    bndbox.appendChild(xmax)                
    ymax = doc.createElement('ymax')    
    if  '\r' == str(datas[4])[-1] or '\n' == str(datas[4])[-1]:
        data = str(datas[4])[0:-1]
    else:
        data = str(datas[4])
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)                
    return obj


def create():
    for ele in os.listdir(labels):
        fidin = open(os.path.join(labels, ele), 'r')
        objIndex = 0
        for data in fidin.readlines():
            data = data.strip('\n')
            datas = data.split(' ')
            if 5 != len(datas):
                continue
            objIndex += 1
            pictureName = ele.replace('.txt', '.JPEG')
            imageFile = os.path.join(imgpath,pictureName)
            img = cv2.imread(imageFile)
            imgSize = img.shape
            if 1 == objIndex:
                xmlName = ele.replace('.txt', '.xml')
                f = open(os.path.join(xmlpath_new,xmlName), "w")
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)
                    
                folder = doc.createElement('folder')
                folder.appendChild(doc.createTextNode(foldername))
                annotation.appendChild(folder)
                    
                filename = doc.createElement('filename')
                filename.appendChild(doc.createTextNode(pictureName))
                annotation.appendChild(filename)
                    
                source = doc.createElement('source')                
                database = doc.createElement('database')
                database.appendChild(doc.createTextNode('My Database'))
                source.appendChild(database)
                source_annotation = doc.createElement('annotation')
                source_annotation.appendChild(doc.createTextNode(foldername))
                source.appendChild(source_annotation)
                image = doc.createElement('image')
                image.appendChild(doc.createTextNode('flickr'))
                source.appendChild(image)
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('NULL'))
                source.appendChild(flickrid)
                annotation.appendChild(source)
                    
                owner = doc.createElement('owner')
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('NULL'))
                owner.appendChild(flickrid)
                name = doc.createElement('name')
                name.appendChild(doc.createTextNode('idaneel'))
                owner.appendChild(name)
                annotation.appendChild(owner)
                    
                size = doc.createElement('size')
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(imgSize[1])))
                size.appendChild(width)
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(imgSize[0])))
                size.appendChild(height)
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(imgSize[2])))
                size.appendChild(depth)
                annotation.appendChild(size)
                    
                segmented = doc.createElement('segmented')
                segmented.appendChild(doc.createTextNode(str(0)))
                annotation.appendChild(segmented)            
                annotation.appendChild(insert_object(doc, datas))
            else:
                annotation.appendChild(insert_object(doc, datas))
        try:
            fidin.close()
            f.write(doc.toprettyxml(indent='    '))
            f.close()
        except:
            pass
            
if __name__ == '__main__':
    create()
