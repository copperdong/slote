import numpy as np
from sklearn import svm

def recognize(characters, classifier):
    identities = []
    for im in range(len(characters)):
        char = classifier.predict(np.reshape(characters[im], [1, 320 * 240]))
        identities.extend(char)
    return identities
