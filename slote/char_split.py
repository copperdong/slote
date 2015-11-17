import cv2
import numpy as np

def seperate(raw_image):

    image_binary = cv2.adaptiveThreshold(raw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 20)


    contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print len(contours)

    characters = []

    for i in range(len(contours)):
        image = np.ones(raw_image.shape)
        cv2.drawContours(image, contours, i, (0, 255, 0), thickness = 1)
        characters.append(image)

    return characters

