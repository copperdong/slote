import sys
import os

dir = os.getcwd()

if dir not in sys.path:
    sys.path.append(dir)
