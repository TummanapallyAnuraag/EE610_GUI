#!/usr/bin/python

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append(os.getcwd() + "/packages")

import cgi
from skimage import color
from skimage.io import imsave, imread
import numpy as np
import json

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

# My custom Histogram equalisation
# Input: Gray Image 0->255 uint8
# Output: Gray Image: 0->255
def my_histeq(Image):
    # convert return image to type float.
    HeqImg = Image.astype(np.float)
    (R,C) = Image.shape
    FlatImage = Image.ravel()
    Freq = np.bincount(FlatImage, minlength=256)
    CDF = np.cumsum(Freq).astype(np.float)/(float(R)*float(C))
    for v in np.arange(256, dtype='int'):
        indices = (Image == v)
        HeqImg[indices] = CDF[v]*255.0

    HeqImg = HeqImg.astype(np.uint8)
    return HeqImg

def my_medianfiler(Img, size):
    Ret = Img;
    (R, C) = Img.shape
    size = size + (size+1)%2
    (Rf, Cf) = (size, size)

    if ( (Rf %2 ==0) or (Cf %2 ==0) ):
        print('Window size should not be even!!')
        return Img

    # Zero Padding. (Rf-1)/2 rows top and bottom
    # Zero Padding. (Cf-1)/2 columns left and right
    Img2 = np.append(np.zeros(((Rf-1)/2,C)), Img, axis=0)
    Img2 = np.append(Img2,np.zeros(((Rf-1)/2,C)), axis=0)
    Img2 = np.append(np.zeros((R+Rf-1,(Cf-1)/2)), Img2,axis=1)
    Img2 = np.append(Img2,np.zeros((R+Rf-1,(Cf-1)/2)),axis=1)

    # Basic Median operation
    for i in np.arange( 0 + (Rf-1)/2,    R + (Rf-1)/2 ):
        for j in np.arange(0 + (Cf-1)/2,    C + (Cf-1)/2 ):
            Ret[i-(Rf-1)/2, j-(Cf-1)/2] = np.median(Img2[i-(Rf-1)/2:i+(Rf-1)/2+1, j-(Cf-1)/2: j+(Cf-1)/2+1])

    return Ret

# Output: Gray Image 0->255 uint8
def getInputImage():
    global foldername
    global filename
    global operation_num
    global format
    global RGB

    # Read Image, RGB->HSV, perform operations on 'V' plane
    I       = imread('../images/'+foldername+'/'+filename)
    if (len(I.shape) == 3):
        RGB     = 1
        HSV     = color.rgb2hsv(I[:,:,0:3])
        Gray    = HSV[:,:,2]
        Gray    = Gray*255.0
    else:
        RGB     = 0
        Gray    = I
        HSV     = 0
        # This has already values from 0->255
    Gray = Gray.astype(np.uint8)
    return (Gray,HSV)

# Input: Gray Image: 0->1
def saveOutputImage(Gray, HSV):
    global foldername
    global filename
    global operation_num
    global format
    global RGB

    Gray = Gray.astype(np.float)
    Gray = Gray/255.0
    # Just to be sure..
    np.place(Gray, Gray>1, 1)
    np.place(Gray, Gray<0, 0)

    # Put it back and save the image
    if (RGB == 1):
        HSV[:,:,2]  = Gray
        I           = color.hsv2rgb(HSV)
    else:
        I = Gray

    imsave('../images/_target/'+operation_num+'.'+format, I);

def histeq(G, HSV):
    G = my_histeq(G)
    Dict = {}
    return (G, Dict)

def logtx(G, HSV):
    c = float(getparam('c',105))
    G = G.astype(np.float)
    G = c*np.log10(G + 1)
    Dict = {}
    return (G, Dict)

def gammacrct(G, HSV):
    gamma   = float(getparam('gamma',0.5))
    gain    = float(getparam('gain',1))
    G       = G.astype(np.float)
    G       = gain*np.power(G,gamma)
    Dict = {}
    return (G, Dict)

def blur(G, HSV):
    sig     = float(getparam('sig',1))
    kernel  = gausskernel(2*sig, sig)
    G       = G.astype(np.float)
    G       = my_conv(G, kernel)
    Dict = {}
    return (G, Dict)

def sharp(G, HSV):
    # Kernel construcion
    # I = I*impulse3 + I*kernelxscale
    # I = I*(impulse3 + scalexkernel)
    # Therefore..
    scale  = float(getparam('scale', 0.25))
    kernel = np.array([
            [-1*scale, -1*scale, -1*scale],
            [-1*scale, 1+8*scale, -1*scale],
            [-1*scale, -1*scale, -1*scale]
            ],dtype='float')

    # Convolution
    G = G.astype(np.float)
    G = my_conv(G, kernel)
    Dict = {}
    return (G, Dict)

def spnoise(G, HSV):
    scale           = float(getparam('scale',0.1))
    (R, C)          = G.shape
    spnoise         = np.random.choice([0, 255, -255], (R, C), p=[1-scale, scale/2, scale/2])
    salt_percent    = 100*np.average((spnoise == 255))
    pepper_percent  = 100*np.average((spnoise == -255))

    G = G.astype(np.float)
    G = G + spnoise
    Dict = {
    'salt_percent'      : salt_percent,
    'pepper_percent'    : pepper_percent
    }
    return (G, Dict)

def medianfilt(G, HSV):
    size = float(getparam('size',3))
    G = my_medianfiler(G, size)
    Dict = {}
    return (G, Dict)

# HTML CONTENT BEGINS
print ("Content-type:text/html\r\n\r\n")

# List of Operations
OpnDictionary = {
    'histeq'    :  histeq,
    'logtx'     :  logtx,
    'gammacrct' :  gammacrct,
    'blur'      :  blur,
    'sharp'     :  sharp,
    'spnoise'   :  spnoise,
    'medianfilt':  medianfilt
}

# Get some parameters
foldername      = getparam('foldername','_target')
filename        = getparam('filename','0.jpg')
operation_num   = getparam('opn','1')
format          = getparam('format','jpg')
RGB             = 1
operation_name  = getparam('opname', 'histeq')

# LOGIC
(G, HSV) = getInputImage()
(G, Dict) = OpnDictionary[operation_name](G, HSV)
saveOutputImage(G, HSV)

# Return Message
Dict['filename'] = 'images/_target/' + operation_num + '.' + format
print(json.dumps(Dict))
