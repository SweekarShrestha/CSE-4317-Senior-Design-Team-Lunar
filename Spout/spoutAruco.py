import sys
import os
 
sys.path.append('{}/Library/3{}'.format(os.getcwd(), sys.version_info[1]))
 
import argparse
import cv2
import SpoutSDK
import cv2.aruco as aruco

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def findArucoMarkers(frame, markerSize = 6, totalMarkersAvailable = 250, draw = False):
    # arg1 -> frame is the feed where we are trying to find the aruco markers
    # arg2 -> the marker size, default is 6x6
    # arg3 -> total numbers of markers that the dictionary is composed of
    # arg4 -> a boolean flag to draw the bounding box if needed, its false by default
    # change frame to greyscale
    frameGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # getattr uses the argument value provided in markerSize and totalMarkersAvailable to be used by arucoDict
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkersAvailable}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    boundingBoxes, foundMarkersIds, rejectedMarkers = aruco.detectMarkers(frameGrey, arucoDict, parameters = arucoParam)

    if draw:
        aruco.drawDetectedMarkers(frame, boundingBoxes)
    
    # we are returning the bounding boxes of markers, and the id of all the foundMarkers
    
    return [boundingBoxes, foundMarkersIds]

 
"""parsing and configuration"""
def parse_args():
    desc = "Spout for Python webcam sender example"
    parser = argparse.ArgumentParser(description=desc)
 
    parser.add_argument('--camSize', nargs = 2, type=int, default=[640, 480], help='File path of content image (notation in the paper : x)')
 
    parser.add_argument('--camID', type=int, default=1, help='Webcam Device ID)')
 
    return parser.parse_args()
 
 
"""main"""
def main():
 
    # parse arguments
    args = parse_args()
 
    # window details
    width = args.camSize[0]
    height = args.camSize[1]
    display = (width,height)
 
    # window setup
    pygame.init()
    pygame.display.set_caption('Webcam')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
 
    # init capture & set size
    #cap = cv2.VideoCapture(args.camID)
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
 
    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glOrtho(0,width,height,0,1,-1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glEnable(GL_TEXTURE_2D)
 
    # init spout sender
    spoutSender = SpoutSDK.SpoutSender()
    spoutSenderWidth = width
    spoutSenderHeight = height
    # Its signature in c++ looks like this: bool CreateSender(const char *Sendername, unsigned int width, unsigned int height, DWORD dwFormat = 0);
    spoutSender.CreateSender('Spout for Python Webcam Sender Example', width, height, 0)
 
    # create texture id for use with Spout
    senderTextureID = glGenTextures(1)
 
    # initalise our sender texture
    glBindTexture(GL_TEXTURE_2D, senderTextureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)
 
    # loop
    while(True):
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()
 
        ret, frame = cap.read()
        7

        foundArucoMarkers = findArucoMarkers(frame)

        if len(foundArucoMarkers[0]) != 0:
            # looping through each boundingBox and markerId -> using zip function
            for boundingBox, markerId in zip(foundArucoMarkers[0], foundArucoMarkers[1]):
                # markers are of type numpy array -> in our case because we are only detecting one marker at a time it will only
                # be a numpy array with one element, containing the id of the marker
                print(markerId[0])
 
        # Copy the frame from the webcam into the sender texture
        glBindTexture(GL_TEXTURE_2D, senderTextureID)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, frame )
 
        # Send texture to Spout
        # Its signature in C++ looks like this: bool SendTexture(GLuint TextureID, GLuint TextureTarget, unsigned int width, unsigned int height, bool bInvert=true, GLuint HostFBO = 0);
        spoutSender.SendTexture(2, GL_TEXTURE_2D, spoutSenderWidth, spoutSenderHeight, False, 0) 
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset the drawing perspective
        glLoadIdentity()
 
        # Draw texture to screen
        glBegin(GL_QUADS)
 
        glTexCoord(0,0)
        glVertex2f(0,0)
 
        glTexCoord(1,0)
        glVertex2f(width,0)
 
        glTexCoord(1,1)
        glVertex2f(width,height)
 
        glTexCoord(0,1)
        glVertex2f(0,height)
 
        glEnd()
 
        # update window
        pygame.display.flip()
 
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_2D, 0)
 
if __name__ == "__main__":
    main()