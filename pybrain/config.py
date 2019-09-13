import os
import platform
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

CACHE_PATH = './cache/'
ABS_CACHE_PATH = os.path.abspath(CACHE_PATH)


def gifsicle_exec():
    if platform.system() == 'Windows':
        return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        return False

def imagemagick_exec():
    if platform.system() == 'Windows':
        return os.path.abspath("./bin/ImageMagick-7.0.8-61-win/convert.exe")
    elif platform.system() == 'Linux':
        return os.path.abspath("./bin/ImageMagick-7.0.8-61-unix/convert")
