#! /usr/bin/python3

import sys
import os
import re
import math
import cv2
import numpy as np

def centerOfImage(img):
    return (img.shape[0]//2, img.shape[1]//2)

# start at center of image, and move out half a triangle height
# along the appropriate angle
def centerOfTriangle(img, tri):
    c = centerOfImage(img)
    a = math.radians( 60*(tri+1) )
    dx = math.cos(a)*h/2
    dy = math.sin(a)*h/2
    return (c[0]+dx, c[1]-dy)

def copyTriangle(img, # openCV image
                 tri, # which triangle of the img, 0-5
                 ctr, # where does the center go, 'bot' or 'lr'
                 row, # 0 (top/front) or 1 (bot/rear)
                 idx): # which triangle in the row
    crot = centerOfTriangle(img, tri)
    src_cnr = -120 + 60*tri # where is the center-corner originally?
    if   ctr == 'bot':
        dst_cnr = -90
    elif ctr == 'lr':
        dst_cnr = -30
    arot = dst_cnr - src_cnr
    R = cv2.getRotationMatrix2D(crot, arot, 1)
    rot = cv2.warpAffine(img, R, (side*4, side*4))
    cv2.imwrite('rot.png', rot)
    minr = int(crot[1]-   h/2);  maxr = int(minr+h)
    minc = int(crot[0]-side/2);  maxc = minc + side
    crop = cv2.cvtColor(rot[minr:maxr, minc:maxc], cv2.COLOR_BGR2BGRA)
    cv2.imwrite('crop.png', crop)
    hh = crop.shape[0]
    if   ctr == 'bot':
        tril = np.array([[0,0], [side//2,hh], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, hh]])
    else:
        tril = np.array([[0,0], [side//2,0], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, 0]])
    cv2.fillConvexPoly(crop, tril, (0,0,0,0))
    cv2.fillConvexPoly(crop, trir, (0,0,0,0))

    cv2.imwrite('crop.png', crop)

    minr = h if row else 0;  maxr = minr+crop.shape[0]
    minc = index * side//2;  maxc = minc+crop.shape[1]
    roi = outimg[minr:maxr, minc:maxc]
    cnd = crop[:, :, 3] > 0
    roi[cnd] = crop[cnd]
    cv2.imwrite('out.png', outimg)

    stophere=1

image=[]
for i in range(len(sys.argv)):
    if i==0: continue
    image.append( cv2.imread(sys.argv[i]) )
    side = image[-1].shape[0] // 2 # TBD: diff, non-square

patfile = open('tri.cfg', 'r')
lines = patfile.readlines()
tri = []
for line in lines:
    line = re.sub("\#.*", '', line)
    if re.match('\S', line):
        tri.append(line)

half = len(tri)//2
h  = math.sqrt(side*side - side*side/4)
nr = int(math.ceil(2*h))
nc = int((half+1) * (side/2))
outimg = np.zeros((nr, nc, 4))
cv2.imwrite('out.png', outimg)



for i in range(len(tri)):
    index   = i % half
    if re.match('GLUE', tri[i]):
        continue;
    ftc = re.match('(\d+)\.(\d)\s+(bot|lr|na)', tri[i])
    facei   = int(ftc.group(1))
    trii    = int(ftc.group(2))
    corner  =     ftc.group(3)
    row     = int(i >= half)
    copyTriangle(image[facei], trii, corner, row, index)




