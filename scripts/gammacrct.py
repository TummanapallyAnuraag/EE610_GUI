#!/usr/bin/python

# This will get us the parameter from the GET/POST request from the webpage
def getparam(param, def_val = ''):
    data = cgi.FieldStorage()
    if data.getvalue(param):
        val = data.getvalue(param)
    else:
        val = def_val
    return val

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append("/var/www/html/gui/packages")

import cgi
from skimage import color
from skimage.io import imsave, imread
import numpy as np
import json

# HTML CONTENT BEGINS
print ("Content-type:text/html\r\n\r\n")

# LOGIC

# Get some parameters
foldername      = getparam('foldername','_target')
filename        = getparam('filename','0.jpg')
operation_num   = getparam('opn','1')
format          = getparam('format','jpg')
gamma           = float(getparam('gamma',0.5))
gain            = float(getparam('gain',1))

# Read Image, RGB->HSV, perform operations on 'V' plane
I       = imread('../images/'+foldername+'/'+filename)
if (len(I.shape) == 3):
    RGB = 1
    I_hsv   = color.rgb2hsv(I[:,:,0:3])
    Gray    = I_hsv[:,:,2]
else:
    RGB = 0
    Gray    = I
    # This has already values from 0->255
    Gray.astype(float)
    Gray = Gray/255.0

# Performing all operations here..
Gray = gain*np.power(Gray,gamma)

# Just to be sure..
np.place(Gray, Gray>1, 1)

# Put it back and save the image
if (RGB == 1):
    I_hsv[:,:,2]    = Gray
    I               = color.hsv2rgb(I_hsv)
else:
    I  = Gray

imsave('../images/_target/'+operation_num+'.'+format, I);

# END
print(json.dumps({ 'filename' : 'images/_target/'+operation_num+'.'+format }))
