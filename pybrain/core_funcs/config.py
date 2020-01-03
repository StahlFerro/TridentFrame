import os
import sys
import platform
import json
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

CACHE_DIRNAME = 'cache'
TEMP_DIRNAME = 'temp'

BIN_DIRNAME = 'bin'


def _bin_dirpath():
    if platform.system() == 'Windows':
        is_x64 = sys.maxsize > 2**32
        return os.path.join(BIN_DIRNAME, 'win64')
    elif platform.system() == 'Linux':
        return os.path.join(BIN_DIRNAME, 'linux')
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")


def _bin_confile():
    with open('config/config.json') as jsonfile:
        return json.load(jsonfile)


def ABS_CACHE_PATH():
    return os.path.abspath(CACHE_DIRNAME)


def ABS_TEMP_PATH():
    return os.path.abspath(TEMP_DIRNAME)


def imager_exec_path(binname: str) -> str:
    """ Get the path to the internal image processing binaries\n
        Supported binname params: ['gifsicle', 'imagemagick', 'apngasm', 'apngopt', 'apngdis', 'pngquant']
    """
    if platform.system() == 'Windows':
        path = _bin_confile()['win'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        path = _bin_confile()['linux'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    path = os.path.abspath(os.path.join(_bin_dirpath(), path))
    # Escape apostrophes
    path = path.replace("'", "''")
    return path