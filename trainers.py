#!/usr/bin/env python3

# sudo apt-get install python-opencv  ?
# sudo apt-get install python3-opencv

import math
import cv2
import numpy as np
import argparse

def draw_hexagon(base_color, spot1, spot2):
    size = 500;
    half = size/2
    img = np.zeros((size,size,3), np.uint8)
    verts = []
    for c in range(7):
        #deg in (30, 90, 150, 210, 270, 330, 30):
        deg = 30 + c*60
        a = math.radians(deg)
        x = round(half + math.cos(a) * half)
        y = round(half - math.sin(a) * half)
        verts.append((x, y))
    cv2.fillConvexPoly(img, np.array(verts, 'int32'), base_color)

    qtr = half/2
    for deg in (30, 150, 270):
        a = math.radians(deg)
        x = round(half + math.cos(a) * qtr)
        y = round(half - math.sin(a) * qtr)
        cv2.circle(img, (x, y), int(qtr/4), spot1, -1)

    for deg in (90, 210, 330):
        a = math.radians(deg)
        x = round(half + math.cos(a) * qtr)
        y = round(half - math.sin(a) * qtr)
        cv2.circle(img, (x, y), int(qtr/4), spot2, -1)

    return img

red = (0,0,255)
ylw = (0,255,255)
blu = (255,0,0)
org = (0,165,255)
grn = (0,255,0)
ppl = (255,0,255)
img = draw_hexagon(red, ylw, ppl)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("0red.png", img)

img = draw_hexagon(ylw, org, blu)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("1ylw.png", img)

img = draw_hexagon(blu, red, grn)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("2blu.png", img)

img = draw_hexagon(ppl, blu, ppl)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("3ppl.png", img)

img = draw_hexagon(org, org, red)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("4org.png", img)

img = draw_hexagon(grn, ylw, grn)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.imwrite("5grn.png", img)



