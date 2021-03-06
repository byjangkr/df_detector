#!/usr/bin/env python

import argparse
from func import kaldi_io as kalIO
from func import dfcluster
from func import dfio
import time
from func.swalignmod import swalign
from func import tmp_mysegment as myseg



#parser = argparse.ArgumentParser()
#parser.add_argument("prb_file",help="input prb file name")
#parser.add_argument("dsf_file",help="output dsf file name")

#args=parser.parse_args()

#spk_info, data = kalIO.read_feat(args.prb_file)

#if len(spk_info)==1:
#  data = data[0]
#else:
#  print 'Warning!! multi speaker data'

start_time = time.time()

#dsflab = dfcluster.run_cluster(data)
#dfio.savepckdata(args.dsf_file,dsflab)


#seg1 = myseg.seg_slice_dsf(0)
#segdata = data[seg1]

#exstr='000BT0B2B000NTA00NTA0AY0HV3000'
exstr='NTA00NTA00NTA0AY0HV3000'

match = 2
mismatch = -1
scoring = swalign.MyScoringMatrix()
#scoring = swalign.KlScoringMatrix()

#sw = swalign.MyLocalAlignment(scoring,gap_penalty=-0.0025,verbose=True)  # you can also choose gap penalties, etc...
sw = swalign.MyLocalAlignment(scoring,gap_penalty=-0.0025,verbose=True)
alignment = sw.align(exstr,exstr)
alignment.dump()



end_time = time.time() - start_time
print 'processing time of this utterance : %0.2f min' % (end_time/60)

"""
exstr='000BT0B2B000NTA00NTA0AY0HV3000'

match = 2
mismatch = -1
#scoring = swalign.NucleotideScoringMatrix(match, mismatch)
scoring = swalign.NucleotideScoringMatrix()

sw = swalign.LocalAlignment(scoring,gap_penalty=-1,verbose=True)  # you can also choose gap penalties, etc...
alignment = sw.align(exstr,exstr)
alignment.dump()



import argparse
from func import dfio
import pickle

import numpy
from scipy import ndimage

parser = argparse.ArgumentParser()
parser.add_argument("dsf_img_file",help="input dsfimg file name")
parser.add_argument("-m",dest="outmode",action='store',default='outscreen',help="the mode of output : outscreen (default), pckout, txtappend")
parser.add_argument("-o",dest="outfile",action='store',help="the output file name for pckout or txtappend of outmode")
args=parser.parse_args()

rep_margin = 300 # rep_margin*10ms
pro_img, rep_img = dfio.loadprorepimg(args.dsf_img_file,1)
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

if not rep_dur_ary.any() :
  lenRP = 0 # mean length of repetition
  numRP = 0 # number of repetition
  RPR = 0 # repetition rate (not smoothed)
else :
  lenRP = numpy.mean(rep_dur_ary) # mean length of repetition
  numRP = nb_labels # number of repetition
  RPR = numpy.sum(rep_dur_ary)/total_dur # repetition rate (not smoothed)

feat = numpy.array([lenPR, numPR, PRR, lenRP, numRP, RPR]) 

outmode = args.outmode
outfile = args.outfile
if outmode == 'outscreen' :
  for x in feat :
    print '%0.3f' % (x),
elif outmode == 'pckout' :
  if not outfile :
    print "error!!! check outmode or output file name"
    raise
  
  pck = open(outfile,'wb')
  pickle.dump(feat,pck)
  pck.close()

elif outmode == 'txtappend' :
  if not outfile :
    print "error!!! check outmode or output file name"
    raise 

  f = open(outfile,'a')
  f.write('\n')
  f.write('%s ' % (args.dsf_img_file))
  for s in feat :
    f.write('%0.3f' % (s))
  f.close()
"""



