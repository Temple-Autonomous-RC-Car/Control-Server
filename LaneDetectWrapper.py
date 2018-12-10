from LaneDetectorObj.tracker import LaneTracker
import socket_man_test
import cv2
from simple_pid import PID
import os
import ip
import time

#try:
#pid = PID(.4 or .3<best, .1, 1, setpoint=0) .26
pid = PID(.3, .1, 1, setpoint=0) 
#pid = PID(.5, .5, .8, setpoint=0)

pid.output_limits = (-1, 1)
def updateSteering(steer):
    """
    Priority timestamp command amount
    """
    socket_man_test.sendFormattedCommand("3 %.2f steer %.3f " % (time.time(),steer))
    print(steer)

    
def offsetToSteeringAngle(value):
    """
    Negative means offset to the left.
    Positive means offset to the right.
    """
    steering = (value / 10) #+ (80 * (1/radius))
    return steering


ipAddr = ip.PORTIP
vidCap = cv2.VideoCapture("http://"+ipAddr)
vidCap.set(cv2.CAP_PROP_FPS, 30)
steering = updateSteering(0)
pid.sample_time = 0.1
socket_man_test.sendFormattedCommand("3 %.2f drive %.3f " % (time.time(),.3))

while True:
    try:
        """
        Get offset and radius
        """
        ret, frame = vidCap.read()
        calibrated = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        lane_tracker = LaneTracker(calibrated)
        overlay_frame = lane_tracker.process(calibrated, draw_lane=False, draw_statistics=False)
        
        radius = lane_tracker.radius_of_curvature()
        leftAmt = lane_tracker.left.camera_distance()
        rightAmt = lane_tracker.right.camera_distance()
        offset = (rightAmt - leftAmt)
        steeringAngle = offsetToSteeringAngle(offset)
        #print("Steer-offset %f" % steeringAngle)
        print("Radius %d Left offset %.2f CM Right Offset %.2f CM Offset: %.2f CM" % (radius, leftAmt, rightAmt, offset))
        """
        Generate steering value with pid
        """
        control = pid(offsetToSteeringAngle(offset))
        
        """
        UpdateSteering with new control
        """
        updateSteering(control)
    except KeyboardInterrupt:
        socket_man_test.sendFormattedCommand("3 %.2f drive %.3f " % (time.time(),0))

        exit()
    except Exception as e:
        print(e)
        continue
    
    
    
    
    



