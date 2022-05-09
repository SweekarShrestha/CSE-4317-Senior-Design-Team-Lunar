import cv2
import HandTrackingModule as htm
import numpy as np

# https://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
# 1) Find Hand landmarks
# 2) Check which fingers are up
# 3) If at selection mode (2 fingers are up) - select
# 4) If at drawing mode (index finger up) - draw

# caputure img from camera
videoCapture = cv2.VideoCapture(0)

# instantiate hand motion tracker class from htm module
handTrackingTracker = htm.HandMotionTracker(detectionConfidence=0.90, trackingConfidence=0.90)

# initalize np array of pixel size 1920 x 1080, third param is 3 because colors are stored in 3 RGBm and we will store in unsigned 8 bit int
background = np.zeros((720, 1280, 3))

while True:
    # get img caputre from opencv, and set success bool flag T or F depending on if video img is caputred
    success, img = videoCapture.read()

    if success:
        # flip the captured img horizontally to make it intuitive to draw
        img = cv2.flip(img, 1)

        # calling mapHands method to map hand with points
        img = handTrackingTracker.mapHands(img)

        # calling retrievePosition method to get the coordinate position of hand
        handPositionList = handTrackingTracker.retrievePosition(img)

        if(len(handPositionList) > 0):
            # print(handPositionList[8])

            # according to Google mediapipe graph, point of index finger is number 8
            # [8][1:] means for id 8 (index finger point), which is 0th element, only get 1th element to the end
            # same for middle finger, id -> 12
            indexFingerPointX, indexFingerPointY = handPositionList[8][1:]
            prevIndexFingerPointX, prevIndexFingerPointY = 0, 0

            fingersPointingUp = handTrackingTracker.fingersPointingUp()
            # print(fingersPointingUp)

            drawMode = False
            nonDrawMode = False

            # only draw if index finger is up and stop drawing if index and middle finger is up
            if(fingersPointingUp[1] == 1 and fingersPointingUp[2] == 0 and fingersPointingUp[3] == 0 and fingersPointingUp[4] == 0 and fingersPointingUp[0] == 0):
                drawMode = True
                # draw a circle in the fingerpoint if draw mode is on might have to edit 3rd parameter depending on the system
                cv2.circle(img, (indexFingerPointX, indexFingerPointY), 17,  (255, 0, 255), cv2.FILLED)
                # print("drawMode")

                # first render when prevIndex = 0
                if(prevIndexFingerPointX == 0 and prevIndexFingerPointY == 0):
                    prevIndexFingerPointX = indexFingerPointX
                    prevIndexFingerPointY = indexFingerPointY

                # Might have to edit the last number of the last parameter for both lines below depennding on the system
                cv2.line(img, (prevIndexFingerPointX, prevIndexFingerPointY), (indexFingerPointX, indexFingerPointY), (255, 0, 255), 12)
                cv2.line(background, (prevIndexFingerPointX, prevIndexFingerPointY), (indexFingerPointX, indexFingerPointY), (255, 0, 255), 30)

                # after something is drawn already
                indexFingerPointX = prevIndexFingerPointX
                indexFingerPointY = prevIndexFingerPointY

            else:
                nonDrawMode = True
                # print("nonDrawMode")

        # blend two images camera, and black background together
        img = cv2.addWeighted(img, 1, background, 0.5, 0, dtype = 0)

        #The following commented line will indicate screen size which must match with the background np.zeoros initaialization up top
        #print(img.shape)
        cv2.imshow('frame', img)
        cv2.imshow('background', background)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
