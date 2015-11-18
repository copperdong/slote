import cv2
import numpy as np
from scipy.ndimage.measurements import center_of_mass

import matplotlib.pyplot as plt

def seperate(raw_image):
    # experiment with last two numbers to find least noisy result
    image_binary = cv2.adaptiveThreshold(raw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 27, 10)

    #plt.imshow(image_binary, cmap = 'gray', interpolation = 'none')
    #plt.show()


    contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    characters = []

    for i in range(len(contours)):
        image = np.ones(raw_image.shape)
        cv2.drawContours(image, contours, i, (0, 255, 0), thickness = 1)
        characters.append(image)
        #plt.imshow(image, cmap = 'gray', interpolation = 'none')
        #plt.show()
    print len(characters)
    centers = locate(characters)

    characters = remove_noise(characters)
    print len(characters)
    characters = merge_vertical(characters, centers)
    print len(characters)
    #characters = order(characters, centers)

    return characters

def locate(characters): 
    #find the "center of mass" of the array

    centers = []

    for char in characters:
        image = invert_image(char)

        #center_of_mass returns a tuple
        centers.append([int(center_of_mass(image)[0]), int(center_of_mass(image)[1])])

    return centers


def remove_noise(characters):
    #attempt to remove noise from characters by checking perimeter length

    for char in characters:
        char_actual = []
        image = invert_image(char)
        if np.sum(image) > 15.0:
            char_actual.append(image)
    return characters[1:]

def merge_vertical(characters, centers):
    #identify discontinuous charicters like = or i

    char_merged = []
    exempt = []

    for char in range(len(characters)):
        for char_test in range(len(characters)):

            if np.array_equal(characters[char], characters[char_test]):
                x_pos = centers[char][1]
                x_test_pos = centers[char][1]
                delta = x_pos - x_test_pos

                if delta < 0.1 * characters[char].shape[1] and (char_test not in exempt):
                    merged = characters[char] + characters[char_test]
                    char_merged.append(merged)
                    exempt.append(char_test)
                else:
                    char_merged.append(characters[char])

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
