#! /usr/bin/python

import cv2
import slote
import numpy as np

def main():
    #filename = raw_input('Choose a photo to LaTeX (full path): ')
    filename = '../slote/training_data/image1.jpeg'

    classifier = slote.train()

    #ask user for input image
    raw_image = cv2.imread(filename, 0)

    while type(raw_image) is not np.ndarray:
        filename = raw_input('Image cannot be opened; try again: ')
        raw_image = cv2.imread(filename, 0)

    #seperate characters into individual images
    #returns a list of raw_character objects
    raw_characters = slote.seperate(raw_image)

    #identify each character
    characters = slote.recognize(raw_characters, classifier)
