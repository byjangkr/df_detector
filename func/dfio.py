#!/usr/bin/env python
import numpy
import pickle
#import matplotlib.pyplot as plt


def saveprorepimg(out_file,img_pro,img_rep):
  # format(tuple) : [img_pro_size array(pro_data) array(rep_data)] 
  # img_pro_size = output[0]
  # array(pro_data) = output[1]
  # array(rep_data) = output[2]
  print "save prolongation and repetition image ->", out_file
  pro_size = img_pro.shape[0]
  rep_size = img_rep.shape[0]
  if not pro_size == rep_size:
    print "error!! do not equalize the size of image between prolongation and repetition"
    raise

  out_data = []
  inx = numpy.arange(pro_size*pro_size)
  inx = numpy.reshape(inx,(pro_size,pro_size))
  data_pro = inx[img_pro>0]
  data_rep = inx[img_rep>0]

  out_data.append(pro_size)
  out_data.append(data_pro)
  out_data.append(data_rep)

  pck = open(out_file,'wb')
  pickle.dump(out_data,pck)

def loadprorepimg(in_file):
  # format(tuple) : [img_pro_size array(pro_data) array(rep_data)] 
  # img_pro_size = output[0]
  # array(pro_data) = output[1]
  # array(rep_data) = output[2]
  print "load prolongation and reptition image ->", in_file
  pck = open(in_file,'rb')
  load_data = pickle.load(pck)
  img_size = int(load_data[0])
  pro_data = load_data[1]
  rep_data = load_data[2]
  if not (img_size or pro_data or rep_data):
    print "error!!!! the load data wrong : ", in_file
    raise

  pro_img = numpy.zeros((img_size*img_size,1))
  rep_img = numpy.zeros((img_size*img_size,1))
  pro_img[pro_data] = 1
  rep_img[rep_data] = 1
  return numpy.reshape(pro_img,(img_size,img_size)), numpy.reshape(rep_img,(img_size,img_size))  




