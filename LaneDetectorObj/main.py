import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import glob
import cv2
from tracker import LaneTracker

def incBrightness(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	value = 42 #whatever value you want to add
	cv2.add(hsv[:,:,2], value, hsv[:,:,2])
	return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


vidCap = cv2.VideoCapture("http://192.168.137.210:8081")
cv2.startWindowThread()
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
#frame = cv2.imread("test_images/straightLane.jpg")
while True:
    #calibrated = calibrate()
    ret, frame = vidCap.read()
	#frame = incBrightness(frame)
    calibrated = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    lane_tracker = LaneTracker(calibrated)
    overlay_frame = lane_tracker.process(calibrated, draw_lane=True, draw_statistics=True)
    #mpimg.imsave(image_name.replace('test_images', 'output_images'), overlay_frame)
    #plt.imshow(overlay_frame)
    #plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    #plt.show()
    #break
    #radius = lane_tracker.radius_of_curvature()
    #print(radius)
    leftAmt = lane_tracker.left.camera_distance()
    rightAmt = lane_tracker.right.camera_distance()
    offset = (rightAmt - leftAmt)
    print(offset)
    overlay_frame = cv2.cvtColor(overlay_frame,cv2.COLOR_RGB2BGR)
    cv2.imshow("frame",overlay_frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break