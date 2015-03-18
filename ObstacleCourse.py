from cv2 import *
from naoqi import *
import cv2
import numpy as np
import Image
import LeftKick
import time
import math

names = list()
times = list()
keys = list()
    
names.append("LHipYawPitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.00456, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.01538, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LHipRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.13810, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.13964, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LHipPitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ -0.28528, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ -0.56549, [ 3, -0.80000, 0.10950], [ 3, 0.06667, -0.00913]], [ -0.64117, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LKneePitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ 1.02007, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ 1.91812, [ 3, -0.80000, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.97558, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LAnklePitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ -0.69955, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ -0.46251, [ 3, -0.80000, -0.17606], [ 3, 0.06667, 0.01467]], [ -0.12736, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LAnkleRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.00311, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.00311, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RHipRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.11202, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.11202, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RHipPitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.20253, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.20406, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RKneePitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.83761, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.84528, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RAnklePitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.45862, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.46016, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RAnkleRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.23466, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.23466, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])


color_tracker_window = "Track Red Ball Now"
HEAD_ANGLE = 0.25

# Color Tracking Values
TENNIS_BALL_UPPER = cv.Scalar(0.10*256, 0.60*256, 0.20*256)
TENNIS_BALL_LOWER = cv.Scalar(0.15*256, 1.00*256, 1.00*256)
FOLDER_UPPER = 0
FOLDER_LOWER = 0

# NAO
IP = "169.254.238.191"
PORT = 9559
motionProxy = None
camProxy    = None
videoClient = None
ledProxy    = None

position   = 0
POSITION_1 = 1
POSITION_2 = 2
POSITION_3 = 3

state               = None
STATE_BEGIN         = 0
STATE_VICTORY_DANCE = 1
STATE_END           = 2

ballState    = 0
BALL_UNKNOWN = 0
BALL_FAR     = 1
BALL_MID     = 2
BALL_NEAR    = 3
BALL_AT_FEET = 4

robotState           = 0
ROBOT_MOVING_TO_BALL = 1
ROBOT_ROTATING_LEFT  = 2
ROBOT_ROTATING_RIGHT = 3
ROBOT_CENTERED       = 4

#MOVEMENTS
STOP_MOVEMENT = (0, 0, 0, 0)
ROTATE_R_MEDIUM = (0, -.35, .85)
ROTATE_L_MEDIUM = (0, .35, -.85)
ROTATE_R_HARD = (0, -.5, .75)
ROTATE_L_HARD = (0, .5, -.75)

TURN_R_15 = (0, 0, .26) #Turns Right 15 degrees
TURN_L_15 = (0, 0, -.26)  #Turns Left 15 degrees

#x, y, theta, velocity
DRIBBLE_SLOW = (.75, 0, 0, 0.05)
DRIBBLE_FAST = (.5, 0, 0, 1)

TIME_SHORT = 5
TIME_LONG = 10

#BALL AND CAMERA
x = None
y = None
CENTER_RANGE = 0.1
CAMERA_HEIGHT = 0
CAMERA_WIDTH = 0
center_x_start = 0
center_x_end   = 0
startFindingBall = None

def setHeadAngle(headAngle):
    CURRENT_HEAD = headAngle
    n  = ["HeadPitch"]
    angles  = [headAngle]
    fractionMaxSpeed  = 0.2
    motionProxy.setAngles(n, angles, fractionMaxSpeed)


def rotate(params):
    global state, ballState, robotState, position
    # Rotate around ball, then locateAndCenter
    print "rotating"
    motionProxy.moveTo(*params)
    locateAndCenter()
def dribble(params, seconds):
    global state, ballState, robotState, position
    print "dribbling"
    # bump the ball forward, walk to ball, then locateAndCenter
    timeout = time.time() + seconds
    while(True):
        if(time.time() > timeout):
            break
        motionProxy.setWalkTargetVelocity(*params)
    motionProxy.setWalkTargetVelocity(*STOP_MOVEMENT)
    locateAndCenter()

def locateAndCenter():
    global state, ballState, robotState, position, startFindingBall
    # Locate the ball, position robot behind ball
    ball_tracker.run()
    if(x == None and y == None):
        if(startFindingBall == None):
            motionProxy.moveTo(-.1, 0, 0)
            startFindingBall = True
        elif(startFindingBall == True):
            motionProxy.moveTo(0, 0, .3)
            startFindingBall = False
        elif(startFindingBall == False):
            motionProxy.moveTo(0, 0, -.6)
            startFindingBall = None
    else:
        startFindingBall = True
        robotState = 0
        ballState = BALL_UNKNOWN
        while(True):
            ball_tracker.run()
            print x, y
            if(y > 200):
                ballState = BALL_AT_FEET
            else:
                motionProxy.moveTo(.05, 0, 0)
            if(x < center_x_end and x > center_x_start):
                robotState = ROBOT_CENTERED
            else:
                if(x < center_x_start):
                    #move to the right some
                    motionProxy.moveTo(0, .05, 0)
                elif(x > center_x_end):
                    #move to the left some
                    motionProxy.moveTo(0, -.05, 0)

            if(robotState == ROBOT_CENTERED and ballState == BALL_AT_FEET):
                break

    print x, y, startFindingBall
def kick():
    global state, ballState, robotState, position
    # Hard kick to goal. /victory dance
    locateAndCenter()
    time.sleep(1)
    motionProxy.angleInterpolationBezier(names, times, keys)


def obstacleCourse():
    global state
    print '====Begin Obstacle Course===='

    obstacleState = 0
    state = STATE_BEGIN
    while(state == STATE_BEGIN):
        ball_tracker.run()
        if(obstacleState == 0):
            motionProxy.moveTo(*TURN_L_15)
            rotate(ROTATE_L_MEDIUM)
            obstacleState+=1
        elif(obstacleState == 1):
            dribble(DRIBBLE_FAST, TIME_SHORT)
            obstacleState+=1
        elif(obstacleState == 2):
            motionProxy.moveTo(*TURN_R_15)
            rotate(ROTATE_R_MEDIUM)
            obstacleState+=1
        elif(obstacleState == 3):
            dribble(DRIBBLE_FAST, TIME_LONG)
            obstacleState+=1
        elif(obstacleState == 4):
            motionProxy.moveTo(*TURN_R_15)
            kick()
        else:
            break
        if cv.WaitKey(10) == 27:
            break
    while(state == STATE_VICTORY_DANCE):
        # Do some legit victory dance
        if cv.WaitKey(10) == 27:
            break
    while(state == STATE_END):
        postureProxy.goToPosture("Crouch", 0.5)
        break

    print "====Program Ending===="

class BallTracker:

    def __init__(self):
        cv.NamedWindow(color_tracker_window, 1)


    def run(self):
        global state, ballState, robotState, position, center_x_start, center_x_end

        cv.NamedWindow(color_tracker_window, 1)

        img = camProxy.getImageRemote(videoClient)
        im = Image.fromstring("RGB", (img[0], img[1]), img[6])
        
        CAMERA_WIDTH, CAMERA_HEIGHT = im.size
        center_x_start = (CAMERA_WIDTH / 2) - \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)
        center_x_end = (CAMERA_WIDTH / 2) + \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)

        frame = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(frame, im.tostring(), im.size[0] * 3)

        img = frame
        cv.CvtColor(img, img, cv.CV_RGB2BGR)
        cv.ShowImage(color_tracker_window, img)
        cv.Smooth(img, img, cv.CV_BLUR, 3)

        hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

        thresholded_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)

        self.findBall(hsv_img, thresholded_img)
        #self.findFolder(hsv_img, thresholded_img)

    def findBall(self, hsv_img, thresh_img):
        global x, y
        #finds the ball
        cv.InRangeS(hsv_img, TENNIS_BALL_UPPER, TENNIS_BALL_LOWER, thresh_img)
        moments = cv.Moments(cv.GetMat(thresh_img), 0)
        area = cv.GetCentralMoment(moments, 0, 0)

        if(area > 10000):
            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)
        else:
            x = None
            y = None

