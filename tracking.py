from tracking_util import *

# HSV color thresholds for GREY
THRESHOLD_LOW = (0, 0, 0)
THRESHOLD_HIGH = (60, 60, 60)

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
    radius = 0
    center = None

    if contours is not None:
        result = findLargestContour(contours)
        if result is not None:
            x, y, center = result

    if center != None:
        x, y = center
        text = str(triggerPin(x,y))
        # for debugging: put the triggered pin index on the video
        cv2.putText(img,text,(30,30), font, 1,(0,0,100),2)

    # Draw a green circle around the largest enclosed contour
    if center != None:
        cv2.circle(img, center, int(round(radius)), (0, 255, 0))
    out.write(img)

