import cv2
import numpy as np
import random


def sp_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


def padding(image):
    height, width = image.shape
    pad = 3

    P1 = height+2*pad
    P2 = width+2*pad

    padded_image = np.zeros((P1, P2))
    padded_image[pad:-pad,pad:-pad] = image

    return padded_image


def adaptiveMedianFilter(image):
   
    h, w = image.shape
    s = 3
    sMax = 21
    a = sMax//2

    padded_image = padding(image)
    print(padded_image.shape)
    final_image = np.zeros(padded_image.shape)
    
    for i in range(a,h-1):
        for j in range(a,w-1):
        
            final_image[i,j] = stageA(padded_image, i,j,s, sMax)
    
    return final_image[a:-a,a:-a] 


def stageA(mat,x,y,s,sMax):

    window = mat[x-(s//2):x+(s//2)+1,y-(s//2):y+(s//2)+1]

    try:
        Zmin = np.min(window)
    except ValueError:  
        Zmin = 0
    Zmed = np.median(window)
    Zmax = np.max(window)

    A1 = Zmed - Zmin
    A2 = Zmed - Zmax

    if(A1 > 0 and A2 < 0):
        return stageB(window)
    else:
        s +=2
        if (s <= sMax):
            return stageA(mat,x,y,s,sMax)
        else:
            return Zmed
def stageB(window):
    h,w = window.shape
    Zmin = np.min(window)
    Zmed = np.median(window) 
    Zmax = np.max(window)

    Zxy = window[h//2,w//2]
    B1 = Zxy - Zmin
    B2 = Zxy - Zmax

    if (B1 > 0 and B2 < 0):
        return Zxy
    else:
        return Zmed

def main():

    image1 = cv2.imread('D:\gg.jpg')
    #print(image1.shape)
    [mr,mc,md]=image1.shape
    if md>1:
      gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    else:
      gray = image1
    image = sp_noise(gray,0.2)
    print(image.shape)
    
    cv2.imshow('Original Image', image1)
    cv2.waitKey(0)

    cv2.imshow('after adding noise', image)
    cv2.waitKey(0)


    final = adaptiveMedianFilter(image)
   
    final = final.astype(np.uint8)
    cv2.imshow('Adaptive Median Filter Image ', final)
    cv2.waitKey(0) 

main()