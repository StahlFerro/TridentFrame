import json
# import numpy
import sys
import os
import traceback
from typing import Any
from pathlib import Path
from apng import FrameControl
from pycore.models import criterion
from pycore.models.diagnostics import CommandDiagnostics
from pycore.utility.encoders import JSONEncoderTrident


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


def debug(logmsg):
    msg = {"debug": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident))


def message(logmsg):
    msg = {"msg": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident))


def warn(logmsg: str):
    msg = {"warning": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident), file=sys.stderr)


def error(logmsg: Any):
    msg = {"error": logmsg}
    print(json.dumps(msg, cls=JSONEncoderTrident), file=sys.stderr)


def error_traceback(tb):
    msg = {"traceback": traceback.extract_tb(tb, limit=None).format()}
    print(json.dumps(msg, cls=JSONEncoderTrident), file=sys.stderr)


def control(logmsg: str):
    msg = {"CONTROL": logmsg}
    print(json.dumps(msg))


def preview_path(logpath: Path):
    msg = {"preview_path": str(logpath)}
    print(json.dumps(msg))


def report_diagnostics(diag: CommandDiagnostics):
    msg = {"diagnostics": diag.__dict__}
    print(json.dumps(msg))
