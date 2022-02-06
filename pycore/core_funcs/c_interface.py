import ctypes
import sys
from pathlib import Path, PurePosixPath
from sys import platform
import time
from PIL import Image
import itertools
import os
from pycore.core_funcs import stdio
from pycore.utility.sysinfo import os_platform, OS


# print(os.getcwd())
CLIB_PATH = Path("ccore/release/libtridentframe_cf.so").resolve()
# print(str(PurePosixPath(CLIB_PATH)))


if os_platform() == OS.WINDOWS:
    TRIDENT_CLIB = ctypes.WinDLL(str(CLIB_PATH))
elif os_platform() == OS.LINUX:
    TRIDENT_CLIB = ctypes.CDLL(str(CLIB_PATH))
elif os_platform() == OS.MACOS:
    TRIDENT_CLIB = ctypes.CDLL(str(CLIB_PATH))
else:
    TRIDENT_CLIB = ctypes.CDLL(str(CLIB_PATH))


def c_ping() -> str:
    TRIDENT_CLIB.ping.argtypes = []
    TRIDENT_CLIB.ping.restype = ctypes.c_char_p
    TRIDENT_CLIB.freeChar.argtypes = ctypes.c_void_p,
    TRIDENT_CLIB.freeChar.restype = None
    ping_ptr = TRIDENT_CLIB.ping()
    stdio.debug(ping_ptr)
    msg = ctypes.cast(ping_ptr, ctypes.c_char_p).value
    TRIDENT_CLIB.freeChar(ping_ptr)
    return msg
