import rubix
import cv2

#open camera
cap = cv2.VideoCapture(2)

#pull frame on q press
rubix.vid2still(cap)

# path
path = r'./still.png'

#Reading an image in default mode
image = cv2.imread(path)

# prep image
prepped_image = rubix.blur_sharpen(image)

#identify interesting square regions
squares = rubix.find_squares(prepped_image)

for square in squares:
    print(rubix.name_color(rubix.get_square_color(image, square)))
