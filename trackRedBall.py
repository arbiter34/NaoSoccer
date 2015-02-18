from cv2.cv import *

img = LoadImage("/home/arbiter34/test-image2.jpg")
NamedWindow("opencv")
ShowImage("opencv",img)
WaitKey(0)