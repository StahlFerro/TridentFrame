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

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, gifsicle_exec, imagemagick_exec
from .criterion import ModificationCriteria
from .utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, _restore_disposed_frames, generate_gifsicle_args, generate_imagemagick_args


def modify_aimg(img_path: str, out_dir: str, criteria: ModificationCriteria):
    img_path = os.path.abspath(img_path)
    if not os.path.isfile(img_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    out_dir = os.path.abspath(out_dir)
    full_name = f"{criteria.name}.{criteria.format.lower()}"
    temp_dir = _mk_temp_dir(prefix_name="temp_mods")
    temp_save_path = os.path.join(temp_dir, full_name)
    sicle_args = generate_gifsicle_args(criteria)
    magick_args = generate_imagemagick_args(criteria)

    if sicle_args:
        args = [gifsicle_exec(), " ".join(sicle_args), img_path, "--output", temp_save_path]
        cmd = ' '.join(args)
        yield "Modifying gif..."
        subprocess.run(cmd, shell=True)
        yield "Finished"