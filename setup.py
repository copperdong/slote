import sys
import os

dir = os.getcwd() + '/bin'

if dir not in sys.path:
    sys.path.append(dir)
    print True
