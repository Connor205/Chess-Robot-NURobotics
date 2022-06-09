import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)
inputPoints = np.array([[114, 0], [1058, 0], [1094, 959], [110, 959]],
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
    dst = cv2.warpPerspective(frame, transform, (1280, 960))
    cv2.imshow('dst', resizeImage(dst, 50))
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()