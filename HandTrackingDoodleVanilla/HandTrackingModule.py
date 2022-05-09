import cv2
import mediapipe as mp

# https://www.youtube.com/c/MurtazasWorkshopRoboticsandAI

class HandMotionTracker():
    # basic parameters required for medapipe Hands
    # these attributes can be used to change the default params that gets passed in when we initialize
    def __init__(self, mode=False, maxNumberOfHands=2, detectionConfidence=0.5, trackingConfidence=0.5):

        # initializing instance of HandMotionTracker
        self.mode = mode
        self.maxNumberOfHands = maxNumberOfHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence
        self.mpHands = mp.solutions.hands
        self.modelComplexity = 1
        self.hands = self.mpHands.Hands(self.mode, self.maxNumberOfHands, self.modelComplexity, self.detectionConfidence,
                                        self.trackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.fingerPointIds = [4, 8, 12, 16, 20] # finger point mediapipe Ids


    def mapHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # check if hand motion is detected in the console
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLandmark in self.results.multi_hand_landmarks:
                # each landmark has a lot of points on the coordinate plane and
                # we want to draw all of them using a function provided by mediapipe, declared above as mpDraw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def retrievePosition(self, img, handJointNumber = 0, draw = True):
        self.landMarkList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handJointNumber]
            for id, landmark in enumerate(hand.landmark):
                # print(id, landmark)
                height, width, channelOfImg = img.shape
                centerX, centerY = int(landmark.x * width), int(landmark.y * height)
                self.landMarkList.append([id, centerX, centerY])

                if draw:
                    cv2.circle(img, (centerX, centerY), 0, (255, 0, 255), 3, cv2.FILLED)

        return self.landMarkList

    def fingersPointingUp(self):
        fingers = []

        # check if thumb is on the left or right, telling us its its opened or closed
        if self.landMarkList[self.fingerPointIds[0]][1] > self.landMarkList[self.fingerPointIds[0] - 1][1]:
            fingers.append(1) # thumb open
        else:
            fingers.append(0) # thumb closed

        # check if other 4 fingers positions are pointing up or below, it will be pointing down if the position of it
        # is 2 positions below the mediapipe point below
        for id in range(1, 5):
            if self.landMarkList[self.fingerPointIds[id]][2] < self.landMarkList[self.fingerPointIds[id] - 2][2]:
                fingers.append(1) # fingers open
            else:
                fingers.append(0) # fingers closed
        return fingers

def main():
    prevTime = 0
    currTime = 0
    videoCapture = cv2.VideoCapture(0)

    # instantiation of HandMotionTracker
    handMotionTracker = HandMotionTracker()

    while True:
        success, img = videoCapture.read()
        img = handMotionTracker.mapHands(img)
        positionList = handMotionTracker.retrievePosition(img)

        if(len(positionList) > 0):
            print(positionList[4])

        if success:
            cv2.imshow('frame', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

# if we are running this script
if __name__ == "__main__":
    main()