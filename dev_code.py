#!/usr/bin/env python

import argparse
import sys

import numpy
from python_speech_features import mfcc
#from python_speech_features import logfbank

from func import vadwav

# option parser
parser = argparse.ArgumentParser()
parser.add_argument("wav_file",help="input wave file name")

args=parser.parse_args()

(vad_data,vad_index,wav_data) = vadwav.run(args.wav_file)

#vadwav.plotvad(vad_data,vad_index,wav_data)

def segment_generator(data,win_size,win_step):
  offset = 0
  while offset + win_step < len(data):
	yield data[offset:offset+win_size]
	offset += win_step
  if offset < len(data):
	yield data[offset:len(data)]


# normalizing
no_data = (vad_data - numpy.mean(vad_data))/numpy.std(vad_data)
no_data = numpy.array(no_data)

mfcc_feat = mfcc(no_data,16000) # frame_win_size = 0.025, frame_win_step = 0.01
#fbank_feat = logfbank(data,16000)

seg_win_size = 20 # frame*10ms
seg_win_step = 10 # frame*10ms

segments = segment_generator(mfcc_feat,seg_win_size,seg_win_step)

#seg_feat = mfcc_feat[0:seg_win_size]
#print len(seg_feat)
#for seg_feat in enumerate(segments):
#  print len(seg_feat)

#for i in range(len(mfcc_feat)):
#  for j in range(len(mfcc_feat)):











