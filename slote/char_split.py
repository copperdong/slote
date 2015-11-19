import cv2
import numpy as np
from scipy.ndimage.measurements import center_of_mass

import matplotlib.pyplot as plt

def seperate(raw_image):
    #experiment with last two numbers to find least noisy result
    image_binary = cv2.adaptiveThreshold(raw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 27, 10)

    #plt.imshow(image_binary, cmap = 'gray', interpolation = 'none')
    #plt.show()


    contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    characters = []

    for i in range(len(contours)):
        image = np.ones(raw_image.shape)
        cv2.drawContours(image, contours, i, (0, 255, 0), thickness = 1)
        characters.append(image)


    characters = remove_noise(characters)

    centers = locate(characters)

    characters = merge_vertical(characters, centers)

    characters = order(characters, centers)

    return characters

def locate(characters): 
    #find the "center of mass" of the array

    centers = []

    for img in characters:
        image = invert_image(img)

        #center_of_mass returns a tuple
        centers.append(tuple([img, center_of_mass(image)]))

    return centers


def remove_noise(characters):
    #attempt to remove noise from characters by checking perimeter length
    char_actual = []
    for char in characters:
        image = invert_image(char)
        if np.sum(image) > 20.0:
            char_actual.append(char)

    return char_actual[1:]

def merge_vertical(characters, centers):
    #identify discontinuous characters like = or i

    char_merged = []
    char_merged_copy = list(characters)
    counted = []
    char_index = 0
    char_test_index = 0
    counter = 0

    for char in characters:
        char_test_index = 0

        for char_test in characters:
            delta = abs(centers[char_index][1][1] - centers[char_test_index][1][1])

            if delta < 0.01 * characters[char_index].shape[1] and delta > 0.0:
                merged = centers[char_index][0] + centers[char_test_index][0]
                char_merged.append(merged)
                
            char_test_index += 1
        char_index += 1

    print len(char_merged)

    char_merged = remove_duplicates(char_merged)

    print len(char_merged)

    return char_merged

def invert_image(char):
    #exchange ones and zeros to compensate for opencv convention

    image = np.zeros(char.shape)
    for row in range(char.shape[0]):
        for col in range(char.shape[1]):
            if char[row, col] == 1.0:
                image[row, col] = 0.0
            else:
                image[row, col] = 1.0
    return image

def remove_duplicates(characters):

    return characters

def order(characters, centers):

    return characters
