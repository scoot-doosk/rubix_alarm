import rubix
import cv2

#open camera
cap = cv2.VideoCapture(2)

#start alarm


solved = False
while(not solved):
    #wait for button press

    #Check if solved
    #loop through faces
    face_cnt = 0
    for i in range(0,3):
        #get still of face
        rubix.vid2still(cap)

        #Check face
        if not rubix.checkFace():
            break

        #rotate platter 90 degrees
    solved = True

#Play affirmation