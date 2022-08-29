import os
import platform
import json
import toml
from pathlib import Path

from pycore.core_funcs import stdio


IMG_EXTS = ["png", "jpg", "jpeg", "gif", "bmp", "tiff"]
STATIC_IMG_EXTS = ["png", "jpg", "jpeg", "bmp", "gif"]
ANIMATED_IMG_EXTS = ["gif", "png"]


# logger.message(f"On config.py, {os.getcwd()}")

with open("./config/engine.toml") as f:
    SETTINGS = toml.loads(f.read())


TEMP_DIR = SETTINGS["temp_dir"]
CACHE_DIR = SETTINGS["cache_dir"]
PREVIEWS_DIR = SETTINGS["previews_dir"]

BINARIES_DIR = Path("bin").resolve()


def _bin_platform_dir() -> Path:
    """Returns the absolute path to the OS-specific imaging binaries

    Raises:
        Exception: [description]

    Returns:
        Path: Absolute path of the imaging binaries
    """
    if platform.system() == "Windows":
        # is_x64 = sys.maxsize > 2 ** 32
        return BINARIES_DIR.joinpath("win64")
    elif platform.system() == "Linux":
        return BINARIES_DIR.joinpath("linux")
    else:
        raise Exception(
            f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}"
        )


# def imager_confile():
#     with open("config/imagers.json", "r") as jsonfile:
#         return json.load(jsonfile)


def get_absolute_cache_dir() -> Path:
    """Get the absolute path of the cache directory

    Returns:
        Path: Absolute path of the cache directory. Creates the directory if it doesn't exist
    """
    cache_dir = Path.cwd().joinpath(Path(CACHE_DIR).resolve())
    if not cache_dir.exists():
        os.makedirs(cache_dir)
    empty_file = cache_dir.joinpath(".include")
    if not empty_file.exists():
        open(empty_file, "x")
    return cache_dir


def get_absolute_previews_dir() -> Path:
    """Get the absolute path of the cache directory

    Returns:
        Path: Absolute path of the cache directory. Creates the directory if it doesn't exist
    """
    previews_dir = Path.cwd().joinpath(Path(PREVIEWS_DIR).resolve())
    if not previews_dir.exists():
        os.makedirs(previews_dir)
    empty_file = previews_dir.joinpath(".include")
    if not empty_file.exists():
        open(empty_file, "x")
    return previews_dir


def get_absolute_temp_dir() -> Path:
    """Get the absolute path of the temp directory

    Returns:
        Path: Asbolute path of the temp directory
    """
    temp_dir = Path(TEMP_DIR).resolve()
    if not temp_dir.exists():
        os.mkdir(temp_dir)
    empty_file = temp_dir.joinpath(".include")
    if not empty_file.exists():
        open(empty_file, "x")
    return temp_dir


def imager_exec_path(binname: str) -> Path:
    """Get the path to the internal image processing binaries\n
    Supported binname params: ['gifsicle', 'imagemagick', 'apngasm', 'apngopt', 'apngdis', 'pngquant']
    """
    # imager_dirfragment = ""
    bin_subdirname: str
    if platform.system() == "Windows":
        bin_subdirname = "win"
        # return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == "Linux":
        bin_subdirname = "linux"
        # return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        raise Exception(
            f"TridentFrame does not have the engine for processing images on this platform! {platform.system()}"
        )

    imager_dirfragment = SETTINGS["imagers"][bin_subdirname][binname]
    # path = f"\"{os.path.abspath(os.path.join(_bin_platform_dir(), path))}\""
    path = BINARIES_DIR.joinpath(bin_subdirname, imager_dirfragment)
    # Escape apostrophes
    # path = path.replace("'", "''")
    # path = f".'{path}'"
    return path
