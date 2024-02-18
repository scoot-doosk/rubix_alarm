# Python program to explain cv2.imshow() method
  
# importing
import cv2
import numpy as np  

# path
path = r'/home/scoots/rubix_alarm/top_old.jpg'
# Reading an image in default mode
image = cv2.imread(path)


# takes bgr image and does proccessing to return a smooth black and white ideal for contour detection
def blur_sharpen(image):
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

    return sharpened_close


def find_squares(close):
    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    #FIXME do something with percentages of image size
    height, width = image.shape[:2]
    image_area = height*width
    min_area = int(image_area*(1/50))
    max_area = int(image_area*(1/5)) 
    squares = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area and area < max_area:
            x,y,w,h = cv2.boundingRect(c)
            square = {
                "topl": (int(x + .2*w), int(y + .2*h)),
                "botr": (int(x + .8*w), int(y + .8*h)) 
            }
            squares.append(square)
    return squares

def draw_squares(image, squares):
    for square in squares:
        cv2.rectangle(image, square["topl"], square["botr"], (36,255,12), 2)
    return image

# prep image
prepped_image = blur_sharpen(image)

#identify interesting square regions
squares = find_squares(prepped_image)

#draw squares arround areas of interest on image and display
cv2.imshow('image', draw_squares(image, squares))
cv2.waitKey(0)