#! /usr/bin/python

from scipy import misc

import training
import char_rec
import char_split

filename = raw_input('Choose a photo to LaTeX (full path): ')

classifier = training.train()

#ask user for input image
while True:
    try:
        raw_image = misc.imread(filename, flatten = True)
        break
    except IOError:
        filename = raw_input('Cannot open file; try again. ')

#seperate characters into individual images
characters = char_split(raw_image)

#identify each character
identities = char_rec(characters, classifier)
