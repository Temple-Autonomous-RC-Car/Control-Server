"""
This is just used to check for OpenCV and PyQt Versions
"""

import cv2
from PyQt5.Qt import PYQT_VERSION_STR


print ("OpenCV Version: ", cv2.__version__)
print("PyQt version:", PYQT_VERSION_STR)
