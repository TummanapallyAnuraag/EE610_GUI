#!/usr/bin/python

import time
t = time.time()
import sys
sys.path.append("/var/www/html/gui/packages")
import cgi
from skimage import color
from skimage import data
from skimage.io import imsave, imread
import numpy as np
import json
import math
print ("Content-type:text/html\r\n\r\n")
print(json.dumps({'import_time':  time.time() - t }))
