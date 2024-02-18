# Python program to explain cv2.imshow() method
  
# importing
import cv2
import numpy as np  
from matplotlib import pyplot as plt

# path
path = r'/Users/sdoskocz/rubix/top.jpg'
# Reading an image in default mode
image = cv2.imread(path)

#convert to hsv for detection blur and sharpen to smooth
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

# Threshold and morph close
thresh = cv2.threshold(sharpen, 30, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# reblur and sharpen
blur = cv2.medianBlur(close, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpened_close = cv2.filter2D(blur, -1, sharpen_kernel)


# Find contours and filter using threshold area
cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

#FIXME do something with percentages of image size
height, width = image.shape[:2]
image_area = height*width
min_area = int(image_area*(1/50))
max_area = int(image_area*(1/5)) 
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > min_area and area < max_area:
        x,y,w,h = cv2.boundingRect(c)
        #ROI = image[y:y+h, x:x+w]
        #cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
        cv2.rectangle(image, (int(x + .2*w), int(y + .2*h)), (int(x + .8*w), int(y + .8*h)), (36,255,12), 2)
        image_number += 1

cv2.imshow('sharpen', sharpen)
cv2.imshow('close', close)
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey(0)