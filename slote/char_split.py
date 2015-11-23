import cv2
import numpy as np
from scipy.ndimage.measurements import center_of_mass

import matplotlib.pyplot as plt

#try to change any tolerances to be dependent on the number of characters
#to avoid scaling issues

class RawCharacter:
    def __init__(self, img):
        self.super_script = [] #list of characters that are a superscript
        self.sub_script = [] #list of characters that are a subscript
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

    characters, image_binary = get_contours(raw_image)

    characters = remove_noise(characters)

    characters = locate(characters)

    characters = merge_vertical(characters)

    characters = order(characters)

    characters = center_image(characters)

    characters = fix_images(characters)

    #for char in characters:
        #plt.imshow(char.image, cmap = 'gray', interpolation = 'none')
        #plt.show()
    #characters = fix_relations(characters)

    return characters, image_binary

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

    return characters, image_binary

def locate(characters): 
    #find the "center of mass" of the array

    for char in characters:
        image = invert_image(char.image)
        char.center = center_of_mass(image)

    return characters


def remove_noise(characters):
    """attempt to remove noise from characters by checking perimeter length"""
    char_actual = []
    for char in characters:
        image = invert_image(char.image)

        if np.sum(image) > 15.0:
            char_actual.append(char)

    return char_actual[1:]

def merge_vertical(characters):
    """identify discontinuous characters like = or i"""
    
    char_index = 0
    char_test_index = 0
    tolerance_x = 0.02
    tolerance_y = 0.1

    #add filter for characters on the same level
    for char in characters:
        char_test_index = 0
        merged = np.zeros(char.image.shape)

        for char_test in characters:
            delta_x = abs(char.center[1] - char_test.center[1])
            delta_y = abs(char.center[0] - char_test.center[0])

            #check if characters are on the same line and not the same character
            if delta_y < tolerance_y * char.shape[0] and char_index != char_test_index:
                #check if characters are near each other 
                if delta_x < tolerance_x * char.shape[1]:
                    char.image = normalize(char.image + char_test.image)
                    char.sub_characters = [char, char_test]
                    del characters[char_test_index]

            char_test_index += 1
        char_index += 1
    return characters

def invert_image(img):
    """exchange ones and zeros to compensate for opencv convention"""

    image_invert = np.zeros(img.shape)
    for row in range(image_invert.shape[0]):
        for col in range(image_invert.shape[1]):
            if img[row, col] == 1.0:
                image_invert[row, col] = 0.0
            else:
                image_invert[row, col] = 1.0
    return image_invert

def normalize(img):
    """normalize to ones and zeros"""

    image_norm = np.zeros(img.shape)
    for row in range(image_norm.shape[0]):
        for col in range(image_norm.shape[1]):
            if img[row, col] >= 2.0:
                image_norm[row, col] = 1.0
            else:
                image_norm[row, col] = 0.0
    return image_norm

def center_image(characters):

    for char in characters:
        col, row, col_len, row_len = cv2.boundingRect(char.contour)

        centered_img = char.image[row:row + row_len, col:col + col_len]
        char.image_centered = centered_img

    return characters

def order(characters):
    """order characters on x, then y and establish superscripts and subscripts"""

#    characters.sort(key = lambda x: (x.center[0], x.center[1]))


    char_index = 0
    char_test_index = 0
    tolerance_x = 0.1
    tolerance_y = 0.01
    thresh = 0.1
    above = []
    below = []

    for char in characters:
        char_test_index = 0

        for char_test in characters:
            delta_x = char_test.center[1] - char.center[1]
            delta_y = char_test.center[0] - char.center[0]

            #check if characters are stacked and not the same character
            if abs(delta_x) < tolerance_x * char.shape[1] and char_index != char_test_index:

                 if delta_y < 0 and abs(delta_y) > tolerance_y * char.shape[0]:
                    if abs(delta_y) > thresh * char.shape[0]:
                         below.append(char_test)

                 elif delta_y > 0 and abs(delta_y) > tolerance_y * char.shape[0]:
                     if abs(delta_y) > thresh * char.shape[0]:
                         above.append(char_test)

            char_test_index += 1

        char.sub_script = below
        char.super_script = above

        char.super_script.extend(below)
        char.sub_script.extend(above)

            #char.super_script = char.super_script.sort(key = lambda x: x.super_script[x].center[1])
            #char.sub_script = char.sub_script.sort(key = lambda x: x.center[1])
        
        above = []
        below = []

        char_index += 1

    for char in characters:
        if len(char.super_script) > 1:
            print len(char.super_script)
            mat = np.add(char.super_script[0].image, char.super_script[1].image)
            plt.imshow(mat, cmap = 'gray', interpolation = 'none')
            plt.show()



#                    ch = [char, char_test]
#                    ch = ch.sort(key = lambda x: x.center[1])

#                    char.sub_characters = [char, char_test]
#                    del characters[char_test_index]


#        char_index += 1
    return characters
	
