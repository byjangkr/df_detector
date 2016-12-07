#!/usr/bin/env python

import argparse
import sys

import numpy
from scipy.spatial import distance as dist
from python_speech_features import mfcc
#from python_speech_features import logfbank
import matplotlib.pyplot as plt

from func import vadwav

# option parser
parser = argparse.ArgumentParser()
parser.add_argument("wav_file",help="input wave file name")

args=parser.parse_args()

# VAD
(vad_data,vad_index,wav_data) = vadwav.run(args.wav_file)
#vadwav.plotvad(vad_data,vad_index,wav_data)

# developing ...

def segment_generator(data,win_size,win_step):
  offset = 0
  while offset + win_step < len(data):
	yield data[offset:offset+win_size]
	offset += win_step
  if offset < len(data):
	yield data[offset:len(data)]

def compute_similarity(x,method='xcorr'):
  (nframe,nfeat) = x.shape
  print 'no. of frames : %d / no. of features : %d' %(nframe,nfeat)
  print 'compute similarity ...'

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

def image_thresholding(img,threshold=0.9):
  if numpy.max(img)!=1 or numpy.min(img)!=0:
    print 'warning!!! image can be distorted becuase the range of image is not 0~1'
  
  img_ = img
  img_[img>=thr] = 1
  img_[img<thr] = 0
  return img_

# normalize zero mean and unit variance
no_data = (vad_data - numpy.mean(vad_data))/numpy.std(vad_data)
no_data = numpy.array(no_data)

mfcc_feat = mfcc(no_data,16000) # frame_win_size = 0.025, frame_win_step = 0.01
#fbank_feat = logfbank(data,16000)

seg_win_size = 200 # frame*10 (ms)
seg_win_step = seg_win_size/2 # frame*10 (ms)

segments = segment_generator(mfcc_feat,seg_win_size,seg_win_step)

seg_feat = mfcc_feat[300:300+seg_win_size]

data1 = seg_feat[0]
data2 = seg_feat[1]

simmat = compute_similarity(seg_feat,'eucl')

# normalize data to 0-1 range
# x_ = (x - min(x))/(max(x) - min(x))
img = (simmat - numpy.min(simmat))/(numpy.max(simmat) - numpy.min(simmat))

# range reverse 0(less) ~ 1(highly) similarity
img = 1 - img

# thresholding image to 0 or 1
thr = 0.8 # for prolongation
img = image_thresholding(img,thr)

plt.imshow(img, cmap='gray')
plt.show()



#print len(seg_feat)
#for seg_feat in enumerate(segments):
#  print len(seg_feat)

#for i in range(len(seg_feat)):
#  for j in range(len(seg_feat)):












