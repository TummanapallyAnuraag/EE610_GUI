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
scale           = float(getparam('scale', 0.25))

# Read Image, RGB->HSV, perform operations on 'V' plane
I = imread('../images/'+foldername+'/'+filename)
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]

# Perform all operations here..

# Kernel construcion
kernel = np.array([
[0, -1, 0],
[-1, 4, -1],
[0, -1, 0]
],dtype='float')

# Convolution
mask = my_conv(Gray, kernel)

# Just to be sure..
np.place(mask, mask>1.0, 1.0)
np.place(mask, mask<0.0, 0.0)

# Adding to the original image
Gray = Gray + scale*mask

# Just to be sure..
np.place(Gray, Gray>1.0, 1.0)
np.place(Gray, Gray<0.0, 0.0)

# Put it back and save the image
I_hsv[:,:,2] = Gray
imsave('../images/_target/'+operation_num+'.'+format, color.hsv2rgb(I_hsv));

# END
print(json.dumps({
    'filename' : 'images/_target/'+operation_num+'.'+format
}))
