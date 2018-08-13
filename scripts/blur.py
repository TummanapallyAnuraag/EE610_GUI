#!/usr/bin/python

def getparam(param, def_val = ''):
    data = cgi.FieldStorage()
    if data.getvalue(param):
        val = data.getvalue(param)
    else:
        val = def_val
    return val

def getformat(filename, def_val = 'png'):
    str_list = filename.split('.')
    format = str_list[-1]
    if format:
        val = format
    else:
        val = def_val
    return val

def my_conv(Img, filter):
    #With Zero Padding
    Ret = Img;
    (R, C) = Img.shape
    (Rf, Cf) = filter.shape
    if ( (Rf %2 ==0) or (Cf %2 ==0) ):
        print('Kernel size should not be even!!')
        return Img
    Img2 = np.append(np.zeros(((Rf-1)/2,C)), Img, axis=0)
    Img2 = np.append(Img2,np.zeros(((Rf-1)/2,C)), axis=0)
    Img2 = np.append(np.zeros((R+Rf-1,(Cf-1)/2)), Img2,axis=1)
    Img2 = np.append(Img2,np.zeros((R+Rf-1,(Cf-1)/2)),axis=1)

    for i in np.arange((Rf-1)/2,R+(Rf-1)/2):
        for j in np.arange((Cf-1)/2,C+(Cf-1)/2):
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
foldername = getparam('foldername','_target')
filename = getparam('filename','0.jpg')
operation_num = getparam('opn','1')
format = getparam('format','jpg')
size = float(getparam('size',1));

I = imread('../images/'+foldername+'/'+filename)
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]

# Perform all operations here..
# Gray = Gray*255;

# Construct kernel
if(size % 2 == 0):
    size = size + 1

kernel = np.ones((size,size),dtype='float')
kernel = kernel/np.sum(kernel)
Gray = my_conv(Gray, kernel)
# Gray = Gray/255;

np.place(Gray, Gray>1, 1)
I_hsv[:,:,2] = Gray
imsave('../images/_target/'+operation_num+'.'+format, color.hsv2rgb(I_hsv));

# END
print(json.dumps({ 'filename' : 'images/_target/'+operation_num+'.'+format }))
