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
print(np.max(Gray), np.min(Gray))
