#!/usr/bin/env python
# difluency detector using clustering
import numpy
import matplotlib.pyplot as plt
from func import imgoperator as imop
import time

#from func import tmp_mysegment as myseg # for my experience

def kldivergence(pdf1,pdf2):
# compute Kullback and Leibler divergence (symmetrised)
# kl_val = ( D(P||Q) + D(Q||P) ) / 2

  if not len(pdf1) == len(pdf2):
    raise IOError("error!!! do not match the sizes of input - %d = %d \n" % (len(pdf1), len(pdf2)))

  Dpq = 0
  Dqp = 0
  for i in range(len(pdf1)):
    Dpq = Dpq + float(pdf1[i])*numpy.log2(float(pdf1[i])/float(pdf2[i]))
    Dqp = Dqp + float(pdf2[i])*numpy.log2(float(pdf2[i])/float(pdf1[i]))
    
  out_val = (Dpq + Dqp)/2
  return out_val

def makesilmodel(lenpdf,peakprob,peakinx):
# make pdf model of silence
# data type : float list [0.1 0.2 0.3 ...]

  val = (1-peakprob)/(lenpdf-1)
  mdl = [float(val) for _ in range(lenpdf-1)]
  out_mdl = mdl[0:peakinx]
  out_mdl.append(float(peakprob))
  for x in mdl[peakinx:]:
    out_mdl.append(x)

  return out_mdl

def segment_generator(datalen,win_size,win_step):
  offset = 0
  while offset + win_size < datalen:
	yield slice(offset,offset+win_size,1)
	offset += win_step
  if offset < datalen:
	yield slice(offset,datalen,1)

def multisenonedist(tarpdf,multipdf):
  ### numpy.min
  out_dist = 9999999999
  out_i = 0
  for i in range(len(multipdf)):
    dist = kldivergence(tarpdf,multipdf[i])
    if dist < out_dist:
      out_dist = dist
      out_i = i
  return out_dist, out_i

def mdlupdate(tarmdl,inpdf,w):
  outmdl = []
  for i in range(len(tarmdl)):
    val = float(tarmdl[i])*w + float(inpdf[i])*(1-w)
    outmdl.append(val)
  return outmdl

def adaptsilmodel(indata,silmdl):
  adt_boundary = 3 
  adt_w = 0.9
  adaptmdl = silmdl
  
  for inx in range(len(indata)):
    idist = 0; imdl = 0
    tarpdf = []
    tarpdf = indata[inx]
    idist, imdl = multisenonedist(tarpdf,adaptmdl)
    if idist < adt_boundary:
      adaptmdl[imdl] = mdlupdate(adaptmdl[imdl],tarpdf,adt_w) 

  #return adaptmdl 

def clustering(indata,inlab,silmdl,cls_boundary,w_update):
  clsmdl = silmdl[:] # initial model
  clslab = [-1 for _ in range(len(silmdl))] # initial index of model
  datalab = inlab[:] # initial label
  silinx = range(len(silmdl))
  newlab = numpy.max(inlab) + 1
  
  for inx in range(len(indata)):
    #tarpdf = indata[inx]
    idist = 0; imdl = 0
    idist, imdl = multisenonedist(indata[inx],clsmdl)
    if idist < cls_boundary:
      # update datalab if datalab is empty (initial 0)
      if datalab[inx] == 0:
        datalab[inx] = clslab[imdl]

      # update model if i_model is not silence model (fix silmdl)
      if not clslab[imdl] == -1:
        clsmdl[imdl] = mdlupdate(clsmdl[imdl],indata[inx],w_update)

    else:
      clsmdl.append(indata[inx])
      if datalab[inx] == 0:
        clslab.append(newlab)
        datalab[inx] = newlab
        newlab += 1
      else:
        clslab.append(datalab[inx])

          
  return datalab

