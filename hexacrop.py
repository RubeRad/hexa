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

def centerRowCol(img):
    midrow = img.shape[0]//2
    midcol = img.shape[1]//2 
    return (midrow, midcol)
            

def drawHexagon(img, row, col, rad):
    rows = []
    cols = []
    blk=(0,0,0)
    for deg in (30, 90, 150, 210, 270, 330, 30):
        a = math.radians(deg)
        dx = round(math.cos(a) * rad)
        dy = round(math.sin(a) * rad)
        cols.append(col+dx)
        rows.append(row-dy)
    for i in range(len(rows)-1):
        cv2.line(img, (cols[i],rows[i]), (col,       row),       blk)
        cv2.line(img, (cols[i],rows[i]), (cols[i+1], rows[i+1]), blk)

#####################################
### Main begins here
#####################################
parser = argparse.ArgumentParser("Crop an image so a hexagon looks good")
parser.add_argument('images', type=str, nargs='+',
                    help='Filename of picture')
parser.add_argument('--pix', type=int,
                    help='Output img size (square)', default=1000)
args = parser.parse_args()

# this is the original image
fname = args.images[0]
path = os.path.abspath(fname)
dir,file = os.path.split(path)
oimg = cv2.imread(fname)
orows = oimg.shape[0] # here rows/h before
ocols = oimg.shape[1] #      cols/w

# scale it down to max dimension 700
ratio = 700 / max(orows, ocols);
oshow = cv2.resize(oimg, None, fx=ratio, fy=ratio)
ctr = centerRowCol(oshow) # hexagon center
row = ctr[0]
col = ctr[1]
rad = min(ctr[0], ctr[1]) # hexagon radius
orad = rad
stp = 1 # pixel
cv2.namedWindow(fname)

while True:
    # draw current hexagon
    show = oshow.copy()
    drawHexagon(show, row, col, rad)
    # render in window, wait for keystroke
    cv2.imshow(fname, show)
    c = cv2.waitKey(0)
    # act on keystroke
    if   (c == ord('q')): break
    elif (c == ord('w')): row -= stp
    elif (c == ord('a')): col -= stp
    elif (c == ord('s')): row += stp
    elif (c == ord('d')): col += stp
    elif (c == ord(',')): rad -= stp
    elif (c == ord('.')): rad += stp
    elif (c >= ord('1') and
          c <= ord('9')): stp = c - ord('0')
    elif (c == ord('c')): # crop!
        # fetch affine xform with no rotation or scale
        # that robustly handles outside-image conditions
        halfpix = int(rad/ratio)
        oldrow = row/ratio # this is where the desired center is originally
        oldcol = col/ratio
        I = np.float32([[1,0,halfpix-oldcol],[0,1,halfpix-oldrow]])
        crop   = cv2.warpAffine(oimg, I, (halfpix*2, halfpix*2))
        outimg = cv2.resize(crop, (args.pix,args.pix))
        outfname = os.path.join(dir, "crop_"+file)
        cv2.imwrite(outfname, outimg)
        print('Wrote '+outfname)
        break

