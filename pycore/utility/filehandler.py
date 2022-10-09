import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from hashlib import sha1, sha256
from typing import List

from pycore.core_funcs import config

BLOCK_SIZE = 65536
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
    temp_dir = config.get_absolute_cache_dir().joinpath(dirname)
    # raise Exception(temp_dir, os.getcwd())
    Path.mkdir(temp_dir)
    return temp_dir


def empty_cache_dir(excluded_files: List[str]) -> None:
    excluded_files.append(".include")
    empty_directory_contents(config.get_absolute_cache_dir(), excluded_files)


def empty_previews_dir(excluded_files: List[str]) -> None:
    excluded_files.append(".include")
    empty_directory_contents(config.get_absolute_previews_dir(), excluded_files)


def empty_temp_dir(excluded_files: List[str]) -> None:
    excluded_files.append(".include")
    empty_directory_contents(config.get_absolute_temp_dir(), excluded_files)


def empty_directory_contents(target_dir: Path, excluded_files: List[str]) -> None:
    for item in target_dir.iterdir():
        try:
            if item.name not in excluded_files:
                if item.is_file():
                    os.unlink(item)
                elif item.is_dir():
                    shutil.rmtree(item)
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


def get_creation_time(path: Path) -> datetime:
    """Get file creation datetime

    Args:
        path (Path): Path to file

    Returns:
        datetime: Datetime of file creation
    """
    mtime = datetime.fromtimestamp(path.stat().st_ctime)
    return mtime


def get_modification_time(path: Path) -> datetime:
    """Get file latest modification time

    Args:
        path (Path): Path to file

    Returns:
        datetime: Datetime of file latest modification
    """
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return mtime


def hash_sha1(path: Path) -> str:
    """Get file SHA1 hash checksum

    Args:
        path (Path): Path to file

    Returns:
        str: Hash checksum
    """
    hasher = sha1()
    with open(path, "rb") as f:
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCK_SIZE)
    hashstr = hasher.hexdigest()
    return hashstr
