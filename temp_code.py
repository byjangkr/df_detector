#!/usr/bin/env python

import argparse
from func import dfio

import numpy
from scipy import ndimage
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("dsf_file",help="input dsf file name")
args=parser.parse_args()
#dsf_file = 'dsf/F_1_KSM_03_r4.dsf'

rep_margin = 300 # rep_margin*10ms
pro_img, rep_img = dfio.loadprorepimg(args.dsf_file)
img_size = rep_img.shape
total_dur = img_size[0]*0.01

# features related prolongation
pro_label_im, pro_nb_labels = ndimage.label(pro_img)
if pro_nb_labels < 1 :
  pro_dur_ary = 0
else :
  pro_dur_ary = numpy.zeros(pro_nb_labels)
  for lab in numpy.arange(1,pro_nb_labels+1):
    findob = ndimage.find_objects(pro_label_im==lab)[0]
    slice_x, slice_y = ndimage.find_objects(pro_label_im==lab)[0]
    comp_im = pro_label_im[slice_x, slice_y]
    pro_dur = comp_im.shape[0]
    pro_dur_ary[lab-1] = pro_dur*0.01

lenPR = numpy.mean(pro_dur_ary) # mean length of prolongation
numPR = pro_nb_labels # number of prolongation
PRR = numpy.sum(pro_dur_ary)/total_dur # prolongation rate ( not smoothed )

# features related repetition
uptrimarginmat = numpy.tril(numpy.ones(rep_img.shape),rep_margin)
msk_rep_img = uptrimarginmat*rep_img

label_im, nb_labels = ndimage.label(msk_rep_img)
rep_dur_ary = numpy.zeros(nb_labels)
for lab in numpy.arange(1,nb_labels+1):
  findob = ndimage.find_objects(label_im==lab)
  if findob:
    slice_x, slice_y = ndimage.find_objects(label_im==lab)[0]
    comp_im = label_im[slice_x, slice_y]
    # repetition duration
    rep_dur = comp_im.shape[0]
    if comp_im.shape[0] < comp_im.shape[1]:
      rep_dur = comp_im.shape[1]
    rep_dur = rep_dur*0.01
    
    rep_dur_ary[lab-1] = rep_dur

if not rep_dur_ary :
  rep_dur_ary = 0
lenRP = numpy.mean(rep_dur_ary) # mean length of repetition
numRP = nb_labels # number of repetition
RPR = numpy.sum(rep_dur_ary)/total_dur # repetition rate (not smoothed)




