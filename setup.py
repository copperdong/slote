import sys
import os

dir = os.getcwd() + '/slote'

if dir not in sys.path:
    sys.path.append(dir)
    print True
