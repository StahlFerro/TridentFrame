from json import JSONEncoder
from pathlib import Path, WindowsPath
from apng import APNG, FrameControl
from PIL._imagingcms import CmsProfile
from numpy import isin
import pycore.models.criterion as criterion
from pycore.models.enums import ALPHADITHER


class JSONEncoderTrident(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return f"0x{obj.hex()}"
        elif isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, WindowsPath):
            return str(obj)
        elif isinstance(obj, FrameControl):
            return obj.__dict__
        elif isinstance(obj, criterion.CriteriaBase):
            return obj.__dict__
        else:
            return repr(obj)
        # elif type(obj) in ALPHADITHER.value:
        # if isinstance(obj, numpy.ndarray):
        #     return obj.tolist()
        # if isinstance(obj, numpy.int32):
        #     return int(obj)
        return JSONEncoder.default(self, obj)
