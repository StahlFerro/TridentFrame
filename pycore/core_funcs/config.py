import os
import json
import sys
import platform
import json
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

with open("./config/settings.json") as f:
    SETTINGS = json.loads(f.read())

CACHE_DIRNAME = SETTINGS['cache_dir']
TEMP_DIRNAME = 'temp'
BUFFERFILE_NAME = SETTINGS['bufferfile']
CRITERIONFILE_NAME = SETTINGS['criterionfile']

BIN_DIRNAME = 'bin'


def _bin_dirpath():
    if platform.system() == 'Windows':
        is_x64 = sys.maxsize > 2**32
        return os.path.join(BIN_DIRNAME, 'win64')
    elif platform.system() == 'Linux':
        return os.path.join(BIN_DIRNAME, 'linux')
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")


def imager_confile():
    with open('config/imagers.json', "r") as jsonfile:
        return json.load(jsonfile)


def ABS_CACHE_PATH():
    return os.path.abspath(CACHE_DIRNAME)


def ABS_TEMP_PATH():
    return os.path.abspath(TEMP_DIRNAME)


def ABS_BUFFERFILE_PATH():
    return os.path.abspath(os.path.join(ABS_CACHE_PATH(), BUFFERFILE_NAME))


def ABS_CRITERIONFILE_PATH():
    return os.path.abspath(os.path.join(ABS_CACHE_PATH(), CRITERIONFILE_NAME))



def imager_exec_path(binname: str) -> str:
    """ Get the path to the internal image processing binaries\n
        Supported binname params: ['gifsicle', 'imagemagick', 'apngasm', 'apngopt', 'apngdis', 'pngquant']
    """
    if platform.system() == 'Windows':
        path = imager_confile()['win'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        path = imager_confile()['linux'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    path = f"\"{os.path.abspath(os.path.join(_bin_dirpath(), path))}\""
    # Escape apostrophes
    # path = path.replace("'", "''")
    # path = f".'{path}'"
    return path


def get_bufferfile_content():
    bufferfile_path = ABS_BUFFERFILE_PATH()
    if not os.path.exists(ABS_CACHE_PATH()):
        os.mkdir(ABS_CACHE_PATH())
    if not os.path.exists(os.path.join(ABS_CACHE_PATH(), ".include")):
        open(os.path.join(ABS_CACHE_PATH(), ".include"), "").close()
    if not os.path.exists(bufferfile_path):
        open(bufferfile_path, "a").close()
    with open(bufferfile_path, "r") as f:
        paths = json.loads(f.read())
    return paths


def set_bufferfile_content(content):
    bufferfile_path = ABS_BUFFERFILE_PATH()
    if not os.path.exists(ABS_CACHE_PATH()):
        os.mkdir(ABS_CACHE_PATH())
    if not os.path.exists(os.path.join(ABS_CACHE_PATH(), ".include")):
        open(os.path.join(ABS_CACHE_PATH(), ".include"), "").close()
    if not os.path.exists(bufferfile_path):
        open(bufferfile_path, "a").close()
    with open(bufferfile_path, "w") as f:
        f.write(json.dumps(content))
    return

def get_criterionfile_content():
    criterionfile_path = ABS_CRITERIONFILE_PATH()
    if not os.path.exists(ABS_CACHE_PATH()):
        os.mkdir(ABS_CACHE_PATH())
    if not os.path.exists(os.path.join(ABS_CACHE_PATH(), ".include")):
        open(os.path.join(ABS_CACHE_PATH(), ".include"), "").close()
    if not os.path.exists(criterionfile_path):
        open(criterionfile_path, "a").close()
    with open(criterionfile_path, "r") as f:
        criteria = json.loads(f.read())
    return criteria

