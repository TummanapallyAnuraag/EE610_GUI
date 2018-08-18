#!/usr/bin/python

# This will get us the parameter from the GET/POST request from the webpage
def getparam(param, def_val = ''):
    data = cgi.FieldStorage()
    if data.getvalue(param):
        val = data.getvalue(param)
    else:
        val = def_val
    return val

# My custom convulution function
# With Zero Padding
def my_conv(Img, filter):
    Ret = Img;
    (R, C) = Img.shape
    (Rf, Cf) = filter.shape

    if ( (Rf %2 ==0) or (Cf %2 ==0) ):
        print('Kernel size should not be even!!')
        return Img

    # Zero Padding. (Rf-1)/2 rows top and bottom
    # Zero Padding. (Cf-1)/2 columns left and right
    Img2 = np.append(np.zeros(((Rf-1)/2,C)), Img, axis=0)
    Img2 = np.append(Img2,np.zeros(((Rf-1)/2,C)), axis=0)
    Img2 = np.append(np.zeros((R+Rf-1,(Cf-1)/2)), Img2,axis=1)
    Img2 = np.append(Img2,np.zeros((R+Rf-1,(Cf-1)/2)),axis=1)

    # Basic Convolution operation
    for i in np.arange( 0 + (Rf-1)/2,    R + (Rf-1)/2 ):
        for j in np.arange(0 + (Cf-1)/2,    C + (Cf-1)/2 ):
            Ret[i-(Rf-1)/2, j-(Cf-1)/2] = np.sum(filter*Img2[i-(Rf-1)/2:i+(Rf-1)/2+1, j-(Cf-1)/2: j+(Cf-1)/2+1])

    return Ret

# Construct a Gaussian kernel for Blurring
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
            #  x and y are same so why waste variables and precious RAM?
            arg = - (x[i]**2. + x[j]**2.)/(2.*(sig**2.))
            G[i,j] = np.exp(arg)
            # Why to compute sum after the for loop, any way it has to loop again,
            # so instead use the same loop...
            sum = sum + G[i,j]

    # So that the sum of new 'G' will be 1
    # We want sum to be 1 becuase: we dont want to brighten / dull the image.
    G = G/sum
    return G

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append("/var/www/html/gui/packages")

import cgi
from skimage import color
from skimage import data
from skimage.io import imsave, imread
import numpy as np
import json
import math

# HTML CONTENT BEGINS
print ("Content-type:text/html\r\n\r\n")

# LOGIC

# Get some parameters
foldername      = getparam('foldername','_target')
filename        = getparam('filename','0.jpg')
operation_num   = getparam('opn','1')
format          = getparam('format','jpg')
sig             = float(getparam('sig',1));

# Read Image, RGB->HSV, perform operations on 'V' plane
I = imread('../images/'+foldername+'/'+filename)
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]

# Perform all operations here..
kernel = gausskernel(2*sig, sig)
Gray = my_conv(Gray, kernel)

# Just to be sure..
np.place(Gray, Gray>1, 1)

# Put it back and save the image
I_hsv[:,:,2] = Gray
imsave('../images/_target/'+operation_num+'.'+format, color.hsv2rgb(I_hsv));

# END
print(json.dumps({ 'filename' : 'images/_target/'+operation_num+'.'+format }))
