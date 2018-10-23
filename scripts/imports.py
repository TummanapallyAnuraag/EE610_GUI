#!/usr/bin/python

import time
t = time.time()
import sys
sys.path.append("/home/anuraag/IITB/Sem3/EE610/gui/packages")
import cgi
import os
from skimage import color
from skimage import data
from skimage.io import imsave, imread
import numpy as np
import json
import math
import cv2
print ("Content-type:text/html\r\n\r\n")
I = imread('../images/_gui/default.jpg')
imsave('../images/_target/0.jpg', I)
print(json.dumps({'import_and_copy_time':  time.time() - t }))
