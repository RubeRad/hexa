#!/usr/bin/env python3

# sudo apt-get install python-opencv  ?
# sudo apt-get install python3-opencv

import sys
import os
import re
import math
sys.path.insert(0, "C:\python3\Lib\site-packages")
import cv2
import numpy as np
import argparse

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
    minr = int(h*row)
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
                  idx,  # which triangle in the row
                  typ): # GLUE or BLANK
    tri = triangleVertices(updn, row, idx)
    if (typ == 'GLUE'):
        color = (255,255,255,255) # white
    else:
        color = (0,0,0,0)         # blank/transparent
    cv2.fillConvexPoly(outimg, tri, color)
    if (typ == 'GLUE'):
        drawBoundary(tri)

def copyTriangle(img, # openCV image
                 tri, # which triangle of the img, 0-5
                 ctr, # where does the center go, 'bot' or 'lr'
                 row, # 0, 1, ...
                 idx): # which triangle in the row
    #crot = centerOfTriangle(img, tri, ctr)
    crot = centerOfImage(img)

    if debug:
        lilsqr=np.array([[int(crot[0]-10),int(crot[1]-10)], [int(crot[0]-10),int(crot[1]+10)], [int(crot[0]+10),int(crot[1]+10)], [int(crot[0]+10),int(crot[1]-10)]])
        cv2.fillConvexPoly(img, lilsqr, (255,0,0))
        cv2.imwrite('imgdot.png', img)
    src_cnr = -120 + 60*tri # where is the center-corner originally?
    if   ctr == 'll':
        dst_cnr = -150
    elif ctr == 'bot':
        dst_cnr = -90
    elif ctr == 'lr':
        dst_cnr = -30
    elif ctr == 'ur':
        dst_cnr = +30
    elif ctr == 'top':
        dst_cnr = +90
    elif ctr == 'ul':
        dst_cnr = +150
    #else:

    arot = dst_cnr - src_cnr
    R = cv2.getRotationMatrix2D(crot, arot, 1)
    rot = cv2.warpAffine(img, R, (side*2, side*2))
    if debug:
        cv2.fillConvexPoly(rot, lilsqr, (255,0,0))
        cv2.imwrite('rot.png', rot)

    hh = int(h)
    # what rows do we copy from?
    if ctr == 'bot' or ctr == 'lr' or ctr == 'll':
        minr = int(crot[1] - h)
        maxr = int(crot[1])
    else: # top or ur or ul
        minr = int(crot[1])
        maxr = int(crot[1] + h)

    # which columns do we copy from?
    if ctr == 'lr' or ctr == 'ur':
        minc = int(crot[0] - side)
        maxc = int(crot[0])
    elif ctr == 'bot' or ctr == 'top':
        minc = int(crot[0] - side/2)
        maxc = int(crot[0] + side/2)
    else: # ll or ul
        minc = int(crot[0])
        maxc = int(crot[0] + side)

    # after cropping, where do we erase?
    if   ctr == 'bot' or ctr == 'ur' or ctr == 'ul': # point dn, blanks ll, lr
        tril = np.array([[0,0], [side//2,hh], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, hh]])
    else:  # top/lr/ll: point up, blanks ul, ur
        tril = np.array([[0,0], [side//2,0], [0, hh]])
        trir = np.array([[side,0], [side,hh], [side//2, 0]])

    crop = cv2.cvtColor(rot[minr:maxr, minc:maxc], cv2.COLOR_BGR2BGRA)
    if debug:
        cv2.imwrite('crop.png', crop)
    cv2.fillConvexPoly(crop, tril, (0,0,0,0))
    cv2.fillConvexPoly(crop, trir, (0,0,0,0))
    if debug:
        cv2.imwrite('crop.png', crop)

    minr = int(h*row);        maxr = minr+crop.shape[0]
    minc = index * side//2;   maxc = minc+crop.shape[1]
    roi = outimg[minr:maxr, minc:maxc]
    cnd = crop[:, :, 3] > 0
    roi[cnd] = crop[cnd]
    if debug:
        cv2.imwrite('out.png', outimg)

    if ctr=='lr' or ctr=='ll' or ctr=='top':
        updn = 'up'
    else: # ul/ur/bot
        updn = 'dn'
    tri = triangleVertices(updn, row, idx)
    drawBoundary(tri)
    stophere=1

parser = argparse.ArgumentParser("Make a printable hexaflexagon template")
parser.add_argument('images', type=str, nargs='+',
                    help='Filenames of pictures')
parser.add_argument('--out', type=str,
                    help='Output filename', default='out.png')
parser.add_argument('--cfg', type=str,
                    help='Config filename', default='tri.cfg')
parser.add_argument('--pix', type=int,
                    help='Input img resample size', default=1000)
parser.add_argument('--hexify', action='store_true',
                    help='Output _hex.png to show hexification')
args = parser.parse_args()
side = args.pix // 2 # each side of each triangle

image=[]
for fname in args.images:
    tmpimg = cv2.imread(fname)
    dim0 = tmpimg.shape[0]
    dim1 = tmpimg.shape[1]
    # resize so smaller dimension is args.pix
    ratio = args.pix / min(dim0,dim1)
    sized = cv2.resize(tmpimg, (math.ceil(dim0*ratio),
                                math.ceil(dim1*ratio)))
    ctr = centerOfImage(sized)
    cropped = sized[ctr[0]-side:ctr[0]+side,
                    ctr[1]-side:ctr[1]+side]
    image.append( cropped )
# now all images are pixXpix = 2side X 2side


if args.hexify: # use hardcoded cfg for each image
    nloops=len(args.images)
else: # read .cfg from file
    nloops=1
    patfile = open(args.cfg, 'r');
    nrows = 2 # default, unless overridden in cfg
    lines = patfile.readlines()
    tri = []
    for line in lines:
        line = re.sub("\#.*", '', line)
        rows = re.match('ROWS\s+(\d+)', line)
        if rows:
            nrows = int(rows.group(1))
        elif re.match('\S', line):
            tri.append(line)

for loop in range(nloops):
    if args.hexify: # set up tri for each face
        print("hexifying", args.images[loop])
        nrows = 2;
        tri = [str(loop)+".1 lr\n",
               str(loop)+".0 bot\n",
               str(loop)+".5 ll\n",
               str(loop)+".2 ur\n",
               str(loop)+".3 top\n",
               str(loop)+".4 ul\n"]

    triwidth = len(tri)//nrows
    h  = math.sqrt(side*side - side*side/4)
    nr = int(math.ceil(nrows*h))
    nc = int((triwidth+1) * (side/2))
    outimg = np.zeros((nr, nc, 4))
    #cv2.imwrite('out.png', outimg)

    for i in range(len(tri)):
        print(tri[i], end='')
        index = i %  triwidth
        row   = i // triwidth
        glue = re.match('(GLUE|BLANK)\s+(up|dn)', tri[i])
        if glue:
            edges  = glue.group(1)
            corner = glue.group(2)
            whiteTriangle(corner, row, index, edges)
            continue;
        # else match face/triangle/corner
        ftc = re.match('(\d+)\.(\d)\s+(bot|top|lr|ll|ul|ur|na)', tri[i])
        facei   = int(ftc.group(1))
        trii    = int(ftc.group(2))
        corner  =     ftc.group(3)

        copyTriangle(image[facei], trii, corner, row, index)

    if args.hexify:
        innfname = args.images[loop]
        bas = re.match('(.*)\....$', innfname) # assume 3-char extension
        outfname = bas.group(1) + "_hex.png"
        cv2.imwrite(outfname, outimg)
    else:
        cv2.imwrite(args.out, outimg)



