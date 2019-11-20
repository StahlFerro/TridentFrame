import os
import platform
import json
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

CACHE_DIRNAME = 'cache'
TEMP_DIRNAME = 'temp'

BIN_DIRNAME = 'bin'

def BIN_CONFILE():
    with open('config/config.json') as jsonfile:
        return json.load(jsonfile)



def ABS_CACHE_PATH():
    return os.path.abspath(CACHE_DIRNAME)


def ABS_TEMP_PATH():
    return os.path.abspath(TEMP_DIRNAME)


def imager_exec_path(binname: str) -> str:
    """ Get the path to the internal image processing binaries\n
        Supported binname params: ['gifsicle', 'imagemagick', 'apngasm', 'apngopt', 'apngdis']
    """
    if platform.system() == 'Windows':
        path = BIN_CONFILE()['win'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        path = BIN_CONFILE()['linux'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    return os.path.abspath(os.path.join(BIN_DIRNAME, path))


def gifsicle_exec() -> str:
    if platform.system() == 'Windows':
        path = BIN_CONFILE()['win']['gifsicle']
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        path = BIN_CONFILE()['linux']['gifsicle']
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    return os.path.abspath(os.path.join(BIN_DIRNAME, path))


def imagemagick_exec() -> str:
    if platform.system() == 'Windows':
        path = BIN_CONFILE()['win']['imagemagick']
        # return os.path.abspath("./bin/ImageMagick-7.0.8-61-win/convert.exe")
    elif platform.system() == 'Linux':
        path = BIN_CONFILE()['linux']['imagemagick']
        # return os.path.abspath("./bin/ImageMagick-7.0.8-61-unix/convert")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    return os.path.abspath(os.path.join(BIN_DIRNAME, path))


def apngasm_exec() -> str:
    if platform.system() == 'Windows':
        path = BIN_CONFILE()['win']['apngasm']
        # return os.path.abspath("./bin/ImageMagick-7.0.8-61-win/convert.exe")
    elif platform.system() == 'Linux':
        path = BIN_CONFILE()['linux']['apngasm']
        # return os.path.abspath("./bin/ImageMagick-7.0.8-61-unix/convert")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    return os.path.abspath(os.path.join(BIN_DIRNAME, path))
