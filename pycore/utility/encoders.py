from json import JSONEncoder
from pathlib import Path
from apng import APNG, FrameControl
from PIL._imagingcms import CmsProfile
import pycore.models.criterion as criterion


class JSONEncoderTrident(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return f"0x{obj.hex()}"
        elif isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, FrameControl):
            return obj.__dict__
        elif isinstance(obj, criterion.CriteriaBase):
            return obj.__dict__
        elif isinstance(obj, CmsProfile):
            return obj.__dict__
        # if isinstance(obj, numpy.ndarray):
        #     return obj.tolist()
        # if isinstance(obj, numpy.int32):
        #     return int(obj)
        return JSONEncoder.default(self, obj)
