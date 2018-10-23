#!/usr/bin/python

# All Kinds of Imports
import sys
# Look for the packages here..
sys.path.append("/home/anuraag/IITB/Sem3/EE610/gui/packages")
import os
import cgi
from skimage import color
from skimage.io import imsave, imread
import numpy as np
import json
import cv2
from skimage.measure import compare_ssim as ssim

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

# Assignment 2 Code:
def get_psnr(img1, img2):
    MAX_PIXEL_VAL = 255.0
    ERR = img1 - img2
    MSE = np.mean( ERR**2 )
    PSNR = 20*math.log10( MAX_PIXEL_VAL/math.sqrt(MSE) )
    return PSNR

def get_ssim(img1, img2):
    return ssim(img1, img2, data_range=np.max(img2) - np.min(img2), multichannel=True)

def deblur_inv():
    global foldername
    global filename
    global format
    global operation_num
    Dict = {}

    _I  = cv2.imread('../images/'+foldername+'/'+filename)
    I   = cv2.cvtColor(_I, cv2.COLOR_BGR2RGB)
    _K   = cv2.imread('../images/_kernel/0.'+kernelformat,0)
    _K   = _K.astype(np.float)
    _K   = _K/np.sum(_K)

    r = I[:,:,0]
    g = I[:,:,1]
    b = I[:,:,2]

    (kr,kc) = _K.shape
    (M,N)   = r.shape

    K = np.zeros([M,N])
    # K[M/2 - kr/2 :M/2 + kr/2, N/2 - kc/2 : N/2 + kc/2 ]  = _K
    K[:kr, :kc] = _K

    RFFT = np.fft.fft2(r)
    GFFT = np.fft.fft2(g)
    BFFT = np.fft.fft2(b)
    KFFT = np.fft.fft2(K)

    # Why fft shift?
    # why take real?
    deblur_r = np.real( np.fft.ifft2(RFFT/KFFT) )
    deblur_g = np.real( np.fft.ifft2(GFFT/KFFT) )
    deblur_b = np.real( np.fft.ifft2(BFFT/KFFT) )

    deblur = np.zeros([M,N,3])
    deblur[:,:,0] = deblur_b
    deblur[:,:,1] = deblur_g
    deblur[:,:,2] = deblur_r
    # plt.imshow(20*np.log(np.abs(RFFT)), cmap='gray')
    # plt.show()
    # deblur = np.roll(deblur, kr/2, axis=0)
    # deblur = np.roll(deblur, kc/2, axis=1)
    cv2.imwrite('../images/'+foldername+'/'+operation_num+'.'+format, deblur)
    return Dict

def deblur_trunc():
    global foldername
    global filename
    global format
    global operation_num
    radius = float(getparam('radius', 150))
    Dict = {}
    # _gt = cv2.imread('../images/'+foldername+'/'+filename)
    # gt = cv2.cvtColor(_gt, cv2.COLOR_BGR2RGB)
    _I  = cv2.imread('../images/'+foldername+'/'+filename)
    I   = cv2.cvtColor(_I, cv2.COLOR_BGR2RGB)
    _K   = cv2.imread('../images/_kernel/0.'+kernelformat,0)
    _K   = _K.astype(np.float)
    _K   = _K/np.sum(_K)

    r = I[:,:,0]
    g = I[:,:,1]
    b = I[:,:,2]

    (kr,kc) = _K.shape
    (M,N)   = r.shape

    K           = np.zeros([M,N])
    # K[M/2 - kr/2 :M/2 + kr/2, N/2 - kc/2 : N/2 + kc/2 ]  = _K
    K[:kr,:kc] = _K

    exists = os.path.isfile('../images/_trash/TRUNC_'+str(M)+'_'+str(N)+'_'+str(radius)+'.png')
    if(exists):
        print('\tLeveraging existing TRUNC')
        TRUNC = cv2.imread('../images/_trash/TRUNC_'+str(M)+'_'+str(N)+'_'+str(radius)+'.png', 0)
        TRUNC = TRUNC.astype(np.float)
    else:
        TRUNC = np.zeros([M,N])
        TRUNC = TRUNC.astype(np.float)
        for row in np.arange(0,M):
            for col in np.arange(0,N):
                # print(radius,row)
                # exit()
                if( (row-radius)*(row-(M-radius)) < 0 ):
                    continue

                if( (col-radius)*(col-(N-radius)) < 0 ):
                    continue

                d1 = np.linalg.norm( np.array([row, col]) )
                d2 = np.linalg.norm( np.array([row-M, col]) )
                d3 = np.linalg.norm( np.array([row, col-N]) )
                d4 = np.linalg.norm( np.array([row-M, col-N]) )
                d = np.min([d1,d2,d3,d4])
                if(d < radius):
                    # TRUNC[row,col] = 1.0/(1.0 + (d/radius)**(2*10) )
                    TRUNC[row,col] = 1.0

        cv2.imwrite('../data/trunc/TRUNC_'+str(M)+'_'+str(N)+'_'+str(radius)+'.png', TRUNC)

    RFFT = np.fft.fft2(r)
    GFFT = np.fft.fft2(g)
    BFFT = np.fft.fft2(b)
    KFFT = np.fft.fft2(K)

    # Why fft shift?
    # why take real?

    deblur_r = np.real( np.fft.ifft2(RFFT*TRUNC/KFFT) )
    deblur_g = np.real( np.fft.ifft2(GFFT*TRUNC/KFFT) )
    deblur_b = np.real( np.fft.ifft2(BFFT*TRUNC/KFFT) )

    deblur = np.zeros([M,N,3])
    deblur[:,:,0] = deblur_b
    deblur[:,:,1] = deblur_g
    deblur[:,:,2] = deblur_r
    # plt.imshow(TRUNC)
    # plt.show()
    # exit()
    cv2.imwrite('../images/'+foldername+'/'+operation_num+'.'+format, deblur)
    return Dict

