import cv2
import HandTrackingModule as htm

videoCapture = cv2.VideoCapture(0)

# instantiation of HandMotionTracker
handMotionTracker = htm.HandMotionTracker()

while True:
    success, img = videoCapture.read()
    img = cv2.flip(img, 1)
    img = handMotionTracker.mapHands(img)
    positionList = handMotionTracker.retrievePosition(img)

    #Print position of joint 4 - refer to mediapipe's hand landmark joints map
    if (len(positionList) > 0):
        print(positionList[4])

    if success:
        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break