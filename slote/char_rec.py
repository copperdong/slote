import numpy as np
from sklearn import svm

class character:
    def __init__(self, raw_character):
        self.identity = None
        

def recognize(characters, classifier):
    for char in characters:
        data = np.reshape(char.image_centered, np.prod(char.image_centered.shape)).reshape(1, -1)
        char.identity = classifier.predict(data)
    return characters
