from LaneDetectorObj.tracker import LaneTracker
import socket_man_test
import cv2
from simple_pid import PID

pid = PID(.6, 0, .2, setpoint=0)
pid.output_limits = (-1, 1)

def updateSteering(steer):
    socket_man_test.sendFormattedCommand("steer %.3f " % steer)
    print(steer)

    
def offsetToSteeringAngle(value):
    """
    Negative means offset to the left.
    Positive means offset to the right.
    """
    steering = (value / 20) #+ (80 * (1/radius))
    return steering


ipAddr = "http://192.168.43.51:8081"

vidCap = cv2.VideoCapture(ipAddr)
steering = updateSteering(0)
pid.sample_time = 0.1
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
    except Exception as e:
        print(e.message)
        continue
    
    
    
    
    



