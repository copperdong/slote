import cv2
import numpy as np
from scipy.ndimage.measurements import center_of_mass

import matplotlib.pyplot as plt

class RawCharacter:
    def __init__(self, img):
        self.super_script = [] #list of characters that are a superscript
        self.sub_script = [] #list of characters that are a subscript
        self.main_char_id = ['']
        self.image = img
        self.center = tuple([0,0])
        self.shape = np.shape(img)
        self.position = 0
        self.sub_characters = [img]
        self.image_centered = None
        self.contour = None
        self.id = 0
    #reform class to populate attributes when initialized
def seperate(raw_image):
    #apply a series of functions to populate class attributes

    characters = get_contours(raw_image)

    characters = remove_noise(characters)

    characters = locate(characters)

    characters = merge_vertical(characters)

    characters = order(characters)

    characters = center_image(characters)

    characters = fix_images(characters)

    return characters

def fix_images(characters):

    for char in characters:
        char.image = invert_image(char.image)
        char.image_centered = cv2.resize(invert_image(char.image_centered), char.shape)

    return characters

def get_contours(raw_image):
    #experiment with last two parameters to find least noisy result
    image_binary = cv2.adaptiveThreshold(raw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 27, 10)

    contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    characters = []
    counter = 0

    for i in range(len(contours)):
        image = np.ones(raw_image.shape)
        cv2.drawContours(image, contours, i, (0, 255, 0), thickness = 1)
        characters.append(RawCharacter(image))
        characters[i].contour = contours[i]

        characters[i].id = counter
        counter += 1

    return characters

def locate(characters): 
    #find the "center of mass" of the array

    for char in characters:
        image = invert_image(char.image)

        #center_of_mass returns a tuple
        char.center = center_of_mass(image)

    return characters


def remove_noise(characters):
    #attempt to remove noise from characters by checking perimeter length
    char_actual = []
    for char in characters:
        image = invert_image(char.image)

        if np.sum(image) > 20.0:
            char_actual.append(char)

    return char_actual[1:]

def merge_vertical(characters):
    #identify discontinuous characters like = or i
    
    char_index = 0
    char_test_index = 0
    tolerance = 0.01
    
    #add filter for characters on the same level
    for char in characters:
        char_test_index = 0
        merged = np.zeros(char.image.shape)
        for char_test in characters:
            delta = abs(char.center[1] - char_test.center[1])

            if delta < tolerance * char.shape[1] and delta > 0.0:
                char.image = normalize(char.image + char_test.image)
                char.sub_characters = [char, char_test]
                del characters[char_test_index]


            char_test_index += 1
        char_index += 1
    return characters

def invert_image(img):
    #exchange ones and zeros to compensate for opencv convention

    image_invert = np.zeros(img.shape)
    for row in range(image_invert.shape[0]):
        for col in range(image_invert.shape[1]):
            if img[row, col] == 1.0:
                image_invert[row, col] = 0.0
            else:
                image_invert[row, col] = 1.0
    return image_invert

def normalize(img):
    #normalize to ones and zeros

    image_norm = np.zeros(img.shape)
    for row in range(image_norm.shape[0]):
        for col in range(image_norm.shape[1]):
            if img[row, col] >= 2.0:
                image_norm[row, col] = 1.0
            else:
                image_norm[row, col] = 0.0
    return image_norm


def order(characters):
    #order characters by x coordinate
    characters.sort(key=lambda x: x.center[1])

    for char in characters:
        char.position = characters.index(char)

    return characters

def center_image(characters):

    for char in characters:
        col, row, col_len, row_len = cv2.boundingRect(char.contour)

        centered_img = char.image[row:row + row_len, col:col + col_len]
        char.image_centered = centered_img

    return characters

