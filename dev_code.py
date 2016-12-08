#!/usr/bin/env python

# reference
# [1] I. Esmaili, N.J. Dabanloo, M. Vali, "Automatic classification of speech dysfluencies in continuous speech based on similarity measures and morphological image processing tools", Biomedical Signal Processing and Control, 23, 104-114, 2016

import argparse
import sys

import numpy
from scipy.spatial import distance as dist
from python_speech_features import mfcc
#from python_speech_features import logfbank
import matplotlib.pyplot as plt

from func import vadwav
from func import imgoperator as imop

# option parser
parser = argparse.ArgumentParser()
parser.add_argument("wav_file",help="input wave file name")

args=parser.parse_args()

# developing ...

def segment_generator(data,win_size,win_step):
  offset = 0
  while offset + win_step < len(data):
	yield data[offset:offset+win_size]
	offset += win_step
  if offset < len(data):
	yield data[offset:len(data)]

def compute_similarity(x,method='xcorr'):
  # create the square matrix of distance between each frame of self
  # do not fix the min or max of distance
  # but, the range of distance is 0-1 in 'xcorr'
  # low ~ high = near ~ far
  (nframe,nfeat) = x.shape
  print 'no. of frames : %d / no. of features : %d' %(nframe,nfeat)
  print 'compute similarity using %s' % (method)

  simmat = numpy.zeros((nframe,nframe))
  for i in range(nframe):
    for j in range(nframe):
      if method == 'xcorr':
	similarity = dist.correlation(x[i],x[j]) # 1 - cross-correlation coeff (pearson)
      elif method == 'eucl':
	similarity = dist.euclidean(x[i],x[j]) # euclidean distance
      else :
	print 'error!! define the method for measuring similarity : %s' % (method)
	raise

      simmat[i,j] = similarity

  return simmat	

# VAD
(vad_data,vad_index,wav_data,sf) = vadwav.run(args.wav_file)
#vadwav.plotvad(vad_data,vad_index,wav_data) # plot the result of VAD

mfcc_feat = mfcc(vad_data,sf) # frame_win_size = 0.025, frame_win_step = 0.01
#fbank_feat = logfbank(data,16000)

seg_win_size = 200 # frame*10 (ms)
seg_win_step = seg_win_size/2 # frame*10 (ms)

segments = segment_generator(mfcc_feat,seg_win_size,seg_win_step)

## example segment
offset = 500
seg_feat = mfcc_feat[offset:offset+seg_win_size]
##


simmat = compute_similarity(seg_feat,'xcorr')

# normalize data to 0-1 range
# method : x_ = (x - min(x))/(max(x) - min(x))
img = (simmat - numpy.min(simmat))/(numpy.max(simmat) - numpy.min(simmat))


bplot = True
# range reverse 0(less) ~ 1(highly) similarity
img = 1 - img
if bplot :
  img_b = numpy.copy(img)

'''
## recipe for detecting prolongation in [1]
# thresholding image to 0 or 1
thr = 0.85 # threshold for binarization
img = imop.thresholding(img,thr)
if bplot :
  img_c = numpy.copy(img)

# remain digonal connected-component
img = imop.remain_digncomp(img)
if bplot :
  img_d = numpy.copy(img)

# closing operation
clssqr = 5 # the size of square matrix for closing
img = imop.closing(img,clssqr)
if bplot :
  img_e = numpy.copy(img)

# opening operation
opnsqr = 20 # the size of square matrix for opening
img = imop.opening(img,opnsqr)
if bplot :
  img_f = numpy.copy(img)
## end of recipe
'''


## recipe for detecting repetition of syllables and words in [1]
# remove digonal connected-component
thr = 0.85 # threshold for binarization
img_bi = imop.thresholding(img,thr)
img_dig = imop.remain_digncomp(img_bi)
img = img - img_dig
if bplot :
  img_c = numpy.copy(img)

# thresholding image to 0 or 1
img = imop.thresholding(img,thr)
if bplot :
  img_d = numpy.copy(img)

# eliminating small components
img = imop.maxpooling(img,3)

if bplot :
  img_e = numpy.copy(img)



if bplot :
  plt.figure(1)
  plt.subplot(231)
  plt.plot(vad_data)
  plt.subplot(232)
  plt.imshow(img_b, cmap='gray')
  plt.subplot(233)
  plt.imshow(img_c, cmap='gray')
  plt.subplot(234)
  plt.imshow(img_d, cmap='gray')
  plt.subplot(235)
  plt.imshow(img_e, cmap='gray')
  #plt.subplot(236)
  #plt.imshow(img_f, cmap='gray')
  
  plt.show()




#for seg_feat in enumerate(segments):
#  print len(seg_feat)