def deblur_weiner():
    global foldername
    global filename
    global format
    global operation_num

    Dict = {}
    _I = cv2.imread('../images/'+foldername+'/'+filename)
    I = cv2.cvtColor(_I, cv2.COLOR_BGR2RGB)

    _kernel =  cv2.imread('../images/_kernel/0.'+kernelformat,0)
    _kernel = _kernel.astype(np.float)
    _kernel = _kernel/np.sum(_kernel)

    K_weiner = float(getparam('k',0))
    (M, N) = I[:,:,0].shape
    (kr, kc) = _kernel.shape

    K = np.zeros([M,N])
    # K[ M/2 - kr/2 : M/2 + kr/2, N/2 - kc/2 : N/2 + kc/2 ] = _kernel
    K[:kr,:kc] = _kernel

    r = I[:,:,0]
    g = I[:,:,1]
    b = I[:,:,2]

    RFFT = np.fft.fft2(r)
    GFFT = np.fft.fft2(g)
    BFFT = np.fft.fft2(b)
    KFFT = np.fft.fft2(K)

    # Why fft shift?
    # why take real?
    deblur_r = np.real( np.fft.ifft2(RFFT*np.abs(KFFT)**2/(KFFT*(K_weiner + np.abs(KFFT)**2 ) ) ) )
    deblur_g = np.real( np.fft.ifft2(GFFT*np.abs(KFFT)**2/(KFFT*(K_weiner + np.abs(KFFT)**2 ) ) ) )
    deblur_b = np.real( np.fft.ifft2(BFFT*np.abs(KFFT)**2/(KFFT*(K_weiner + np.abs(KFFT)**2 ) ) ) )

    deblur = np.zeros([M,N,3])
    deblur[:,:,0] = deblur_b
    deblur[:,:,1] = deblur_g
    deblur[:,:,2] = deblur_r
    # plt.imshow(deblur_r, cmap='gray')
    # plt.show()
    cv2.imwrite('../images/'+foldername+'/'+operation_num+'.'+format, deblur)
    return Dict

