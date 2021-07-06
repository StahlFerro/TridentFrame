import json
from json import JSONEncoder
# import numpy
import sys
import os
import traceback
from typing import Any
from pathlib import Path
from apng import FrameControl


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


class JSONEncoderTrident(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        if isinstance(obj, FrameControl):
            return obj.__dict__
        if isinstance(obj, Path):
            return str(obj)
        # if isinstance(obj, numpy.ndarray):
        #     return obj.tolist()
        # if isinstance(obj, numpy.int32):
        #     return int(obj)
        return JSONEncoder.default(self, obj)


sys.stdout = UnbufferedStream(sys.stdout)
os.environ["PYTHONUNBUFFERED"] = "1"


def data(logdata: Any):
    msg = {"data": logdata}
    print(json.dumps(msg))


def debug(logmsg):
    msg = {"debug": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident))


def message(logmsg):
    msg = {"msg": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident))


def warn(logmsg: str):
    msg = {"warning": logmsg}
    print(json.dumps(msg))


def error(logmsg: Any):
    msg = {"error": logmsg}
    print(json.dumps(msg), file=sys.stderr)


def error_traceback(tb):
    msg = {"traceback": traceback.extract_tb(tb, limit=None).format()}
    print(json.dumps(msg), file=sys.stderr)


def control(logmsg: str):
    msg = {"CONTROL": logmsg}
    print(json.dumps(msg))


def preview_path(logpath: Path):
    msg = {"preview_path": str(logpath)}
    print(json.dumps(msg))
