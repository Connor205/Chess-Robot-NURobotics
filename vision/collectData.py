import numpy as np
import cv2
import time

# define a video capture object
vid = cv2.VideoCapture(0)
inputPoints = np.array([[195, 70], [964, 70], [1065, 850], [40, 850]],
                       np.float32)
outputPoints = np.array([[0, 0], [960, 0], [960, 960], [0, 960]], np.float32)
transform = cv2.getPerspectiveTransform(inputPoints, outputPoints)


def resizeImage(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', resizeImage(frame, 50))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.warpPerspective(gray, transform, (1280, 960))
    cv2.imshow('dst', resizeImage(dst, 50))

    for row in range(8):
        for col in range(8):
            img = dst[col * 120:(col + 1) * 120, row * 120:(row + 1) * 120]
            # save image to disk
            cv2.imwrite(
                'unclassifiedImages/' + str(row) + '_' + str(col) + "_" +
                str(time.time()) + '.jpg', img)
    print("Saved Images")

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(0)