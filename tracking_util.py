import RPi.GPIO as GPIO
from math import floor
import cv2

#pin list for the vaults to controll
chan_list = [7,8,9,10,11,23,24,25]
# this list contains active pins (indexes of the channel list)
# for now this will just hold one value,
# but we might have several active pins in the future
active_pins = []

# Resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

#gpio settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)
GPIO.output(chan_list, 0)

# Minimum required radius of enclosing circle of contour
MIN_RADIUS = 2


def findLargestContour(contours):
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < MIN_RADIUS:
                center = None
            return x, y, center


# trigger pin every time a object is tracked
def triggerPin(x,y):
        index = find_index(x,y)
        print("x:", x, "y:", y, "triggering index: " , index)

        if index not in active_pins:
            GPIO.output(chan_list[index], GPIO.HIGH)
            del active_pins[:]
            active_pins.append(index)

        for i in range(len(chan_list)):
            if i not in active_pins:
                GPIO.output(chan_list[i], GPIO.LOW)

        return index


def find_index(x, y):
    row = int(floor(x / (CAMERA_WIDTH / 4)))
    col = int(floor(y / (CAMERA_HEIGHT / 2)))
    return row + (col * 4)