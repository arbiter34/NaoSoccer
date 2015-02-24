from cv2 import *
from naoqi import *
import cv2
import numpy as np
import Image


# This is the range that the ball needs to be within such that we consider it
# centered on the screen. If the ball is within this range, the robot should
# move forward. So if the camera is 100x100 then the at x=50, the range of the
# center would be from x=35 to x=65. Obviously this value will need some tweaking
# and slowly get smaller as the robot moves towards the ball.
CENTER_RANGE = 0.20
CAMERA_WIDTH = 0
CAMERA_HEIGHT = 0

# Where the ball is on the screen.
LEFT_SIDE = -1
CENTER = 0
RIGHT_SIDE = 1
UNKNOWN = None
BALL_LOCATION = None
LAST_LOCATION = None

color_tracker_window = "Track Red Ball Now"

# NAO
motionProxy = None
camProxy = None
videoClient = None

TURN_RIGHT = -0.25
TURN_LEFT = 0.25
MOVE_FORWARD = .25
MOVE_BACKWARD = -.15


IP = "169.254.124.254"
PORT = 9559


class BallTracker:

    def __init__(self):
        cv.NamedWindow(color_tracker_window, 1)
        # self.capture = cv.CaptureFromCAM(1)

    def run(self):
        global BALL_LOCATION, LAST_LOCATION

        img = camProxy.getImageRemote(videoClient)
        im = Image.fromstring("RGB", (img[0], img[1]), img[6])
        
        CAMERA_WIDTH, CAMERA_HEIGHT = im.size
        center_x_start = (CAMERA_WIDTH / 2) - \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)
        center_x_end = (CAMERA_WIDTH / 2) + \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)

        frame = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(frame, im.tostring(), im.size[0] * 3)
        # cv.SaveImage("bb.png", frame)

        img = frame
        cv.CvtColor(img, img, cv.CV_RGB2BGR)
        # blur theself source image to reduce color noise
        cv.Smooth(img, img, cv.CV_BLUR, 3)

        # convert the image to hsv(Hue, Saturation, Value) so its
        # easier to determine the color to track(hue)
        hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

        thresholded_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)

        # Finds a red ball color! DO NOT DELETE THIS IT TOOK FOREVER TO GET THE RIGHT COLOR STUPID
        # OPENCV AND ITS BS WAY OF DOING HSV... /rant COMMENT OUT IF
        # NEEDED. :)
        cv.InRangeS(hsv_img, cv.Scalar(170, 100, 100), cv.Scalar(
            180, 255, 255), thresholded_img)

        # determine the objects moments and check that the area is large
        # enough to be our object
        moments = cv.Moments(cv.GetMat(thresholded_img), 0)
        area = cv.GetCentralMoment(moments, 0, 0)

        # there can be noise in the video so ignore objects with small areas
        # if(area > 100000):
        if(area > 15000):
            # determine the x and y coordinates of the center of the object
            # we are tracking by dividing the 1, 0 and 0, 1 moments by the
            # area
            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)

            # create an overlay to mark the center of the tracked object
            overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
            
            # shows the white dot on the object.
            # cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
            # cv.Add(img, overlay, img)

            if(x < center_x_start):
                BALL_LOCATION = LEFT_SIDE
                LAST_LOCATION = LEFT_SIDE
            elif(x > center_x_end):
                BALL_LOCATION = RIGHT_SIDE
                LAST_LOCATION = RIGHT_SIDE
            else:
                BALL_LOCATION = CENTER
                LAST_LOCATION = CENTER

        else:
            BALL_LOCATION = UNKNOWN

        cv.ShowImage(color_tracker_window, img)

if __name__ == "__main__":
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    motionProxy = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    videoClient = camProxy.subscribe("pyclient2", 1, 11, 5)
    camProxy.setParam(18, 1)

    # We will need a loop here that calls ball_tracker.run(), then calls a method
    # to make the robot do movements based on the BALL_LOCATION results of ball_tracker.run()
    # ball_tracier.run() will break out as soon as it finds the ball sets the
    # BALL_LOCATION
    ball_tracker = BallTracker()

    #Stand the robot up
    postureProxy.goToPosture("StandInit", 0.5)

    while True:
        ball_tracker.run()
        if (BALL_LOCATION == LEFT_SIDE):
            motionProxy.moveTo(0, 0, TURN_LEFT)
            print 'Turn Right'
        elif (BALL_LOCATION == RIGHT_SIDE):
            motionProxy.moveTo(0, 0, TURN_RIGHT)
            print 'Turn Left'
        elif (BALL_LOCATION == CENTER):
            motionProxy.moveTo(MOVE_FORWARD, 0, 0)
            print 'Walk Forward'
        else:
            if (LAST_LOCATION == LEFT_SIDE):
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            if (LAST_LOCATION == RIGHT_SIDE):
                motionProxy.moveTo(0, 0, TURN_LEFT)
            if (LAST_LOCATION == CENTER):
                motionProxy.moveTo(MOVE_BACKWARD, 0, 0)

        
        if cv.WaitKey(10) == 27:
            break

    camProxy.unsubscribe(videoClient)
