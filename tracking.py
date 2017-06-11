import cv2
import RPi.GPIO as GPIO
import numpy as np
import cv2
from math import floor

#pin list for the vaults to controll
chan_list = [7,8,9,10,11,23,24,25]

#gpio settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)
GPIO.output(chan_list, 0)

# HSV color thresholds for GREY
THRESHOLD_LOW = (0, 0, 0);
THRESHOLD_HIGH = (60, 60, 60);

# Resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Minimum required radius of enclosing circle of contour
MIN_RADIUS = 2

# trigger pin every time a object is tracked
def triggerPin(x,y):
        row = int(floor(x/(CAMERA_WIDTH/4)))
        col = int(floor(y/(CAMERA_HEIGHT / 2)))
        index = row + (col * 4)
        print("x:", x, "y:", y, "triggering index: " , index)
        for x in chan_list:
                GPIO.output(x, GPIO.LOW)
        GPIO.output(chan_list[index], GPIO.HIGH)
        return index

# test output writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (CAMERA_WIDTH,CAMERA_HEIGHT))
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera and get actual resolution
cam = cv2.VideoCapture(0)
cam.set(3, CAMERA_WIDTH)
cam.set(4, CAMERA_HEIGHT)
camWidth = cam.get(3)
camHeight = cam.get(4)
print "Camera initialized: (" + str(camWidth) + ", " + str(camHeight) + ")"

# Main loop
while True:

    # Get image from camera
    ret_val, img = cam.read()

    # Blur image to remove noise
    img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)

    # Convert image from BGR to HSV
    img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

    # Set pixels to white if in color range, others to black (binary bitmap)
    img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)

    # Dilate image to make white blobs larger
    img_binary = cv2.dilate(img_binary, None, iterations = 1)

    # Find center of object using contours instead of blob detection. From:
    # http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    img_contours = img_binary.copy()
    contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    # Find the largest contour and use it to compute the min enclosing circle
    center = None
    radius = 0
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < MIN_RADIUS:
                center = None

    # Print out the location and size (radius) of the largest detected contour
    if center != None:
        x, y = center
        print str(center) + " " + str(radius)
        text = str(triggerPin(x,y))
        cv2.putText(img,text,(30,30), font, 1,(0,0,100),2)

    # Draw a green circle around the largest enclosed contour
    if center != None:
        cv2.circle(img, center, int(round(radius)), (0, 255, 0))
    out.write(img)
