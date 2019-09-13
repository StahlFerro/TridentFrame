import os
import io
import string
import shutil
import math
import time
import subprocess
import tempfile
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image
from apng import APNG, PNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ModificationCriteria, ABS_CACHE_PATH, gifsicle_exec, imagemagick_exec
from .utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, _restore_disposed_frames


def modify_aimg(img_path: str, out_dir: str, criteria: ModificationCriteria):
    pass
