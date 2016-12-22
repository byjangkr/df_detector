#!/usr/bin/env python

import argparse
from func import dfio

import numpy
from scipy import ndimage
import matplotlib.pyplot as plt

#parser = argparse.ArgumentParser()
#parser.add_argument("dsf_file",help="input dsf file name")
#args=parser.parse_args()
dsf_file = 'dsf/F_1_KSM_03_r4.dsf'

#dfio.plotprorepimg(dsf_file)

rep_margin = 300 # rep_margin*10ms
pro_img, rep_img = dfio.loadprorepimg(dsf_file)

img_size = rep_img.shape
uptrimarginmat = numpy.tril(numpy.ones(rep_img.shape),rep_margin)
msk_rep_img = uptrimarginmat*rep_img

label_im, nb_labels = ndimage.label(msk_rep_img)

plt.figure
plt.imshow(label_im)
plt.show()


