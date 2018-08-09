#!/usr/bin/python

##
# Usage: [BASEURL]/scripts/brightness.py?filename=..&foldername=..&b_add=..&b_minus=..&opn=..
# filename, foldername are optional.. default values are _target and 0.jpg
# b_add and b_minus are between 0 and 1 (both positive)
# b_add means brightness to add (image can have brightness values in 0 to 1)
# b_minus means brightness to subtract
# opn means the operation number, this is used in saving the image after performing the operation
#
# Example:
# http://localhost/scripts/brightness.py?b_add=0.3&opn=2
# Output:
# File: [BASEDIR]/images/_target/.jpg -> brightness increased by 0.3 -> saved as 2.jpg
##
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
from skimage.io import imsave, imread
import numpy as np

# HTML CONTENT BEGINS
print ("Content-type:text/html\r\n\r\n")

# LOGIC
foldername = getparam('foldername','_target')
filename = getparam('filename','0.jpg')
b_add = float(getparam('b_add',0))
b_minus = float(getparam('b_minus',0))
operation_num = getparam('opn',1)

format = getformat(filename)

I = imread('../images/'+foldername+'/'+filename)
I_hsv = color.rgb2hsv(I)
Gray = I_hsv[:,:,2]
# imsave('../images/I_before.png', I);
Gray = Gray + b_add - b_minus;
np.place(Gray, Gray>1, 1)
I_hsv[:,:,2] = Gray
imsave('../images/_target/'+operation_num+'.'+format, color.hsv2rgb(I_hsv));

# END
print('The Job is Done !!')
