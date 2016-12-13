


def segment_generator(data,win_size,win_step):
  offset = 0
  while offset + win_step < len(data):
	yield data[offset:offset+win_size]
	offset += win_step
  if offset < len(data):
	yield data[offset:len(data)]

seg_win_size = 200 # frame*10 (ms)
seg_win_step = seg_win_size/2 # frame*10 (ms)


#segments = segment_generator(feat_data,seg_win_size,seg_win_step)


#for seg_feat in enumerate(segments):
#  print len(seg_feat)
