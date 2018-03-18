#! /usr/bin/python3

import sys
import os
import re
import math
import cv2
import numpy as np

debug = False

def centerOfImage(img):
    return (img.shape[0]//2, img.shape[1]//2)

# start at center of image, and move out half a triangle height
# along the appropriate angle
def centerOfTriangle(img, tri, ctr):
    c = centerOfImage(img)
    if (ctr == 'bot'):
        a = math.radians( 60*(tri+1) )
        dx = math.cos(a)*h/2
        dy = math.sin(a)*h/2
    else:
        a = math.radians( 60*(tri+1)+30)
        dx = math.cos(a)*side/2
        dy = math.sin(a)*side/2
        a -= math.radians(90)
        dx += math.cos(a)*h/2
        dy += math.sin(a)*h/2

    return (c[0]+dx, c[1]-dy)

def triangleVertices(updn, row, idx):
    minc = side*idx//2;
    maxc = minc+side
    minr = int(h) if row else 0
    maxr = int(minr + h)
    basr = maxr if updn=='up' else minr
    tipr = minr if updn=='up' else maxr
    tri = np.array([[minc, basr], [maxc, basr], [(minc + maxc) // 2, tipr]])
    return tri

def drawBoundary(tri):
    cv2.line(outimg, (tri[0][0],tri[0][1]), (tri[1][0],tri[1][1]), (0,0,0,255), 3)
    cv2.line(outimg, (tri[1][0],tri[1][1]), (tri[2][0],tri[2][1]), (0,0,0,255), 3)
    cv2.line(outimg, (tri[2][0],tri[2][1]), (tri[0][0],tri[0][1]), (0,0,0,255), 3)


def whiteTriangle(updn, # is the point 'up' or 'dn'?
                  row,  # 0 (top/front) or 1 (bot/rear)
                  idx): # which triangle in the row
    tri = triangleVertices(updn, row, idx)
    cv2.fillConvexPoly(outimg, tri, (255,255,255,255))
    drawBoundary(tri)

def copyTriangle(img, # openCV image
                 tri, # which triangle of the img, 0-5
                 ctr, # where does the center go, 'bot' or 'lr'
                 row, # 0 (top/front) or 1 (bot/rear)
                 idx): # which triangle in the row
    #crot = centerOfTriangle(img, tri, ctr)
    crot = centerOfImage(img)

    if debug:
        lilsqr=np.array([[int(crot[0]-10),int(crot[1]-10)], [int(crot[0]-10),int(crot[1]+10)], [int(crot[0]+10),int(crot[1]+10)], [int(crot[0]+10),int(crot[1]-10)]])
        cv2.fillConvexPoly(img, lilsqr, (255,0,0))
        cv2.imwrite('imgdot.png', img)
    src_cnr = -120 + 60*tri # where is the center-corner originally?
    if   ctr == 'bot':
        dst_cnr = -90
    elif ctr == 'lr':
        dst_cnr = -30
    elif ctr == 'ur':
        dst_cnr = +30
    arot = dst_cnr - src_cnr
    R = cv2.getRotationMatrix2D(crot, arot, 1)
    rot = cv2.warpAffine(img, R, (side*2, side*2))
    if debug:
        cv2.fillConvexPoly(rot, lilsqr, (255,0,0))
        cv2.imwrite('rot.png', rot)


    hh = int(h)
    # where do we copy the triangle from the rotated image?
    if ctr == 'bot':
        minc = int(crot[0] - side/2)
        maxc = int(crot[0] + side/2)
        minr = int(crot[1] - h)
        maxr = int(crot[1])
    elif ctr == 'lr':
        minc = int(crot[0] - side)
        maxc = int(crot[0])
        minr = int(crot[1] - h)
        maxr = int(crot[1])
    elif ctr == 'ur':
        minc = int(crot[0]-side)
        maxc = int(crot[0])
        minr = int(crot[1])
        maxr = int(crot[1] + h)
    #else: not implemented yet

    # after cropping, where do we erase?
    if   ctr == 'bot' or ctr == 'ur': # point dn, blanks ll, lr
        tril = np.array([[0,0], [side//2,hh], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, hh]])
    else:                             # point up, blanks ul, ur
        tril = np.array([[0,0], [side//2,0], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, 0]])

    crop = cv2.cvtColor(rot[minr:maxr, minc:maxc], cv2.COLOR_BGR2BGRA)
    if debug:
        cv2.imwrite('crop.png', crop)
    cv2.fillConvexPoly(crop, tril, (0,0,0,0))
    cv2.fillConvexPoly(crop, trir, (0,0,0,0))
    if debug:
        cv2.imwrite('crop.png', crop)

    minr = hh if row else 0;  maxr = minr+crop.shape[0]
    minc = index * side//2;   maxc = minc+crop.shape[1]
    roi = outimg[minr:maxr, minc:maxc]
    cnd = crop[:, :, 3] > 0
    roi[cnd] = crop[cnd]
    if debug:
        cv2.imwrite('out.png', outimg)

    updn = 'up' if ctr=='lr' else 'dn'
    tri = triangleVertices(updn, row, idx)
    drawBoundary(tri)
    stophere=1

image=[]
for i in range(len(sys.argv)):
    if i==0: continue
    tmpimg = cv2.imread(sys.argv[i])
    img = cv2.resize(tmpimg, (316,316))
    image.append( img ) #cv2.imread(sys.argv[i]) )
    side = image[-1].shape[0] // 2 # TBD: diff, non-square

if (len(sys.argv) == 4):
    patfile = open('tri.cfg', 'r')
elif (len(sys.argv) == 7):
    patfile = open('hex.cfg', 'r')
# else ...

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
#cv2.imwrite('out.png', outimg)



for i in range(len(tri)):
    print(tri[i])
    index =     i %  half
    row   = int(i >= half)
    glue = re.match('GLUE\s+(up|dn)', tri[i])
    if glue:
        corner = glue.group(1)
        whiteTriangle(corner, row, index)
        continue;
    # else match face/triangle/corner
    ftc = re.match('(\d+)\.(\d)\s+(bot|lr|ur|na)', tri[i])
    facei   = int(ftc.group(1))
    trii    = int(ftc.group(2))
    corner  =     ftc.group(3)

    copyTriangle(image[facei], trii, corner, row, index)

cv2.imwrite('out.png', outimg)



