from json import JSONEncoder
from pathlib import Path
from apng import APNG, FrameControl
import pycore.models.criterion as criterion


class JSONEncoderTrident(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, FrameControl):
            return obj.__dict__
        if isinstance(obj, criterion.CriteriaBase):
            return obj.__dict__
        # if isinstance(obj, numpy.ndarray):
        #     return obj.tolist()
        # if isinstance(obj, numpy.int32):
        #     return int(obj)
        return JSONEncoder.default(self, obj)
