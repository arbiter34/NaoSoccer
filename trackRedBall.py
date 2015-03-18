from cv2 import *
from naoqi import *
import cv2
import numpy as np
import Image
import LeftKick
import time

# Hunters Kick = NAMES_LEFT, TIMES_LEFT, KEYS_LEFT
# My Internet Found Kick = names, times, keys


# This is the range that the ball needs to be within such that we consider it
# centered on the screen. If the ball is within this range, the robot should
# move forward. So if the camera is 100x100 then the at x=50, the range of the
# center would be from x=35 to x=65. Obviously this value will need some tweaking
# and slowly get smaller as the robot moves towards the ball.

CENTER_RANGE = 0.2
CENTER_RANGE_NEAR_FEET = 0.1
CENTER_RANGE_NORMAL = 0.2
CENTER_RANGE_GOALIE = 0.25

LEFT_FOOT_RANGE = 0.2

CAMERA_WIDTH = 0
CAMERA_HEIGHT = 0

# Where the ball is on the screen.
LEFT_SIDE = -1
CENTER = 0
RIGHT_SIDE = 1
LEFT_FOOT_ALIGNED = 2
MOVING_AWAY = 3
UNKNOWN = None
BALL_LOCATION = None
LAST_LOCATION = None
NEAR_FEET = False

goaliePosition = None
currentArea = None
previousArea = None

#Used to calculate the balls line of travel
x1 = 0
x2 = 0 
y1 = 0
y2 = 0
firstPass = True

color_tracker_window = "Track Red Ball Now"

# NAO
motionProxy = None
camProxy = None
videoClient = None
ledProxy = None

TURN_RIGHT = -0.15
TURN_LEFT = 0.15
MOVE_FORWARD_FAST = .2
MOVE_FORWARD_KICK = .07
MOVE_FORWARD_SLOW = .05
MOVE_BACKWARD = -.1
MOVE_FORWARD = MOVE_FORWARD_FAST
# NAO HEAD
HEAD_DOWN = .78
HEAD_FORWARD = .25
HEAD_GOALIE = .15
CURRENT_HEAD = HEAD_FORWARD

# States
state = 0
goalieState = 0

MOVING_TO_BALL = 0
PREPARING_KICK = 1
BEING_GOALIE = 2


IP = "169.254.238.191"
PORT = 9559

def setHeadAngle(headAngle):
    CURRENT_HEAD = headAngle
    n  = ["HeadPitch"]
    angles  = [headAngle]
    fractionMaxSpeed  = 0.2
    motionProxy.setAngles(n, angles, fractionMaxSpeed)

