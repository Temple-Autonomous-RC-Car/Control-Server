#!/usr/bin/env python
# coding: utf-8

# In[7]:

import cv2
import time
import socket_man_test
import os
import ip
#from servoController.inputController import stop,drive,steer

directions = []
scale_factor = 1.3
min_neighbors = 10
min_size = (75, 75)
webcam=True #if working with video file then make it 'False'


def updateDirectionsList():
    f = open("directions.txt", "r")
    f1 = f.readlines()
    directionsBackward =[]
    for x in f1:
        directionsBackward.append(x)
    for i in range(0, len(directionsBackward)):
        directions.append(directionsBackward.pop())

def updateSteering(steer):
    socket_man_test.sendFormattedCommand("2 %.2f steer %.3f" % (time.time(),steer))
    print(steer)

def updateSpeed(speed):
    socket_man_test.sendFormattedCommand("2 %.2f drive %.3f" % (time.time(),speed))
    #socket_man_test.sendFormattedCommand("speed %.3f" % speed)
    print(speed)
def stopCommand(ts):
    socket_man_test.sendFormattedCommand("1 %.2f stop %.3f" % (time.time(),ts))

 

def detect(path):
    ipAddr = ip.PORTIP
    cascade = cv2.CascadeClassifier(path)
    if webcam:
        video_cap = cv2.VideoCapture("http://"+ipAddr) # use 0,1,2..depanding on your webcam
        video_cap.set(cv2.CAP_PROP_FPS, 30)
    else:
        video_cap = cv2.VideoCapture("stopvideo.MOV")
    
    #updateSteering(0)
   # WINDOW_NAME = "Object Detection"
   # cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
   # cv2.startWindowThread()
    #updateSpeed(0.26)
    while True:
        # Capture frame-by-frame
        ret, img = video_cap.read()
        
        if (ret==False):
            break
 
        #converting to gray image for faster video processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
        rects = cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors,
                                         minSize=min_size)
        # if at least 1 face detected
        if len(rects) > 0:
            stopCommand(3)    
            print("Object Detecting")
            turn()
            break
            #steer(-1)
            #drive(0.28)
            #time.sleep(1)
            #drive(0)
            # Display the resulting frame
           # r = 1000.0 / img.shape[1]
           # dim = (1000, int(img.shape[0] * r))
           # resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
           # cv2.imshow(WINDOW_NAME, resized)
            #wait for 'c' to close the application
           # if cv2.waitKey(1) & 0xFF == ord('q'):
            #    stop()
             #   break
    
    video_cap.release()
    
def main():
    updateDirectionsList()
    cascadeFilePath="stop.xml"
    try:
        detect(cascadeFilePath)
    except KeyboardInterrupt: 
        stopCommand(1)
        #stop()
            
    #cv2.destroyAllWindows()
        cv2.waitKey(1)
 
def turn():
    direction = directions.pop()
    print(direction)
    if "L" in direction:
        updateSteering(1)
    elif "R" in direction:
        updateSteering(-1)
    updateSpeed(0.26)
    time.sleep(3)
    updateSteering(0)
    updateSpeed(0.26)
    time.sleep(1)
    updateSpeed(0)

if __name__ == "__main__":
    main()


# In[ ]:
