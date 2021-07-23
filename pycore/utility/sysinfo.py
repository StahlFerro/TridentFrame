import os
import re
import psutil
from sys import platform
from enum import Enum, unique


@unique
class OS(Enum):
    WINDOWS = 0
    LINUX = 1
    MACOS = 2


@unique
class SHELL(Enum):
    CMD = 0
    POWERSHELL = 1
    BASH = 2
    SH = 3
    ZSH = 4
    FISH = 5
    OTHER = 99


def os_platform() -> OS:
    if platform.startswith('win') or platform.startswith('cygwin'):
        return OS.WINDOWS
    elif platform.startswith('linux'):
        return OS.LINUX
    elif platform.startswith('darwin'):
        return OS.MACOS


def parent_process_name() -> str:
    return psutil.Process(os.getppid()).name()


def shell_type() -> SHELL:
    pproc_name = parent_process_name()
    if bool(re.fullmatch('cmd|cmd.exe', pproc_name)):
        return SHELL.CMD
    elif bool(re.fullmatch('pwsh|pwsh.exe|powershell.exe', pproc_name)):
        return SHELL.POWERSHELL
    elif bool(re.fullmatch('bash|bash.sh|bash.exe', pproc_name)):
        return SHELL.BASH
    elif bool(re.fullmatch('sh', pproc_name)):
        return SHELL.SH
    elif bool(re.fullmatch('zsh', pproc_name)):
        return SHELL.ZSH
    elif bool(re.fullmatch('fish', pproc_name)):
        return SHELL.FISH
    else:
        return SHELL.OTHER
