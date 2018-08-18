#!/usr/bin/python
def gausskernel(size, sig):
    # size should be odd
    size = size + (size+1.)%2
    xmin = -(size - 1)/2
    xmax =  (size - 1)/2
    x = np.arange(xmin, xmax + 1.)
    G = np.zeros((size,size),dtype='float')
    sum = 0
    for i in np.arange(size):
        for j in np.arange(size):
            arg = - (x[i]**2. + x[j]**2.)/(2.*(sig**2.))
            G[i,j] = np.exp(arg)
            sum = sum + G[i,j]

    G = G/sum
    return G

def my_histeq(Image):
    HeqImg = Image
    (R,C) = Image.shape
    Freq = np.zeros((256,1),dtype='float')
    for i in np.arange(R):
        for j in np.arange(C):
            Freq[ Image[i,j] ] += 1.
    CDF = np.cumsum(Freq)/(R*C)
    for i in np.arange(R):
        for j in np.arange(C):
            HeqImg[i,j] = int( CDF[ Image[i,j] ]*255. )
    np.place(HeqImg, HeqImg>255, 255)
    np.place(HeqImg, HeqImg<0, 0)

    return HeqImg

def my_histeq2(Image):
    HeqImg = Image
    (R,C) = Image.shape
    # This is the Freq count array, type float because we want CDF to be float.
    Freq = np.zeros((256,1),dtype='float')
    for v in np.arange(256, dtype='int'):
        Freq[v] = np.count_nonzero( np.all([ (Image >= v-0.5), (Image < v+0.5) ], axis=0) )
    # Max CDF values is 1
    CDF = np.cumsum(Freq)/(R*C)
    for v in np.arange(256, dtype='int'):
        np.place(HeqImg, np.all([ (Image >= v-0.5), (Image < v+0.5) ], axis=0), CDF[v]*255.0)
    return HeqImg

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append("/var/www/html/gui/packages")
import numpy as np
import cgi
from skimage import color
from skimage import data
from skimage.io import imsave, imread
import json
import math

# HTML CONTENT BEGINS
I = imread('../images/_target/0.jpg')
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]
Gray = Gray*255.0
Gray = my_histeq2(Gray)
Gray = Gray/255.0
I_hsv[:,:,2] = Gray
imsave('../images/_target/test.jpg', color.hsv2rgb(I_hsv) )
