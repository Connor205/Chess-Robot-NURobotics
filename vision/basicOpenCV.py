# import the opencv library
import cv2
import cameratransform as ct

# define a video capture object
vid = cv2.VideoCapture(0)


def resizeImage(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    # print(frame.shape)
    # print(newFrame.shape)
    # print(topView.shape)
    # print('--')

    # Display the resulting frame
    cv2.imshow('frame', resizeImage(frame, 50))
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', resizeImage(img_gray, 50))
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()