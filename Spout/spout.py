import sys
import os
 
sys.path.append('{}/Library/3{}'.format(os.getcwd(), sys.version_info[1]))
 
import argparse
import cv2
import SpoutSDK

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import HandTrackingModule as htm
import numpy as np
 
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

    handTrackingTracker = htm.HandMotionTracker(detectionConfidence=0.90, trackingConfidence=0.90)

# initalize np array of pixel size 1920 x 1080, third param is 3 because colors are stored in 3 RGBm and we will store in unsigned 8 bit int
    background = np.zeros((480, 640, 3))

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
        frame = cv2.flip(frame, 1 )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = handTrackingTracker.mapHands(frame)

        handPositionList = handTrackingTracker.retrievePosition(frame)

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
                cv2.circle(frame, (indexFingerPointX, indexFingerPointY), 17,  (255, 0, 255), cv2.FILLED)
                # print("drawMode")

                # first render when prevIndex = 0
                if(prevIndexFingerPointX == 0 and prevIndexFingerPointY == 0):
                    prevIndexFingerPointX = indexFingerPointX
                    prevIndexFingerPointY = indexFingerPointY

                # Might have to edit the last number of the last parameter for both lines below depennding on the system
                cv2.line(frame, (prevIndexFingerPointX, prevIndexFingerPointY), (indexFingerPointX, indexFingerPointY), (255, 0, 255), 12)
                cv2.line(background, (prevIndexFingerPointX, prevIndexFingerPointY), (indexFingerPointX, indexFingerPointY), (255, 0, 255), 30)

                # after something is drawn already
                indexFingerPointX = prevIndexFingerPointX
                indexFingerPointY = prevIndexFingerPointY

            else:
                nonDrawMode = True

        frame = cv2.addWeighted(frame, 1, background, 0.5, 0, dtype = 0)
        # print(frame.shape)

        

 
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