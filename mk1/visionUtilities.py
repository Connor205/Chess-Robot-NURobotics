import cv2
import numpy as np
import time

vid = cv2.VideoCapture(0)
inputPoints = np.array([[114, 0], [1058, 0], [1094, 959], [110, 959]],
                       np.float32)
outputPoints = np.array([[0, 0], [960, 0], [960, 960], [0, 960]], np.float32)
transform = cv2.getPerspectiveTransform(inputPoints, outputPoints)


def get_image():
    ret, frame = vid.read()
    return frame


def get_perspective_image():
    image = get_image()
    return cv2.warpPerspective(image, transform, (960, 960))


def get_perspective_image_gray():
    image = get_perspective_image()
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def split_image_into_squares(image):
    size = 960
    square_size = int(size / 8)
    squares = []

    for i in range(0, 8):
        for j in range(7, -1, -1):
            squares.append(image[i * square_size:(i + 1) * square_size,
                                 j * square_size:(j + 1) * square_size])
    return squares


def save_image(image, name):
    cv2.imwrite(name, image)


def save_split_images():
    image = get_perspective_image_gray()
    squares = split_image_into_squares(image)
    for i, square in enumerate(squares):
        save_image(
            square,
            "unclassified/square_" + str(i) + '_' + str(time.time()) + ".png")
    save_image(image, "unclassified/full_image_" + str(time.time()) + ".png")


if __name__ == "__main__":
    save_split_images()