def goalieKick():
    print 'Moving to Ball!'
    global state

    state = BEING_GOALIE

    #If no state, do nothing and just show the camera
    while state == None:
        ball_tracker.run()

    if(state == BEING_GOALIE):
        print 'Setting Goalie Head Angle'
        postureProxy.goToPosture("Crouch", 0.5)
        setHeadAngle(HEAD_GOALIE)
        CENTER_RANGE = CENTER_RANGE_GOALIE

    while state == BEING_GOALIE:
        ball_tracker.run()
        if(goaliePosition == LEFT_SIDE):
            ledProxy.off("FaceLeds")
            ledProxy.on("LeftFaceLeds")
            print 'Dive Left!'
        elif(goaliePosition == RIGHT_SIDE):
            ledProxy.off("FaceLeds")
            ledProxy.on("RightFaceLeds")
            print 'Dive Right!'
        elif(goaliePosition == CENTER):
            ledProxy.on("FaceLeds")
            print 'Gaurd Center!'
        elif(goaliePosition == MOVING_AWAY):
           ledProxy.off("FaceLeds")
           print '---Ball Moving Away---'

    print 'no longer goalie'    
    #state = MOVING_TO_BALL

    CENTER_RANGE = CENTER_RANGE_NORMAL
    while state == MOVING_TO_BALL:
        ball_tracker.run()
        if (NEAR_FEET):
            if (BALL_LOCATION == LEFT_SIDE):
                motionProxy.moveTo(0, 0, TURN_LEFT)
            if (BALL_LOCATION == RIGHT_SIDE):
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            if (BALL_LOCATION == CENTER):
                motionProxy.moveTo(-.05, 0, 0)
                state = PREPARING_KICK
                #tts.say("Any last words?. Stupid ball!")
                print 'Preparing Kick!'
        elif (BALL_LOCATION == UNKNOWN):
            if (LAST_LOCATION == LEFT_SIDE):
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            if (LAST_LOCATION == RIGHT_SIDE):
                motionProxy.moveTo(0, 0, TURN_LEFT)
            if (LAST_LOCATION == CENTER):
                motionProxy.moveTo(-.05, 0, 0)

        elif (BALL_LOCATION == LEFT_SIDE):
            motionProxy.moveTo(0, 0, TURN_LEFT)
            print 'Turn Right'
        elif (BALL_LOCATION == RIGHT_SIDE):
            motionProxy.moveTo(0, 0, TURN_RIGHT)
            print 'Turn Left'
        elif (BALL_LOCATION == CENTER):
            motionProxy.moveTo(MOVE_FORWARD, 0, 0)
            print 'Walk Forward'

            if cv.WaitKey(10) == 27:
                break

    while state == PREPARING_KICK:
        ball_tracker.run()
        if (BALL_LOCATION == CENTER): #Normnally BALL_LOCATION == LEFT_LEG_ALIGNED
            print 'Power Up Kick!'
            motionProxy.moveTo(MOVE_FORWARD_KICK, 0, 0)
            #tts.say("Commence ball kicking!")
            time.sleep(1)
            motionProxy.angleInterpolationBezier(names, times, keys)
            break
        elif (BALL_LOCATION == LEFT_SIDE):
            print '1'
            motionProxy.moveTo(0, 0, TURN_LEFT)
        elif (BALL_LOCATION == RIGHT_SIDE or BALL_LOCATION == CENTER):
            print '2'
            motionProxy.moveTo(0, 0, TURN_RIGHT)
        elif (BALL_LOCATION == UNKNOWN):
            if (LAST_LOCATION == LEFT_SIDE):
                print '3'
                motionProxy.moveTo(0, 0, TURN_LEFT)
            elif (LAST_LOCATION == RIGHT_SIDE):
                print '4'
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            else:
                print '5'
                motionProxy.moveTo(-.05, 0, 0)

        if cv.WaitKey(10) == 27:
            break

