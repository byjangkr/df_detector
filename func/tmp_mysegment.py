#!/usr/bin/env python 

# temporal segment for experience
# for M_1_KGT_02.info
def seg_slice_dsf():
  # disfluencies
  seg1 = slice(400,600,1)
  seg2 = slice(1600,2200,1)
  seg3 = slice(2300,2500,1)
  seg4 = slice(2500,2700,1)
  seg5 = slice(3400,3600,1)
  seg6 = slice(3900,4100,1)
  seg7 = slice(4900,5100,1)
  segall = [seg1,seg2,seg3,seg4,seg5,seg6,seg7]
  return segall

def seg_slice_ref():
  # reference (manual tagging)
  ref1 = slice(351,419,1)
  ref2 = slice(1862,1958,1)
  ref3 = slice(2377,2419,1)
  ref4 = slice(2593,2637,1)
  ref5 = slice(3481,3502,1)
  ref6 = slice(3960,4008,1)
  ref7 = slice(4966,5013,1)
  segall = [ref1,ref2,ref3,ref4,ref5,ref6,ref7]
  return segall

def seg_slice_nor():
  # normal speech
  nseg1 = slice(600,800,1)
  nseg2 = slice(700,900,1)
  nseg3 = slice(1500,1700,1)
  nseg4 = slice(2200,2400,1)
  nseg5 = slice(3000,3200,1)
  nseg6 = slice(3600,3800,1)
  nseg7 = slice(4500,4700,1)
  segall = [nseg1,nseg2,nseg3,nseg4,nseg5,nseg6,nseg7]
  return segall

def segment_generator(data,win_size,win_step):
  offset = 0
  while offset + win_step < len(data):
	yield data[offset:offset+win_size]
	offset += win_step
  if offset < len(data):
	yield data[offset:len(data)]

# Usage :
#	seg_win_size = 200 # frame*10 (ms)
#	seg_win_step = seg_win_size/2 # frame*10 (ms)
#	segments = segment_generator(feat_data,seg_win_size,seg_win_step)
#	for seg_feat in enumerate(segments):
#  	  print len(seg_feat)
