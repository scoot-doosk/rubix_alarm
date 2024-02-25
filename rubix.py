# Rubix cube image detection library
  
# importing
import cv2
import numpy as np  
import copy

# takes bgr image and does proccessing to return a smooth black and white ideal for contour detection
def blur_sharpen(image):
#convert to hsv for detection blur and sharpen to smooth
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 45, 255, cv2.THRESH_BINARY_INV)[1]
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
    height, width = close.shape[:2]
    image_area = height*width
    min_area = int(image_area*(1/50))
    max_area = int(image_area*(1/10)) 
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

def get_square_color(image, square):
    average_color = cv2.mean(image[square["topl"][1]:square["botr"][1],square["topl"][0]:square["botr"][0]])
    return average_color


cap = cv2.VideoCapture(2)


#Display camera and wait for y to capture
def vid2still():
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        init_frame = copy.deepcopy(frame)
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # prep image
        prepped_image = blur_sharpen(frame)

        #identify interesting square regions
        squares = find_squares(prepped_image)

        cv2.imshow("frame", draw_squares(frame, squares))

        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite('./still.png',init_frame)
            break
        if cv2.waitKey(1) == ord('y'): #save on pressing 'y' 
            #cv2.imwrite('./still.png',frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def name_color(bgr_color):
    color = "Undefined"
    hsv = cv2.cvtColor(np.uint8([[[int(bgr_color[0]),int(bgr_color[1]),int(bgr_color[2])]]]), cv2.COLOR_BGR2HSV)
    hue_value = hsv[0][0][0]
    print(hue_value)
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 80:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"
    return color

vid2still()

# path
path = r'./still.png'

#Reading an image in default mode
image = cv2.imread(path)

# prep image
prepped_image = blur_sharpen(image)

#identify interesting square regions
squares = find_squares(prepped_image)

for square in squares:
    print(name_color(get_square_color(image, square)))