def deblur_cls():
    global foldername
    global filename
    global format
    global operation_num

    Dict = {}
    gamma = float(getparam('cls_gamma',0))

    _I = cv2.imread('../images/'+foldername+'/'+filename)
    I = cv2.cvtColor(_I, cv2.COLOR_BGR2RGB)

    _kernel =  cv2.imread('../images/_kernel/0.'+kernelformat,0)
    _kernel = _kernel.astype(np.float)
    _kernel = _kernel/np.sum(_kernel)

    (M, N) = I[:,:,0].shape
    (kr, kc) = _kernel.shape

    K = np.zeros([M,N])
    # no problem only for even kr
    K[ M/2 - kr/2 : M/2 + kr/2, N/2 - kc/2 : N/2 + kc/2 ] = _kernel

    P = np.zeros([M,N])
    P[M/2 -1: M/2 + 2 , N/2 - 1 : N/2 + 2] = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]
    ])

    r = I[:,:,0]
    g = I[:,:,1]
    b = I[:,:,2]

    RFFT = np.fft.fftshift(np.fft.fft2(r))
    GFFT = np.fft.fftshift(np.fft.fft2(g))
    BFFT = np.fft.fftshift(np.fft.fft2(b))
    KFFT = np.fft.fftshift(np.fft.fft2(K))
    PFFT = np.fft.fftshift(np.fft.fft2(P))

    # Why fft shift?
    # why take real?
    deblur_r = np.real( np.fft.ifftshift( np.fft.ifft2(RFFT*np.conj(KFFT)/( gamma*np.abs(PFFT)**2 + np.abs(KFFT)**2 ) ) ) )
    deblur_g = np.real( np.fft.ifftshift( np.fft.ifft2(GFFT*np.conj(KFFT)/( gamma*np.abs(PFFT)**2 + np.abs(KFFT)**2 ) ) ) )
    deblur_b = np.real( np.fft.ifftshift( np.fft.ifft2(BFFT*np.conj(KFFT)/( gamma*np.abs(PFFT)**2 + np.abs(KFFT)**2 ) ) ) )

    deblur = np.zeros([M,N,3])
    deblur[:,:,0] = deblur_b
    deblur[:,:,1] = deblur_g
    deblur[:,:,2] = deblur_r
    # plt.imshow(P, cmap='gray')
    # plt.show()
    cv2.imwrite('../images/'+foldername+'/'+operation_num+'.'+format, deblur)
    return Dict


def blur_image():
    Dict = {}
    sigma = float(getparam('sigma', 0.0))
    # print(sigma)
    # sigma = 10.0
    _I = cv2.imread('../images/'+foldername+'/'+filename)
    (b,g,r) = cv2.split(_I)
    _K   = cv2.imread('../images/_kernel/0.'+kernelformat,0)
    _K   = _K.astype(np.float)
    _K   = _K/np.sum(_K)

    (kr,kc) = _K.shape
    (M,N)   = r.shape

    K = np.zeros([M,N])
    K[:kr,:kc] = _K

    RFFT = np.fft.fft2(r)
    GFFT = np.fft.fft2(g)
    BFFT = np.fft.fft2(b)
    KFFT = np.fft.fft2(K)

    blur_r = np.real( np.fft.ifft2(RFFT*KFFT) )
    blur_g = np.real( np.fft.ifft2(GFFT*KFFT) )
    blur_b = np.real( np.fft.ifft2(BFFT*KFFT) )

    blur = np.zeros([M,N,3])
    if(sigma > 0):
        blur[:,:,0] = blur_b + np.random.normal(0, sigma, (M,N))
        blur[:,:,1] = blur_g + np.random.normal(0, sigma, (M,N))
        blur[:,:,2] = blur_r + np.random.normal(0, sigma, (M,N))
    else:
        blur[:,:,0] = blur_b
        blur[:,:,1] = blur_g
        blur[:,:,2] = blur_r
    # plt.imshow(blur, cmap='gray')
    # plt.show()
    cv2.imwrite('../images/'+foldername+'/'+operation_num+'.'+format, blur)
    return Dict


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
    'medianfilt':  medianfilt,
}

deblurDictionary = {
    'deblur_inv'    : deblur_inv,
    'deblur_trunc'  : deblur_trunc,
    'deblur_weiner' : deblur_weiner,
    'blur_image'    : blur_image
}

# Get some parameters
foldername      = getparam('foldername','_target')
filename        = getparam('filename','0.jpg')
operation_num   = getparam('opn','1')
format          = getparam('format','jpg')
RGB             = 1
operation_name  = getparam('opname', 'histeq')
kernelformat    = getparam('kernelformat', 'jpg')

# LOGIC
if operation_name in OpnDictionary:
    (G, HSV) = getInputImage()
    (G, Dict) = OpnDictionary[operation_name](G, HSV)
    saveOutputImage(G, HSV)
else:
    (Dict) = deblurDictionary[operation_name]()

# Return Message
Dict['filename'] = 'images/_target/' + operation_num + '.' + format
print(json.dumps(Dict))
