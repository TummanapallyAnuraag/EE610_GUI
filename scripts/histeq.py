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

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append("/var/www/html/gui/packages")

import cgi
from skimage import color
from skimage import data
from skimage import exposure
from skimage.io import imsave, imread
import numpy as np
import json

# HTML CONTENT BEGINS
print ("Content-type:text/html\r\n\r\n")

# LOGIC
foldername = getparam('foldername','_target')
filename = getparam('filename','0.jpg')
operation_num = getparam('opn','1')

format = getparam('format','jpg')

I = imread('../images/'+foldername+'/'+filename)
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]

# Perform all operations here..

Gray = exposure.equalize_hist(Gray)

np.place(Gray, Gray>1, 1)
I_hsv[:,:,2] = Gray
imsave('../images/_target/'+operation_num+'.'+format, color.hsv2rgb(I_hsv));

# END
print(json.dumps({ 'filename' : 'images/_target/'+operation_num+'.'+format }))
