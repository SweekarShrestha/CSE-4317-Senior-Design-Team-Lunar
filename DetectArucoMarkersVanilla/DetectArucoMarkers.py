import cv2
import cv2.aruco as aruco
import numpy as np
import os #needed to access directory containing actual marker pictures

# Steps to use this module
# 1) Load all the images using loadAugmentedImages function
# 2) Find all the markers using the findArucoMarkers function
# 3) Then, we will call augmentImageOntoAruco function to augment images onto the found markers

def findArucoMarkers(webcamFeed, markerSize = 6, totalMarkersAvailable = 250, draw = False):
    # arg1 -> webcamFeed is the feed where we are trying to find the aruco markers
    # arg2 -> the marker size, default is 6x6
    # arg3 -> total numbers of markers that the dictionary is composed of
    # arg4 -> a boolean flag to draw the bounding box if needed, its false by default
    # change webcamFeed to greyscale
    webcamFeedGrey = cv2.cvtColor(webcamFeed, cv2.COLOR_BGR2GRAY)

    # getattr uses the argument value provided in markerSize and totalMarkersAvailable to be used by arucoDict
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkersAvailable}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    boundingBoxes, foundMarkersIds, rejectedMarkers = aruco.detectMarkers(webcamFeedGrey, arucoDict, parameters = arucoParam)

    if draw:
        aruco.drawDetectedMarkers(webcamFeed, boundingBoxes)
    
    # we are returning the bounding boxes of markers, and the id of all the foundMarkers
    return [boundingBoxes, foundMarkersIds]


def main():
    webcamCapture = cv2.VideoCapture(0)

    while True:

        # checking if webcam feed is successfully captured
        success, webcamFeed = webcamCapture.read()

        # a list is returned, 0th element is the bounding boxes, 1st element contains all of the Ids
        foundArucoMarkers = findArucoMarkers(webcamFeed)

        # loop through all the foundArucoMarkers and augment an image onto each of the marker
        # if length of the 1st element (bounding boxes) is 0, then we did not detect anything
        if len(foundArucoMarkers[0]) != 0:
            # looping through each boundingBox and markerId -> using zip function
            for boundingBox, markerId in zip(foundArucoMarkers[0], foundArucoMarkers[1]):
                # markers are of type numpy array -> in our case because we are only detecting one marker at a time it will only
                # be a numpy array with one element, containing the id of the marker
                print(markerId[0])

        cv2.imshow("Webcam Feed", webcamFeed)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
