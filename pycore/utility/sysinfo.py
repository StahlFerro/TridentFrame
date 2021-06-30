from sys import platform
from enum import Enum, unique


@unique
class OS(Enum):
    WINDOWS = 0
    LINUX = 1
    MACOS = 2


def os_platform() -> OS:
    if platform.startswith('win') or platform.startswith('cygwin'):
        return OS.WINDOWS
    elif platform.startswith('linux'):
        return OS.LINUX
    elif platform.startswith('darwin'):
        return OS.MACOS
