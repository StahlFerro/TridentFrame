import json
import sys
import os
from typing import Any
from pathlib import Path


class UnbufferedStream(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, payload):
        self.stream.write(payload)
        self.stream.flush()

    def writelines(self, payload):
        self.stream.writelines(payload)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = UnbufferedStream(sys.stdout)
os.environ["PYTHONUNBUFFERED"] = "1"


def data(logdata: Any):
    msg = {"data": logdata}
    print(json.dumps(msg))


def debug(logmsg: str):
    msg = {"debug": logmsg}
    print(json.dumps(msg))


def message(logmsg: str):
    msg = {"msg": logmsg}
    print(json.dumps(msg))


def warn(logmsg: str):
    msg = {"warning": logmsg}
    print(json.dumps(msg))


def error(logmsg: str):
    msg = {"error": logmsg}
    print(json.dumps(msg), file=sys.stderr)


def control(logmsg: str):
    msg = {"CONTROL": logmsg}
    print(json.dumps(msg))


def preview_path(logpath: Path):
    msg = {"preview_path": str(logpath)}
    print(json.dumps(msg))