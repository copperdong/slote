#! /usr/bin/python

import cv2
import slote

def main():
    #filename = raw_input('Choose a photo to LaTeX (full path): ')
    filename = 'training_data/test/image1.jpeg'

    classifier = slote.train()

    #ask user for input image
    while True:
        try:
            raw_image = cv2.imread(filename, 0)
            break
        except IOError:
            filename = raw_input('Cannot open file; try again. ')

    #seperate characters into individual images
    characters = slote.seperate(raw_image)

    #identify each character
    identities = slote.recognize(characters, classifier)