#    def findFolder(self, hsv_img, thresh_img):
#        #finds the folder
#        cv.InRangeS(hsv_img, cv.Scalar(170, 100, 100), cv.Scalar(180, 255, 255), thresh_img)
#        moments = cv.Moments(cv.GetMat(thresh_img), 0)
#        area = cv.GetCentralMoment(moments, 0, 0)
#
#        contours, h = cv2.findContours(np.asarray(thresh_img[:,:]), 1, 2)
#        biggestContourSize = 0
#        biggestContour = None
#        for contour in contours:
#            if (len(contour) > biggestContourSize):
#                biggestContourSize = len(contour)
#                biggestContour = contour
#        if(biggestContour is not None):
#            # (x, y) point is not used, just holding a value
#            (x,y), radius = cv2.minEnclosingCircle(biggestContour)
#            radius = int(radius)
#            print "Contours: ", len(biggestContour)
#            print "Diameter: ", radius*2
#
#        if(area > 28000):
#            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
#            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)
#
#            print "Folder:  ",x, y

if __name__ == "__main__":
    camProxy        = ALProxy("ALVideoDevice", IP, PORT)
    motionProxy     = ALProxy("ALMotion", IP, PORT)
    postureProxy    = ALProxy("ALRobotPosture", IP, PORT)
    ledProxy        = ALProxy("ALLeds", IP, PORT)
    tts             = ALProxy("ALTextToSpeech", IP, PORT) 
    tts.setParameter("doubleVoice", 1)
    tts.setParameter("doubleVoiceLevel", 1)

    videoClient = camProxy.subscribe("pyclient3", 1, 11, 5)
    camProxy.setParam(18, 1)

    # We will need a loop here that calls ball_tracker.run(), then calls a method
    # to make the robot do movements based on the BALL_LOCATION results of ball_tracker.run()
    # BALL_LOCATION
    ball_tracker = BallTracker()

    ledProxy.off("FaceLeds")

    #Only needed for BUGS!
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    #Only needed for BUGS!

    postureProxy.goToPosture("Stand", 0.5)

    # Move to the ball, then back up slightly
    #tts.say("Stand back citizen! A ball needs to be kicked!")
    # Example showing how to set angles, using a fraction of max speed
    
    setHeadAngle(HEAD_ANGLE)
    obstacleCourse()
    postureProxy.goToPosture("Crouch", 0.5)

    camProxy.unsubscribe(videoClient)