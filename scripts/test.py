def my_conv(Img, filter):
    Ret = Img;
    (R, C) = Img.shape
    (Rf, Cf) = filter.shape
    if ( (Rf %2 ==0) or (Cf %2 ==0) ):
        return Img
    Img2 = np.append(np.zeros(((Rf-1)/2,C)), Img, axis=0)
    Img2 = np.append(Img2,np.zeros(((Rf-1)/2,C)), axis=0)
    Img2 = np.append(np.zeros((R+Rf-1,(Cf-1)/2)), Img2,axis=1)
    Img2 = np.append(Img2,np.zeros((R+Rf-1,(Cf-1)/2)),axis=1)

    for i in np.arange((Rf-1)/2,R+(Rf-1)/2):
        for j in np.arange((Cf-1)/2,C+(Cf-1)/2):
            Ret[i-(Rf-1)/2, j-(Cf-1)/2] = np.sum(filter*Img2[i-(Rf-1)/2:i+(Rf-1)/2+1, j-(Cf-1)/2: j+(Cf-1)/2+1])

    return Ret

import numpy as np

A = np.array([
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1]
])
H = np.array([
[0,0,0],
[0,0,0],
[0,0,1],
])
print(my_conv(A, H))
