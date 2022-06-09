import cv2
import time

# define a video capture object
vid = cv2.VideoCapture(0)

count = 0
success = True
while success:
    success, image = vid.read()
    cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    if cv2.waitKey(10) == 27:  # exit if Escape is hit
        break
    count += 1
    if count > 10:
        break
