import os
import json
import sys
import platform
import json
from pathlib import Path
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

print(json.dumps({"msg": f"On config.py, {os.getcwd()}"}))

with open("./config/settings.json") as f:
    SETTINGS = json.loads(f.read())

CACHE_DIRNAME = SETTINGS['cache_dir']
TEMP_DIRNAME = 'temp'
BUFFERFILE_NAME = SETTINGS['bufferfile']
CRITERIONFILE_NAME = SETTINGS['criterionfile']

BINARIES_DIR = Path('bin').resolve()


def _bin_dirpath() -> Path:
    """Returns the absolute path to the OS-specific imaging binaries

    Raises:
        Exception: [description]

    Returns:
        Path: Absolute path of the imaging binaries
    """
    if platform.system() == 'Windows':
        is_x64 = sys.maxsize > 2**32
        return BINARIES_DIR.joinpath('win64')
    elif platform.system() == 'Linux':
        return BINARIES_DIR.joinpath('linux')
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")


def imager_confile():
    with open('config/imagers.json', "r") as jsonfile:
        return json.load(jsonfile)


def ABS_CACHE_PATH() -> Path:
    """Get the absolute path of the cache directory

    Returns:
        Path: Absolute path of the cache directory
    """
    return Path(CACHE_DIRNAME).resolve()


def ABS_TEMP_PATH() -> Path:
    """Get the absolute path of the temp directory

    Returns:
        Path: Asbolute path of the temp directory
    """
    return Path(TEMP_DIRNAME).resolve()


def ABS_BUFFERFILE_PATH():
    return ABS_CACHE_PATH().joinpath(BUFFERFILE_NAME)


def ABS_CRITERIONFILE_PATH():
    return ABS_CACHE_PATH().joinpath(CRITERIONFILE_NAME)



def imager_exec_path(binname: str) -> Path:
    """ Get the path to the internal image processing binaries\n
        Supported binname params: ['gifsicle', 'imagemagick', 'apngasm', 'apngopt', 'apngdis', 'pngquant']
    """
    imager_dirfragment = ''
    if platform.system() == 'Windows':
        imager_dirfragment = imager_confile()['win'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        imager_dirfragment = imager_confile()['linux'][binname]
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}")
    
    # path = f"\"{os.path.abspath(os.path.join(_bin_dirpath(), path))}\""
    path = _bin_dirpath().joinpath(imager_dirfragment)
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

