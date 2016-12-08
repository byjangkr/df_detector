#!/usr/bin/env python
import numpy
from scipy.ndimage import morphology as morp
from scipy.ndimage.filters import maximum_filter as maxpool
from scipy.ndimage import convolve

def thresholding(img,threshold=0.9):
  if numpy.max(img)!=1 or numpy.min(img)!=0:
    print 'warning!!! image can be distorted becuase the range of image is not 0~1'
  
  img_ = numpy.copy(img)
  img_[img>=threshold] = 1
  img_[img<threshold] = 0
  return img_

def remain_digncomp(img):
  img_ = numpy.zeros(img.shape)
  for digpnt in range(img.shape[0]):
    img_[digpnt,digpnt] = 1

    # up direction
    movpnt = digpnt - 1
    while movpnt >= 0 and img[movpnt,digpnt] == 1:
	img_[movpnt,digpnt] = 1
	movpnt -= 1

    # left direction
    movpnt = digpnt - 1
    while movpnt >= 0 and img[digpnt,movpnt] == 1:
	img_[digpnt,movpnt] = 1
	movpnt -= 1

    # down direction
    movpnt = digpnt + 1
    while movpnt < img.shape[0] and img[movpnt,digpnt] == 1:
	img_[movpnt,digpnt] = 1
	movpnt += 1

    # right direction
    movpnt = digpnt + 1
    while movpnt < img.shape[0] and img[digpnt,movpnt] == 1:
	img_[digpnt,movpnt] = 1
	movpnt += 1

  return img_

def closing(img,sqaure_size):
  img_ = morp.binary_closing(img,structure=numpy.ones((sqaure_size,sqaure_size))).astype(int)
  return img_
    
def opening(img,sqaure_size):
  img_ = morp.binary_opening(img,structure=numpy.ones((sqaure_size,sqaure_size))).astype(int)
  return img_

def maxpooling(img,sqaure_size):
  n = sqaure_size
  #mask = numpy.ones((n+2,n+2))
  #mask[1:n+1,1:n+1] = 0
  mask = numpy.zeros((n,n))
  mask[n/2,n/2] = 1
  #img_ = (img == maxpool(img,footprint=mask))
  img_ = convolve(img,mask,mode='constant',cval=0.0)
  img_[img_>0] = 1
  return img_
    
