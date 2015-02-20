from cv2 import *
import cv2
import numpy as np

#Where the ball is on the screen.
LEFT_SIDE 	= -1;
CENTER 		= 0;
RIGHT_SIDE 	= 1;

#This is the range that the ball needs to be within such that we consider it
#centered on the screen. If the ball is within this range, the robot should 
#move forward. So if the camera is 100x100 then the at x=50, the range of the
#center would be from x=35 to x=65. Obviously this value will need some tweaking
#and slowly get smaller as the robot moves towards the ball.
CENTER_RANGE = 0.30;
CAMERA_WIDTH = 0;

color_tracker_window = "Color Tracker"

class ColorTracker:

    def __init__(self):
        cv.NamedWindow( color_tracker_window, 1)
        self.capture = cv.CaptureFromCAM(1)

    def run(self):

    	cap = cv2.VideoCapture(1)
    	CAMERA_WIDTH = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)

    	center_x_start = (CAMERA_WIDTH/2) - int((CAMERA_WIDTH * CENTER_RANGE)/2)
    	center_x_end = (CAMERA_WIDTH/2) + int((CAMERA_WIDTH * CENTER_RANGE)/2)

    	print center_x_start
    	print center_x_end

        while True:
            img = cv.QueryFrame( self.capture )

            #blur theself source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 3)

            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)

            #Finds a red ball color! DO NOT DELETE THIS IT TOOK FOREVER TO GET THE RIGHT COLOR STUPID
            #OPENCV AND ITS BS WAY OF DOING HSV... /rant COMMENT OUT IF NEEDED. :)
            cv.InRangeS(hsv_img, cv.Scalar(170, 100, 100), cv.Scalar(180, 255, 255), thresholded_img)

            #determine the objects moments and check that the area is large  
            #enough to be our object 
            moments = cv.Moments(cv.GetMat(thresholded_img), 0)
            area = cv.GetCentralMoment(moments, 0, 0)

            #there can be noise in the video so ignore objects with small areas 
            #if(area > 100000):
            if(area > 1000):
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = int(cv.GetSpatialMoment(moments, 1, 0)/area)
                y = int(cv.GetSpatialMoment(moments, 0, 1)/area)

                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3)

                cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
                cv.Add(img, overlay, img)
                #add the thresholded image back to the img so we can see what was  
                #left after it was applied 
                cv.Merge(thresholded_img, None, None, None, img)

                if(x < center_x_start):
                	print 'turn right'
                elif(x > center_x_end):
                	print 'turn left'
                else:
                	print 'move forward'
            
            if(area < 1000):
            	print 'Ball not in view!'

            #display the image  
            cv.ShowImage(color_tracker_window, img)

            if cv.WaitKey(10) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()