def detectdf(inlab,df_min_state,df_min_frame):
  dfregion = [0 for _ in range(len(inlab))]
  
  deltaprob = float(1/float(len(inlab)))
  epsilon = float(deltaprob*deltaprob)
  dfprob = [epsilon for _ in range(len(inlab))]  
  grad = -1
  preprob = dfprob[0]

  maxinx = numpy.max(inlab)
  #print 'max index of label : %d\n' %(maxinx)
  # 2D array (0=silence)
  tranmat = numpy.zeros((maxinx+1,maxinx+1))
  
  for i in range(maxinx): 
    tranmat[i,i] = 1 # self-loop
    tranmat[0,i] = 1 # sil-path
    tranmat[i,0] = 1

  if inlab[0] == -1:
    prevlab = 0
    nextlab = 0
  else :
    prevlab = inlab[0]
    nextlab = inlab[0]

  regbuf = []
  statbuf = []
  
  for i in range(len(inlab)):
    ilab = inlab[i]
    if ilab == -1: # silence
      dfregion[i] = -1
      ilab = prevlab
    else:
      nextlab = ilab
      path = tranmat[prevlab,nextlab]
      if path == 1: # rep path
        regbuf.append(i)
        if not statbuf[-1:] == ilab:
          statbuf.append(ilab)
        if not prevlab == 0 and not prevlab == nextlab:
          grad = 1 # gradient
          
      else: # new path
        if len(statbuf) >= df_min_state and len(regbuf) >= df_min_frame:
          for dfreg in regbuf: 
            dfregion[dfreg] = 1
        regbuf = []
        regbuf.append(i)
        statbuf = []
        statbuf.append(ilab)
        tranmat[prevlab,nextlab] = 1
        grad = -1 # gradient
   
    prevlab = ilab
    dfprob[i] = float(preprob + (grad)*deltaprob)
    if dfprob[i] < epsilon:
      dfprob[i] = epsilon
    preprob = dfprob[i]

  """
  plt.subplot(211)
  plt.plot(dfregion)

  plt.subplot(212)
  plt.plot(dfprob)
    
  plt.show()
  """    

  return dfregion,dfprob

def merge_dsflab(dsflab1,dsflab2,offset):
  out_dsflab = dsflab1[:]
  for i in range(len(out_dsflab)):
    if dsflab1[i]==-1 or dsflab2[i]==-1:
      out_dsflab[i] = -1
    if dsflab1[i]==1 or dsflab2[i]==1:
      out_dsflab[i] = 1
    out_dsflab[i] += offset
  return out_dsflab

def merge_dsfprob(dsfprob1,dsfprob2):
  for i in range(len(dsfprob1)):
    dsfprob1[i] += dsfprob2[i]
  return dsfprob1

def run_cluster(data):

  # hyper parameter
  winsize = 400 # winsize * 10ms
  winshift = 100
  w_update = 0.8 # cluster update weight
  cls_boundary = 5
  # silpdf = [0,39,40] # timit
  silpdf = [0,39,40] # etri_nonnative_adv
  peak_silmdl = 0.7
  adaptsil = True

  df_min_state = 5
  df_min_frame = 10

  clslab = [ 0 for _ in range(len(data))]
  #f_dsflab = [ 0 for _ in range(len(data))] # forward clustering
  #b_dsflab = [ 0 for _ in range(len(data))] # backward clustering
  dsflab = [ 0 for _ in range(len(data))]
  dsfprob = [ 0 for _ in range(len(data))]

  
  ## make reference using manual tagging ######################
  #reflab = [ 0 for _ in range(len(data))]
  #for ref_slice in myseg.seg_slice_ref():
  #  seg_ref = [ 1 for _ in range(len(reflab[ref_slice]))]
  #  reflab[ref_slice] = seg_ref 
  ##############################################################
  
  # make silence model (index: 0~2)
  silmdl = []
  for i in silpdf:
    silmdl.append(makesilmodel(len(data[0]),peak_silmdl,i))
  
  if adaptsil:
    #print "adaptive silence model...",
    #ad_time = time.time() 
    #silmdl = adaptsilmodel(data,silmdl)
    adaptsilmodel(data,silmdl)
    #print "%0.2f sec" %(time.time()-ad_time)

 
  segments = segment_generator(len(data),winsize,winshift) 
  tcost = time.time()
  for inx, seg_slice in enumerate(segments):
    f_dsflab = [];   d_dsflab = [];    tmp_dsflab = [];    merged_dsflab = []
    seg_time = time.time()
    clslab[seg_slice] = clustering(data[seg_slice],clslab[seg_slice],silmdl,cls_boundary,w_update)

    #clslab[seg_slice] = seg_clslab
    f_dsflab, tmpf_dfprob = detectdf(clslab[seg_slice],df_min_state,df_min_frame) # forward search
    tmp_dsflab,tmp_dfprob = detectdf(clslab[seg_slice][::-1],df_min_state,df_min_frame) # backward search
    b_dsflab = tmp_dsflab[::-1]
    b_dfprob = tmp_dfprob[::-1]
    
    offset = 0 #numpy.max(seg_clslab)/2
    merged_dsflab = merge_dsflab(f_dsflab,b_dsflab,offset) # merge dsf
    dsflab[seg_slice] = merge_dsflab(dsflab[seg_slice],merged_dsflab,offset) # merge dsf
    #dsfprob[seg_slice] = merge_dsfprob(dsfprob[seg_slice],b_dfprob) # merge dsf prob

  print "time cost : %0.2f min" % ((time.time()-tcost)/60) 

   
  return dsflab
  
 