class BallTracker:

    def __init__(self):
        cv.NamedWindow(color_tracker_window, 1)
        # self.capture = cv.CaptureFromCAM(1)

    def run(self):
        global BALL_LOCATION, LAST_LOCATION, MOVE_FORWARD, CURRENT_HEAD, NEAR_FEET, CENTER_RANGE, goaliePosition
        global x1, x2, y1, y2, firstPass, previousArea, currentArea
        cv.NamedWindow(color_tracker_window, 1)

        img = camProxy.getImageRemote(videoClient)
        im = Image.fromstring("RGB", (img[0], img[1]), img[6])
        
        CAMERA_WIDTH, CAMERA_HEIGHT = im.size

        center_x_start = (CAMERA_WIDTH / 2) - \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)
        center_x_end = (CAMERA_WIDTH / 2) + \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)

        left_foot_start = 60
        left_foot_end   = 60+(CAMERA_WIDTH * LEFT_FOOT_RANGE)

        frame = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(frame, im.tostring(), im.size[0] * 3)
        # cv.SaveImage("bb.png", frame)

        img = frame
        cv.CvtColor(img, img, cv.CV_RGB2BGR)
        cv.ShowImage(color_tracker_window, img)
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
        #print area
        if(area > 28000):
            # determine the x and y coordinates of the center of the object
            # we are tracking by dividing the 1, 0 and 0, 1 moments by the
            # area
            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)

            if (state == BEING_GOALIE):
                if (firstPass):
                    previousArea = area
                    x1 = x;
                    y1 = y;
                    firstPass = False
                else:
                    currentArea = area
                    #Get the x-intercept to calculate where the ball is going
                    xIntercept = None
                    x2 = x;
                    y2 = y;

                    #print '(', x1, ',', y1, ') (', x2, ',', y2, ')'
                    try:
                        slope = (float(y2)-y1)/(float(x2)-x1)
                    except ZeroDivisionError:
                        #Line is vertical
                        slope = None

                    yIntercept = None
                    if(slope != None):
                        yIntercept = y1 - slope * x1

                    if (slope != 0 and slope):
                        xIntercept = float((CAMERA_HEIGHT - float(yIntercept))) / float(slope)
                        
                        if(currentArea > previousArea):
                            if(xIntercept < center_x_start):
                                goaliePosition = LEFT_SIDE
                            elif(xIntercept > center_x_end):
                                goaliePosition = RIGHT_SIDE
                            else:
                                goaliePosition = CENTER
                        else:
                            goaliePosition = MOVING_AWAY

                    firstPass = True

            else:
                if(x < center_x_start):
                    BALL_LOCATION = LEFT_SIDE
                    LAST_LOCATION = LEFT_SIDE
                elif(x > center_x_end):
                    BALL_LOCATION = RIGHT_SIDE
                    LAST_LOCATION = RIGHT_SIDE
                else:
                    BALL_LOCATION = CENTER
                    LAST_LOCATION = CENTER

                if(CURRENT_HEAD == HEAD_DOWN):
                    if(y > (CAMERA_HEIGHT/2)):
                        print '---Ball is near feet!---'
                        CENTER_RANGE = CENTER_RANGE_NEAR_FEET
                        NEAR_FEET = True

                if(y > (CAMERA_HEIGHT - (CAMERA_HEIGHT/3))):
                    print '----HEAD NOW DOWN----'
                    CURRENT_HEAD = HEAD_DOWN
                    MOVE_FORWARD = MOVE_FORWARD_SLOW
                    setHeadAngle(HEAD_DOWN)
                #else:
                #    print '----HEAD NOW FORWARD----'
                #    setHeadAngle(HEAD_FORWARD)
                #    MOVE_FORWARD = MOVE_FORWARD_FAST

                #print 'x: ', x, ' left end:', left_foot_end
                #if((x < left_foot_end and x > left_foot_start) and state == PREPARING_KICK):
                #    print 'LEFT_FOOT_ALIGNED'
                #    BALL_LOCATION = LEFT_FOOT_ALIGNED



        else:
            BALL_LOCATION = UNKNOWN

if __name__ == "__main__":
    camProxy        = ALProxy("ALVideoDevice", IP, PORT)
    motionProxy     = ALProxy("ALMotion", IP, PORT)
    postureProxy    = ALProxy("ALRobotPosture", IP, PORT)
    ledProxy        = ALProxy("ALLeds", IP, PORT)
    tts             = ALProxy("ALTextToSpeech", IP, PORT) 
    tts.setParameter("doubleVoice", 1)
    tts.setParameter("doubleVoiceLevel", 1)

    videoClient = camProxy.subscribe("pyclient1", 1, 11, 5)
    camProxy.setParam(18, 1)

    # We will need a loop here that calls ball_tracker.run(), then calls a method
    # to make the robot do movements based on the BALL_LOCATION results of ball_tracker.run()
    # BALL_LOCATION
    ball_tracker = BallTracker()

    ledProxy.off("FaceLeds")

    #Stand the robot up
    postureProxy.goToPosture("Stand", 0.5)

    # Move to the ball, then back up slightly
    #tts.say("Stand back citizen! A ball needs to be kicked!")
    # Example showing how to set angles, using a fraction of max speed
    
    setHeadAngle(HEAD_FORWARD)
    goalieKick()
    postureProxy.goToPosture("Crouch", 0.5)

    camProxy.unsubscribe(videoClient)