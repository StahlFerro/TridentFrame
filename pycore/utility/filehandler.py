import os
import shutil
import time
from pathlib import Path

from pycore.core_funcs import config


SIZE_SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]


def mk_cache_dir(prefix_name: str = "") -> Path:
    """Creates a directory for temporary storage inside cache/, and then returns its absolute path

    Args:
        prefix_name (str, optional): Name of the temporary directory. Defaults to ''.

    Returns:
        Path: Absolute path of the created temporary directory
    """
    dirname = str(int(round(time.time() * 1000)))
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = config.get_absolute_cache_path().joinpath(dirname)
    # raise Exception(temp_dir, os.getcwd())
    Path.mkdir(temp_dir)
    return temp_dir


def empty_directory_contents(target_dir: Path) -> None:
    for stuff in os.listdir(target_dir):
        stuff_path = os.path.join(target_dir, stuff)
        try:
            name, ext = os.path.splitext(stuff_path)
            if os.path.isfile(stuff_path) and ext:
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            raise Exception(e)


def read_filesize(nbytes: int) -> str:
    """Convert bytes into a human-readable file size notation using the biggest unit suffix in which the numerical
    value is equal or greater than 1

    Args:
        nbytes (int): Amount of bytes

    Returns:
        str: Human-readable file size
    """
    i = 0
    while nbytes >= 1024 and i < len(SIZE_SUFFIXES) - 1:
        nbytes /= 1024.0
        i += 1
    size = str(round(nbytes, 3)).rstrip("0").rstrip(".")
    return f"{size} {SIZE_SUFFIXES[i]}"
